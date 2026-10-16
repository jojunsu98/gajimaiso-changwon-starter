(() => {
  "use strict";
  document.documentElement.classList.add("js");
  const menuButton = document.querySelector(".menu-toggle");
  const nav = document.querySelector("#main-nav");
  const progress = document.querySelector(".reading-progress span");
  const links = [...nav.querySelectorAll('a[href^="#"]')];
  menuButton.hidden = false;
  function closeMenu() {
    nav.classList.remove("is-open");
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.innerHTML = '목차 열기 <span aria-hidden="true">＋</span>';
  }
  menuButton.addEventListener("click", () => {
    const open = menuButton.getAttribute("aria-expanded") !== "true";
    nav.classList.toggle("is-open", open);
    menuButton.setAttribute("aria-expanded", String(open));
    menuButton.innerHTML = open ? '목차 닫기 <span aria-hidden="true">−</span>' : '목차 열기 <span aria-hidden="true">＋</span>';
  });
  links.forEach(link => link.addEventListener("click", closeMenu));
  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
      closeMenu();
      menuButton.focus();
    }
  });
  const sections = links.map(link => document.querySelector(link.getAttribute("href")));
  let pending = false;
  function updateReadingPosition() {
    const available = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.width = (available > 0 ? Math.min(100, Math.max(0, window.scrollY / available * 100)) : 0) + "%";
    let current = -1;
    sections.forEach((section, index) => { if (section.getBoundingClientRect().top <= 150) current = index; });
    links.forEach((link, index) => {
      if (index === current) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
    pending = false;
  }
  function scheduleUpdate() {
    if (!pending) { pending = true; window.requestAnimationFrame(updateReadingPosition); }
  }
  window.addEventListener("scroll", scheduleUpdate, { passive: true });
  window.addEventListener("resize", () => { if (window.innerWidth > 600) closeMenu(); scheduleUpdate(); });
  window.addEventListener("load", updateReadingPosition);
  updateReadingPosition();
})();
