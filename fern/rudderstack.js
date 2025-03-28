(function () {
  "use strict";
  window.RudderSnippetVersion = "3.0.32";
  var identifier = "rudderanalytics";
  if (!window[identifier]) {
    window[identifier] = [];
  }
  var rudderanalytics = window[identifier];
  if (Array.isArray(rudderanalytics)) {
    if (
      rudderanalytics.snippetExecuted === true &&
      window.console &&
      console.error
    ) {
      console.error(
        "RudderStack JavaScript SDK snippet included more than once.",
      );
    } else {
      rudderanalytics.snippetExecuted = true;
      window.rudderAnalyticsBuildType = "legacy";
      var sdkBaseUrl = "https://rs-cdn.assemblyai.com/v3";
      var sdkName = "rsa.min.js";
      var scriptLoadingMode = "async";
      var methods = [
        "setDefaultInstanceKey",
        "load",
        "ready",
        "page",
        "track",
        "identify",
        "alias",
        "group",
        "reset",
        "setAnonymousId",
        "startSession",
        "endSession",
        "consent",
      ];
      for (var i = 0; i < methods.length; i++) {
        var method = methods[i];
        rudderanalytics[method] = (function (methodName) {
          return function () {
            if (Array.isArray(window[identifier])) {
              rudderanalytics.push(
                [methodName].concat(Array.prototype.slice.call(arguments)),
              );
            } else {
              var _methodName;
              (_methodName = window[identifier][methodName]) === null ||
                _methodName === void 0 ||
                _methodName.apply(window[identifier], arguments);
            }
          };
        })(method);
      }
      try {
        new Function(
          'class Test{field=()=>{};test({prop=[]}={}){return prop?(prop?.property??[...prop]):import("");}}',
        );
        window.rudderAnalyticsBuildType = "modern";
      } catch (e) {}
      var head = document.head || document.getElementsByTagName("head")[0];
      var body = document.body || document.getElementsByTagName("body")[0];
      window.rudderAnalyticsAddScript = function (
        url,
        extraAttributeKey,
        extraAttributeVal,
      ) {
        var scriptTag = document.createElement("script");
        scriptTag.src = url;
        scriptTag.setAttribute("data-loader", "RS_JS_SDK");
        if (extraAttributeKey && extraAttributeVal) {
          scriptTag.setAttribute(extraAttributeKey, extraAttributeVal);
        }
        if (scriptLoadingMode === "async") {
          scriptTag.async = true;
        } else if (scriptLoadingMode === "defer") {
          scriptTag.defer = true;
        }
        if (head) {
          head.insertBefore(scriptTag, head.firstChild);
        } else {
          body.insertBefore(scriptTag, body.firstChild);
        }
      };
      window.rudderAnalyticsMount = function () {
        (function () {
          if (typeof globalThis === "undefined") {
            var getGlobal = function getGlobal() {
              if (typeof self !== "undefined") {
                return self;
              }
              if (typeof window !== "undefined") {
                return window;
              }
              return null;
            };
            var global = getGlobal();
            if (global) {
              Object.defineProperty(global, "globalThis", {
                value: global,
                configurable: true,
              });
            }
          }
        })();
        window.rudderAnalyticsAddScript(
          ""
            .concat(sdkBaseUrl, "/")
            .concat(window.rudderAnalyticsBuildType, "/")
            .concat(sdkName),
          "data-rsa-write-key",
          "2hNPzeocLrXEJ6fuVktdhExfmUr",
        );
      };
      if (typeof Promise === "undefined" || typeof globalThis === "undefined") {
        window.rudderAnalyticsAddScript(
          "https://polyfill-fastly.io/v3/polyfill.min.js?version=3.111.0&features=Symbol%2CPromise&callback=rudderAnalyticsMount",
        );
      } else {
        window.rudderAnalyticsMount();
      }
      var loadOptions = {
        pluginsSDKBaseURL: "https://rs-cdn.assemblyai.com/v3/modern/plugins",
      };
      rudderanalytics.load(
        "2hNPzeocLrXEJ6fuVktdhExfmUr",
        "https://rs-dp.assemblyai.com",
        loadOptions,
      );
    }
  }
})();

