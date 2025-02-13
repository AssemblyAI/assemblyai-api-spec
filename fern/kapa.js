function insertKapa() {
  const originalElement = document.getElementById('fern-search-button');
  const clonedElement = originalElement.cloneNode(true);
  originalElement.parentNode.replaceChild(clonedElement, originalElement);
  
  const newElement = document.getElementById('fern-search-button');
  newElement.disabled = false;
  
  const script = document.createElement("script");
  script.src = "https://widget.kapa.ai/kapa-widget.bundle.js";
  script.async = true;
  script.setAttribute("data-website-id", "42353092-36d7-42bd-a213-6fd7af0de0cd");
  script.setAttribute("data-project-name", "AssemblyAI");
  script.setAttribute("data-project-color", "#2C4BD4");
  script.setAttribute("data-project-logo", "https://www.assemblyai.com/static/images/logo-blue400x400.jpeg");
  script.setAttribute("data-modal-override-open-id-search", "fern-search-button");
  script.setAttribute("data-search-include-source-names", '["Pylon FAQ", "Documentation"]');
  document.head.appendChild(script);
  
  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
      e.preventDefault();
      document.getElementById('fern-search-button').click();
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  insertKapa();
});

if (document.readyState === 'complete' || document.readyState === 'interactive') {
  insertKapa();
}
