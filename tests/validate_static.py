#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ALLOWED_FILES = {
    "index.html",
    "assets/portal.css",
    "assets/portal.js",
}
REQUIRED_FILES = {SITE / relative for relative in ALLOWED_FILES}

SECRET_PATTERNS = {
    "github_token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    "github_pat": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "jwt_like": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
}

FORBIDDEN_REFERENCES = (
    "api.homosapiens.id",
    "HS_API_BASE",
    "/v1/",
    "/admin/",
    "/tokens/",
    "fetch(",
    "XMLHttpRequest",
    "WebSocket",
    "EventSource",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
)

class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.labels: list[str] = []
        self.references: list[str] = []
        self.buttons_without_type: list[str] = []
        self.html_lang = ""
        self.viewport = False
        self.referrer = False
        self.csp = False
        self._button_index = 0

    def handle_starttag(self, tag, attrs):
        values = {key: value or "" for key, value in attrs}
        if tag == "html":
            self.html_lang = values.get("lang", "")
        if tag == "meta" and values.get("name", "").lower() == "viewport":
            self.viewport = bool(values.get("content"))
        if tag == "meta" and values.get("name", "").lower() == "referrer":
            self.referrer = values.get("content") == "no-referrer"
        if tag == "meta" and values.get("http-equiv", "").lower() == "content-security-policy":
            self.csp = "default-src 'self'" in values.get("content", "")
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "label" and values.get("for"):
            self.labels.append(values["for"])
        if tag in {"script", "img"} and values.get("src"):
            self.references.append(values["src"])
        if tag == "link" and values.get("href"):
            self.references.append(values["href"])
        if tag == "button":
            self._button_index += 1
            if not values.get("type"):
                self.buttons_without_type.append(values.get("id") or f"button#{self._button_index}")

def local_reference(page: Path, reference: str):
    parsed = urlparse(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("#", "data:", "mailto:", "tel:", "/")):
        return None
    return (page.parent / parsed.path).resolve()

def validate_text(path: Path, text: str) -> list[str]:
    failures: list[str] = []
    for name, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            failures.append(f"{path}: possible {name} committed")
    if "http://" in text:
        failures.append(f"{path}: insecure HTTP endpoint detected")
    for forbidden in FORBIDDEN_REFERENCES:
        if forbidden in text:
            failures.append(f"{path}: forbidden external/runtime reference: {forbidden}")
    return failures

def validate_page(page: Path) -> list[str]:
    failures: list[str] = []
    text = page.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)

    duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicates:
        failures.append(f"{page}: duplicate ids: {', '.join(duplicates)=")
    missing_targets = sorted(set(parser.labels) - set(parser.ids))
    if missing_targets:
        failures.append(f"{page}: labels without target: {', '.join(missing_targets)}")
    if parser.buttons_without_type:
        failures.append(f"{page}: buttons without explicit type: {', '.join(parser.buttons_without_type)}")
    if parser.html_lang.lower() != "pt-br":
        failures.append(f"{page}: html lang must be pt-BR")
    if not parser.viewport:
        failures.append(f"{page}: viewport meta is required")
    if not parser.referrer:
        failures.append(f"{page}: no-referrer policy is required")
    if not parser.csp:
        failures.append(f"{page}: restrictive Content-Security-Policy is required")
    if "<main" not in text or 'id="conteudo"' not in text:
        failures.append(f"{page}: accessible main landmark is missing")
    if "skip-link" not in text:
        failures.append(f"{page}: skip link is missing")

    for reference in parser.references:
        target = local_reference(page, reference)
        if target is not None and not target.is_file():
            failures.append(f"{page}: missing referenced asset: {reference}")

    failures.extend(validate_text(page, text))
    return failures

def main() -> int:
    failures: list[str] = []

    actual_files = {
        str(path.relative_to(SITE)).replace("\\", "/")
        for path in SITE.rglob("*")
        if path.is_file()
    }
    unexpected = sorted(actual_files - ALLOWED_FILES)
    missing = sorted(ALLOWED_FILES - actual_files)
    if unexpected:
        failures.append(f"unexpected files in published site: {', '.join(unexpected)}")
    if missing:
        failures.append(f"missing required published files: {', '.join(missing)}")

    for path in REQUIRED_FILES:
        if not path.is_file():
            failures.append(f"missing required file: {path}")

    if not failures:
        failures.extend(validate_page(SITE / "index.html"))

        for path in (SITE / "assets" / "portal.js", SITE / "assets" / "portal.css"):
            text = path.read_text(encoding="utf-8")
            failures.extend(validate_text(path, text))

        portal_js = (SITE / "assets" / "portal.js").read_text(encoding="utf-8")
        if "online" in portal_js.lower():
            failures.append("portal.js must not claim products are online")
        if "external_request_sent: false" not in portal_js:
            failures.append("local sandbox must explicitly record that no external request was sent")
        if "executed: false" not in portal_js:
            failures.append("local sandbox must explicitly record that no execution occurred")

        css = (SITE / "assets" / "portal.css").read_text(encoding="utf-8")
        if css.count("{") != css.count("}"):
            failures.append("portal.css: unbalanced CSS braces")
        for required in (":focus-visible", "@media", "prefers-reduced-motion", ".skip-link"):
            if required not in css:
                failures.append(f"portal.css missing accessibility/responsive rule: {required}")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print("static-site validation: PASS")
    print(f"allowlist={len(ALLOWED_FILES)} mode=static-only")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