// Function to track page views
function trackPage() {
  const pageProperties = {
    url: window.location.href,
    path: window.location.pathname,
    search: window.location.search,
    title: document.title,
    referrer: document.referrer,
  };

  // Send page view event to RudderStack
  rudderanalytics.page({
    properties: pageProperties,
  });
}

// Track initial page load
trackPage();

// Setup history change listener for SPA navigation
let lastPathname = window.location.pathname;

// Function to check if pathname has changed
function hasPathnameChanged() {
  const currentPathname = window.location.pathname;
  const hasChanged = currentPathname !== lastPathname;
  lastPathname = currentPathname;
  return hasChanged;
}

// Setup listeners for different types of navigation
// 1. History API changes (pushState/replaceState)
const originalPushState = history.pushState;
const originalReplaceState = history.replaceState;

history.pushState = function () {
  originalPushState.apply(this, arguments);
  if (hasPathnameChanged()) {
    trackPage();
  }
};

history.replaceState = function () {
  originalReplaceState.apply(this, arguments);
  if (hasPathnameChanged()) {
    trackPage();
  }
};

// 2. Listen for popstate events (browser back/forward)
window.addEventListener("popstate", () => {
  if (hasPathnameChanged()) {
    trackPage();
  }
});

// 3. Listen for hashchange events
window.addEventListener("hashchange", () => {
  if (hasPathnameChanged()) {
    trackPage();
  }
});

// Function to track copy button clicks
function trackCopyClick(event) {
  const button = event.currentTarget;
  const codeBlock =
    button.closest("pre")?.querySelector("code")?.textContent || "unknown";

  rudderanalytics.track("docs_click_copy-code", {
    location: window.location.pathname,
  });
}

// Function to setup copy button tracking
function setupCopyButtonTracking() {
  // Remove existing listeners first
  document.querySelectorAll(".fern-copy-button").forEach((button) => {
    button.removeEventListener("click", trackCopyClick);
    button.addEventListener("click", trackCopyClick);
  });
}

// Function to track feedback button clicks and form submissions
function trackFeedback(event) {
  const button = event.currentTarget;
  const isPositive = button.textContent.includes("Yes");

  rudderanalytics.track("docs_click_feedback", {
    location: window.location.pathname,
    sentiment: isPositive ? "positive" : "negative",
  });
}

function trackFeedbackForm(event) {
  // Get the selected reason (radio button value)
  const selectedReason = event.target.querySelector(
    'input[type="radio"]:checked',
  )?.value;

  // Get email consent and value
  const emailConsent = event.target.querySelector(
    'input[type="checkbox"]',
  )?.checked;
  const emailInput = event.target.querySelector('input[type="email"]')?.value;

  const feedbackData = {
    location: window.location.pathname,
    reason: selectedReason || "not_selected",
    email_consent: !!emailConsent,
    email: emailConsent ? emailInput : undefined,
  };

  // Track the form submission without interfering with the form's normal behavior
  rudderanalytics.track("docs_fill_feedback-form", feedbackData);
}

// Function to setup feedback tracking
function setupFeedbackTracking() {
  // Setup button click listeners for thumbs up/down
  document
    .querySelectorAll('button[aria-haspopup="dialog"]')
    .forEach((button) => {
      // Only add to thumbs up/down buttons
      if (button.querySelector(".lucide-thumbs-up, .lucide-thumbs-down")) {
        button.removeEventListener("click", trackFeedback);
        button.addEventListener("click", trackFeedback);
      }
    });

  // Setup form submission listeners - no need for data-feedback-form attribute
  // since we can identify the form by its unique structure
  document.querySelectorAll("form:has(#feedback-reason)").forEach((form) => {
    form.removeEventListener("submit", trackFeedbackForm);
    form.addEventListener("submit", trackFeedbackForm);
  });
}

// Function to setup all tracking (combined setup function)
function setupTracking() {
  setupCopyButtonTracking();
  setupFeedbackTracking();
}

// Setup initial listeners and watch for changes
document.addEventListener("DOMContentLoaded", setupTracking);

if (typeof window !== "undefined") {
  // Handle navigation events
  window.addEventListener("popstate", setupTracking);
  document.addEventListener("next-navigation", setupTracking);
  document.addEventListener("routeChangeComplete", setupTracking);

  // Watch for DOM changes
  const observer = new MutationObserver(setupTracking);
  observer.observe(document.body, { childList: true, subtree: true });
}
