(() => {
  'use strict';

  const catalog = [
    {
      slug: 'lex-juridica',
      name: 'Lex Jurídica',
      description: 'Demonstração de estruturas e contratos para apresentação de conteúdo jurídico público.',
      status: 'demonstração',
      operations: ['pesquisa', 'saúde', 'metadados'],
    },
    {
      slug: 'lex-search-core',
      name: 'Lex Search Core',
      description: 'Demonstração de modelos de pesquisa, citação e rastreabilidade.',
      status: 'demonstração',
      operations: ['pesquisa', 'metadados'],
    },
    {
      slug: 'datajud-connector',
      name: 'DataJud Connector',
      description: 'Demonstração de contratos para consultas públicas a metadados processuais.',
      status: 'demonstração',
      operations: ['pesquisa', 'saúde', 'metadados'],
    },
  ];

  const grid = document.getElementById('api-grid');
  const form = document.getElementById('sandbox-form');
  const result = document.getElementById('sandbox-result');

  function escapeHtml(value) {
    return String(value)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  function renderCatalog() {
    grid.innerHTML = catalog.map((item) => `
      <article class="card">
        <div class="card-head">
          <h3>${escapeHtml(item.name)}</h3>
          <span class="status status-preview"><span aria-hidden="true"></span> ${escapeHtml(item.status)}</span>
        </div>
        <p>${escapeHtml(item.description)}</p>
        <ul class="tags">${item.operations.map((op) => `<li>${escapeHtml(op)}</li>`).join('')}</ul>
        <p class="muted">Sem endpoint produtivo publicado.</p>
      </article>
    `).join('');
  }

  function renderLocalResult(event) {
    event.preventDefault();
    const product = document.getElementById('sandbox-product').value;
    const operation = document.getElementById('sandbox-operation').value;
    const query = document.getElementById('sandbox-query').value.trim();

    const payload = {
      mode: 'demonstracao-local',
      product,
      operation,
      query: query || null,
      executed: false,
      external_request_sent: false,
      note: 'Resultado sintético gerado no navegador. Nenhum serviço externo foi consultado.',
    };

    result.innerHTML = `<p>Demonstração local gerada.</p><pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre>`;
  }

  renderCatalog();
  form.addEventListener('submit', renderLocalResult);
})();
