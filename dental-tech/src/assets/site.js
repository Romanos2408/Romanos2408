(function () {
  var doc = document.documentElement;
  if (!doc.lang) doc.lang = "el";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Header line once the page scrolls
  var header = document.querySelector(".site-header");
  function onScroll() { if (header) header.classList.toggle("scrolled", window.scrollY > 8); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Hide the phone call bar while another call button is on screen
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

  // Gentle parallax
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

  // Reveal sections below the first screen as they scroll in
  if (!reduceMotion && "IntersectionObserver" in window) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.remove("pending"); ro.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll(".reveal").forEach(function (el, i) {
      if (el.getBoundingClientRect().top > window.innerHeight) {
        el.classList.add("pending");
        el.style.transitionDelay = (i % 3) * 90 + "ms";
        ro.observe(el);
      }
    });
  }

  var year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
})();
