(function () {
  var LIGHT_LOGO_URL =
    "https://raw.githubusercontent.com/AssemblyAI/assemblyai-api-spec/main/fern/assets/logo-light.svg";
  var DARK_LOGO_URL =
    "https://raw.githubusercontent.com/AssemblyAI/assemblyai-api-spec/main/fern/assets/AssemblyAI_White.svg";

  function fixBrokenLogos() {
    var imgs = document.querySelectorAll("header a img");
    for (var i = 0; i < imgs.length; i++) {
      var img = imgs[i];
      if (img.naturalWidth === 0 && img.complete) {
        var src = img.getAttribute("src") || "";
        if (src.indexOf("logo-light") !== -1) {
          img.src = LIGHT_LOGO_URL;
        } else if (
          src.indexOf("AssemblyAI_White") !== -1 ||
          src.indexOf("logo-dark") !== -1
        ) {
          img.src = DARK_LOGO_URL;
        }
      }
    }
  }

  function tryFix() {
    fixBrokenLogos();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      setTimeout(tryFix, 500);
    });
  } else {
    setTimeout(tryFix, 500);
  }

  window.addEventListener("load", tryFix);
  setInterval(tryFix, 3000);
})();
