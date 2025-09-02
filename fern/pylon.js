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

// fetch pylon credentials (email, and email_hash) based on user's auth cookie and show chat bubble
(function () {
  executeRequest(BASE_URL + "/dashboard/api/pylon-credentials", {
    // will no longer be needed when we're on the same domain
    credentials: "include",
  })
    .then((res) => {
      if (res && res.email && res.emailHash) {
        window.pylon = {
          chat_settings: {
            app_id: "f28d5a70-a10d-4a6c-bd5e-cff70ac09f60",
            name: "User",
            email: res.email,
            email_hash: res.emailHash,
          },
        };
      }
    })
    .catch((error) => {});
})();
