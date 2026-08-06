# homosapiens-site

Portal público estático de `homosapiens.id`.

## Fonte vigente

- Conteúdo publicado: `site/index.html`, `site/assets/portal.css` e `site/assets/portal.js`.
- Hospedagem: GitHub Pages.
- Publicação: `.github/workflows/pages.yml`.
- Validação: `tests/validate_static.py` e `.github/workflows/ci.yml`.
- O artefato publicado usa allowlist explícita e não contém backend, autenticação, tokens ou console administrativo.

## Produção

- Domínio: `https://homosapiens.id`
- Alias: `https://www.homosapiens.id`
- A antiga VPS `76.13.226.21` está aposentada e não integra a arquitetura vigente.

## Legado

Os diretórios `ops/` e documentos históricos de VPS em `docs/` são preservados somente para auditoria histórica. Não devem ser executados como procedimento operacional atual.

A referência de aposentadoria é `docs/VPS_APOSENTADA.md`.

## Regra operacional

Publicação real é ação A4. O deploy só ocorre após validação da allowlist, segurança básica, sintaxe JavaScript e correspondência com o commit exato.
