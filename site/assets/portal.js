(() => {
  const sandbox = Object.freeze({
    external_request_sent: false,
    executed: false
  });

  const products = [
    ['Intuitus','PESQUISA · CONTEXTO','Pesquisa com contexto, fontes e sínteses.','https://intuitus.homosapiens.id'],
    ['Sensus','PERCEPÇÃO · SINAIS','Integra sinais, padrões, riscos e oportunidades.','https://sensus.homosapiens.id'],
    ['Littera','LINGUAGEM · ESCRITA','Revisão, reescrita, adaptação e tradução.','https://littera.homosapiens.id'],
    ['Vita','SAÚDE · CIÊNCIAS DA VIDA','Formação e pesquisa educacional em saúde.','https://vita.homosapiens.id'],
    ['Visio','IMAGEM · AVATAR · VOZ · VÍDEO','Estúdio multimodal para imagem, avatar, voz e animação.','https://visio.homosapiens.id']
  ];

  const grid = document.getElementById('product-grid');
  grid.innerHTML = products.map(([name,kicker,description,url]) => `
    <article class="product">
      <span class="kicker">${kicker}</span>
      <h3>${name}</h3>
      <p>${description}</p>
      <a href="${url}" rel="noopener">Abrir ${name} →</a>
    </article>
  `).join('');

  void sandbox;
})();