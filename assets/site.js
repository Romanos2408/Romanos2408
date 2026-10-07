(function () {
  var doc = document.documentElement;
  if (!doc.lang) doc.lang = "el";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Dymo headline: letters appear one by one, like the label maker clicking.
  if (!reduceMotion) {
    document.querySelectorAll(".typing").forEach(function (el) {
      var text = el.textContent;
      var start = parseInt((el.style.getPropertyValue("--d") || "0").replace("ms", ""), 10) || 0;
      el.setAttribute("aria-label", text);
      el.textContent = "";
      Array.prototype.forEach.call(text, function (c, i) {
        var s = document.createElement("span");
        s.className = "ch";
        s.setAttribute("aria-hidden", "true");
        s.textContent = c;
        el.appendChild(s);
        setTimeout(function () { s.classList.add("on"); }, start + 250 + i * 70);
      });
    });
  }

  // Hide the phone call strip while another call button is on screen.
  var callbar = document.querySelector(".callbar");
  var spots = document.querySelectorAll("[data-hide-callbar]");
  if (callbar && spots.length && "IntersectionObserver" in window) {
    var seen = new Set();
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { e.isIntersecting ? seen.add(e.target) : seen.delete(e.target); });
      callbar.classList.toggle("hide", seen.size > 0);
    });
    spots.forEach(function (el) { io.observe(el); });
  }

  // Depth: things closer to you move a little faster than the counter.
  var layers = Array.prototype.slice.call(document.querySelectorAll("[data-speed]"));
  if (layers.length && !reduceMotion) {
    var ticking = false;
    var paint = function () {
      var vh = window.innerHeight;
      layers.forEach(function (el) {
        var box = el.parentElement.getBoundingClientRect();
        if (box.bottom < -200 || box.top > vh + 200) return;
        var y = (box.top + box.height / 2 - vh / 2) * (parseFloat(el.getAttribute("data-speed")) || 0);
        el.style.transform = "translate3d(0," + y.toFixed(1) + "px,0)";
      });
      ticking = false;
    };
    paint();
    window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(paint); } }, { passive: true });
    window.addEventListener("resize", paint);
  }

  // Objects below the first screen settle onto the bench as you reach them.
  if (!reduceMotion && "IntersectionObserver" in window) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.remove("pending"); ro.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -10% 0px" });
    document.querySelectorAll(".reveal").forEach(function (el) {
      if (el.getBoundingClientRect().top > window.innerHeight) { el.classList.add("pending"); ro.observe(el); }
    });
  }

  var year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
})();
