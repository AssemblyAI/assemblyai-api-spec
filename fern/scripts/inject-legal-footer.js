(function () {
  function injectLegalFooter() {
    const footer = document.querySelector("footer");
    if (!footer || footer.querySelector(".legal-footer-links")) return true;

    if (!document.getElementById("legal-footer-styles")) {
      const style = document.createElement("style");
      style.id = "legal-footer-styles";
      style.textContent = `
        .legal-footer-links {
          margin-top: 2rem;
          padding-top: 1rem;
          border-top: 1px solid rgba(0, 0, 0, 0.1);
          text-align: center;
        }
        :is(.dark) .legal-footer-links {
          border-top-color: rgba(255, 255, 255, 0.1);
        }
        .legal-footer-links .footer-main_col-title {
          font-size: 0.875rem;
          font-weight: 500;
          opacity: 0.7;
          margin-bottom: 0.75rem;
          text-align: center;
        }
        .legal-footer-links .footer-main_links-wrapper {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem 1.5rem;
          justify-content: center;
        }
        .legal-footer-links .footer-main_link {
          font-size: 0.8125rem;
          opacity: 0.6;
          transition: opacity 0.2s ease;
          text-decoration: none;
          color: inherit;
        }
        .legal-footer-links .footer-main_link:hover {
          opacity: 0.9;
        }
        .legal-footer-links .footer-main_link div {
          margin: 0;
          padding: 0;
        }
        @media (max-width: 768px) {
          .legal-footer-links .footer-main_links-wrapper {
            flex-direction: column;
            gap: 0.5rem;
            align-items: center;
          }
          .legal-footer-links {
            margin-top: 1.5rem;
            padding-top: 1.5rem;
          }
        }
      `;
      document.head.appendChild(style);
    }

    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = `
      <div class="footer-main_col legal-footer-links">
        <div class="footer-main_col-title">Legal</div>
        <div class="footer-main_links-wrapper">
          <a href="https://www.assemblyai.com/legal/terms-of-service" class="footer-main_link w-inline-block">
            <div>Terms of Service</div>
          </a>
          <a href="https://www.assemblyai.com/legal/privacy-policy" class="footer-main_link w-inline-block">
            <div>Privacy Policy</div>
          </a>
          <a href="https://app.vanta.com/assemblyai/trust/7n80syl8zln1bn1qm3x8eg" class="footer-main_link w-inline-block">
            <div>Trust Center</div>
          </a>
          <a href="https://app.vanta.com/assemblyai/trust/7n80syl8zln1bn1qm3x8eg/subprocessors" class="footer-main_link w-inline-block">
            <div>Subprocessors</div>
          </a>
        </div>
      </div>
    `;

    footer.appendChild(tempDiv.firstElementChild);
    return true;
  }

  function tryInject() {
    if (!injectLegalFooter()) {
      setTimeout(tryInject, 3000);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", tryInject);
  } else {
    tryInject();
  }

  setInterval(tryInject, 5000);

  window.addEventListener("popstate", () => setTimeout(tryInject, 300));

  const originalPushState = history.pushState;
  const originalReplaceState = history.replaceState;

  history.pushState = function (...args) {
    originalPushState.apply(history, args);
    setTimeout(tryInject, 300);
  };

  history.replaceState = function (...args) {
    originalReplaceState.apply(history, args);
    setTimeout(tryInject, 300);
  };

  if (typeof MutationObserver !== "undefined") {
    const observer = new MutationObserver(function (mutations) {
      const footerChanged = mutations.some(
        (m) =>
          m.type === "childList" &&
          [...m.addedNodes, ...m.removedNodes].some(
            (n) =>
              n.nodeType === Node.ELEMENT_NODE &&
              (n.tagName === "FOOTER" ||
                (n.querySelector && n.querySelector("footer")))
          )
      );

      if (footerChanged) setTimeout(tryInject, 300);
    });

    observer.observe(document.body, { childList: true, subtree: true });
  }
})();
