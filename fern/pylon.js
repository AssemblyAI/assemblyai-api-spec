(function () {
  var e = window;
  var t = document;
  var n = function () {
    n.e(arguments);
  };
  n.q = [];
  n.e = function (e) {
    n.q.push(e);
  };
  e.Pylon = n;
  var r = function () {
    var e = t.createElement("script");
    e.setAttribute("type", "text/javascript");
    e.setAttribute("async", "true");
    e.setAttribute(
      "src",
      "https://widget.usepylon.com/widget/f28d5a70-a10d-4a6c-bd5e-cff70ac09f60"
    );
    var n = t.getElementsByTagName("script")[0];
    n.parentNode.insertBefore(e, n);
  };
  if (t.readyState === "complete") {
    r();
  } else if (e.addEventListener) {
    e.addEventListener("load", r, false);
  }
})();

(function () {
  fetch("https://www.assemblyai.com/dashboard/api/pylon-credentials", {
    credentials: "include",
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok: " + response.statusText);
      }
      return response.json();
    })
    .then((data) => {
      if (data && data.email && data.emailHash) {
        window.pylon = {
          chat_settings: {
            app_id: "f28d5a70-a10d-4a6c-bd5e-cff70ac09f60",
            name: "User",
            email: data.email,
            email_hash: data.emailHash,
          },
        };
      }
    })
    .catch((error) => {
      console.error("Failed to initialize Pylon widget:", error);
    });
})();
