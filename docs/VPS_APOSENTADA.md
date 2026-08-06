# VPS aposentada

Estado vigente desde 2026-08-06.

## Fonte de verdade

- O portal público `homosapiens.id` é publicado por GitHub Pages a partir de `site/`.
- A antiga VPS Hostinger `1799286` está suspensa e não faz parte da arquitetura ativa.
- Nenhuma API, runner, autenticação ou console administrativo está hospedado no portal estático.

## Legado

Os diretórios `ops/` e documentos históricos referentes a Docker, Caddy, deploy em VPS e rollback de servidor são preservados apenas para auditoria histórica.

Eles não devem ser executados como procedimento vigente.

## Regra operacional

Qualquer backend futuro deve ter:

1. infraestrutura própria definida;
2. escopo e alvo identificados;
3. backup e rollback;
4. segregação de clientes;
5. ausência de segredos no repositório;
6. pós-teste;
7. evidência técnica;
8. homologação específica.

Sem esses requisitos, o estado correto é `não publicado`.
