(function () {
  let k = window.Kapa;
  if (!k) {
    let i = function () {
      i.c(arguments);
    };
    i.q = [];
    i.c = function (args) {
      i.q.push(args);
    };
    window.Kapa = i;
  }
})();

// track event for kapa modal opening
window.Kapa("onModalOpen", function ({ mode }) {
  rudderanalytics.track("docs_click_search-open",
    {
      "search_mode": mode,
    });
  if(rudderanalytics.getUserId()!=='') {
    window.kapaSettings = {
      user: {
        uniqueClientId: rudderanalytics.getUserId(),
        email: rudderanalytics.getUserTraits().email
      }
    }
  }
});

// track event for kapa modal closing
window.Kapa("onModalClose", function ({ mode }) {
  rudderanalytics.track("docs_click_search-close",
    {
      "search_mode": mode,
    });
});

// track event for kapa modal search completing
window.Kapa("onSearchResultsCompleted", ({ query, searchResults }) => {
  const searchInput = document
    .querySelector("#kapa-widget-container")
    .shadowRoot.querySelector("input[type=text]");
  rudderanalytics.track("docs_completed_search",
    {
      "search_query": query,
      "search_results": searchResults,
      "clicked_url": searchResults.url,
      "clicked_title": searchResults.title,
    });
  searchInput.addEventListener("keyup", function handleQuery(event) {
    this.removeEventListener("keyup", handleQuery);
    if (event.key === "Enter") {
      window.Kapa("open", { mode: "ai", query: query, submit: true });
    }
  });
});

// track event for kapa modal search result clicked from list
window.Kapa("onSearchResultClick", ({ query, searchResult, rank }) => {
  rudderanalytics.track("docs_click_search-result",
    {
      "search_query": query,
      "search_results": searchResult,
      "search_rank": rank,
      "clicked_url": searchResult.url,
      "clicked_title": searchResult.title,
    });
});

// track event for kapa modal search clicking "ask ai" in search results
window.Kapa("onAskAIQuerySubmit", ({ threadId, questionAnswerId, question }) => {
  rudderanalytics.track("docs_click_search-ask-ai",
    {
      "search_query": question,
    });
});

// track event for kapa modal search result clicking "ask ai" completing
window.Kapa("onAskAIAnswerCompleted", ({ threadId, questionAnswerId, question, answer, conversation }) => {
  rudderanalytics.track("docs_completed_search-ask-ai",
    {
      "search_query": question,
    });
});

// track event for kapa modal search result clicked from "ask ai" answer text
window.Kapa("onAskAILinkClick", ({ href, threadId, questionAnswerId, question, answer }) => {
  rudderanalytics.track("docs_click_search-ask-ai-result",
    {
      "search_query": question,
      "clicked_url": href,
    });
});

// track event for kapa modal search result clicked from "ask ai" answer sources
window.Kapa("onAskAISourceClick", ({ source, threadId, questionAnswerId, question, answer }) => {
  rudderanalytics.track("docs_click_search-ask-ai-source",
    {
      "search_query": question,
      "clicked_url": source.url,
      "clicked_title": source.title,
    });
});

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
  script.setAttribute("data-user-analytics-fingerprint-enabled", true);
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
