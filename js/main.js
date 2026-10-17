(function () {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const nav = [
    ["Home", "index.html"],
    ["Explore Stories", "stories.html"],
    ["Share Your Story", "share-story.html"],
    ["States", "states.html"],
    ["Travel Tips", "travel-tips.html"],
    ["About", "about.html"],
    ["Contact", "contact.html"],
  ];
  const header = `<div class="topline"><div class="wrap"><span>Real stories. Real people. Real Nigeria.</span><a href="https://welcometonigeria.com/" target="_blank" rel="noopener">Visit Welcome to Nigeria Travels &amp; Tourism ↗</a></div></div><header class="site-header"><div class="wrap header-main"><a class="brand" href="index.html" aria-label="Welcome to Nigeria Travel Magazine home"><span class="brand-mark" aria-hidden="true">W</span><span class="brand-copy"><span class="brand-name">Welcome to Nigeria</span><span class="brand-tag">Travel Magazine</span></span></a><nav class="main-nav" id="main-navigation" aria-label="Main navigation">${nav.map(([label, url]) => `<a href="${url}">${label}</a>`).join("")}<form class="global-search mobile-search" role="search"><input type="search" aria-label="Search stories, states and travellers" placeholder="Search Nigeria"><button aria-label="Search">⌕</button></form></nav><div class="header-actions" id="header-account"><form class="global-search" role="search"><input type="search" aria-label="Search stories, states and travellers" placeholder="Search Nigeria"><button aria-label="Search">⌕</button></form><a class="signin-link" href="signin.html">Sign in</a><a class="button small" href="signup.html">Sign up</a></div><button class="menu-toggle" aria-label="Open navigation" aria-expanded="false" aria-controls="main-navigation">☰</button></div></header>`;
  const footer = `<footer class="site-footer"><div class="wrap"><div class="footer-grid"><div class="footer-brand"><a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">W</span><span class="brand-copy"><span class="brand-name">Welcome to Nigeria</span><span class="brand-tag">Travel Magazine</span></span></a><p>Real stories from people travelling across Nigeria. Every journey adds a new point of view.</p><a href="https://welcometonigeria.com/" target="_blank" rel="noopener" class="text-link">Visit Welcome to Nigeria Travels &amp; Tourism ↗</a></div><div class="footer-col"><h3>Discover</h3><a href="index.html">Home</a><a href="stories.html">Explore stories</a><a href="share-story.html">Share your story</a><a href="states.html">States</a><a href="travel-tips.html">Travel tips</a></div><div class="footer-col"><h3>Magazine</h3><a href="about.html">About</a><a href="contact.html">Contact</a><a href="privacy-policy.html">Privacy policy</a><a href="terms.html">Terms &amp; conditions</a></div><div class="footer-col"><h3>Follow along</h3><div class="social-links"><a href="https://instagram.com/" aria-label="Instagram">Instagram</a><a href="https://facebook.com/" aria-label="Facebook">Facebook</a><a href="https://x.com/" aria-label="X">X</a><a href="https://youtube.com/" aria-label="YouTube">YouTube</a><a href="https://tiktok.com/" aria-label="TikTok">TikTok</a></div></div></div><div class="footer-bottom"><span>© 2026 Welcome to Nigeria Travel Magazine. All Rights Reserved.</span><span>Made for the stories that make a place.</span></div></div></footer>`;

  document.addEventListener("DOMContentLoaded", () => {
    const mount = document.querySelector("[data-site-header]");
    if (mount) mount.innerHTML = header;
    const footerMount = document.querySelector("[data-site-footer]");
    if (footerMount)
      footerMount.innerHTML = `<section class="newsletter"><div class="wrap newsletter-inner"><div><p class="eyebrow">A letter from the road</p><h2>Stay Connected With Nigeria</h2><p>Get new travel stories and experiences from across Nigeria delivered to you.</p></div><div><form class="newsletter-form"><input type="email" aria-label="Email for newsletter" placeholder="Your email address" required><button class="button" type="submit">Subscribe</button></form><p class="form-message" aria-live="polite"></p></div></div></section>${footer}`;
    const menu = document.querySelector(".menu-toggle");
    const navEl = document.querySelector(".main-nav");
    menu?.addEventListener("click", () => {
      const open = menu.getAttribute("aria-expanded") !== "true";
      menu.setAttribute("aria-expanded", String(open));
      menu.setAttribute(
        "aria-label",
        open ? "Close navigation" : "Open navigation",
      );
      menu.textContent = open ? "×" : "☰";
      navEl?.classList.toggle("open", open);
    });

    const current = location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll(".main-nav a").forEach((link) => {
      if (link.getAttribute("href") === current)
        link.setAttribute("aria-current", "page");
    });

    function applyUserNav(user) {
      const actions = document.getElementById("header-account");
      if (actions) {
        if (user) {
          actions.innerHTML = `<form class="global-search" role="search"><input type="search" aria-label="Search stories, states and travellers" placeholder="Search Nigeria"><button aria-label="Search">⌕</button></form><a class="account-nav" href="account.html">${escapeHtml(user.name.split(" ")[0])} · Account</a>`;
        } else {
          actions.innerHTML = `<form class="global-search" role="search"><input type="search" aria-label="Search stories, states and travellers" placeholder="Search Nigeria"><button aria-label="Search">⌕</button></form><a class="signin-link" href="signin.html">Sign in</a><a class="button small" href="signup.html">Sign up</a>`;
        }
      }
      const existingMobile = document.querySelector(".mobile-account");
      if (existingMobile) existingMobile.remove();
      const mobileAccount = document.createElement("a");
      mobileAccount.className = "mobile-account";
      mobileAccount.href = user ? "account.html" : "signin.html";
      mobileAccount.textContent = user ? "My account" : "Sign in / Sign up";
      navEl?.insertBefore(mobileAccount, navEl.querySelector(".mobile-search"));
    }

    // Try reading cached user first for immediate render
    let cachedUser = read("wtnUser", null);
    applyUserNav(cachedUser);

    // Verify session with Django backend
    fetch("/api/auth/me/")
      .then((res) => res.json())
      .then((data) => {
        if (data.authenticated && data.user) {
          localStorage.setItem("wtnUser", JSON.stringify(data.user));
          applyUserNav(data.user);
        } else {
          localStorage.removeItem("wtnUser");
          applyUserNav(null);
        }
      })
      .catch(() => {});

    // Backend-backed Newsletter Subscription
    document.querySelectorAll(".newsletter-form").forEach((form) =>
      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const input = form.querySelector("input[type=email]");
        const email = input.value.trim();
        const out = form.parentElement.querySelector(".form-message");
        if (!email) return;

        try {
          const res = await fetch("/api/interactions/newsletter/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken") || "",
            },
            body: JSON.stringify({ email }),
          });
          const data = await res.json();
          if (out) {
            out.textContent = data.message || "Thank you for subscribing!";
            out.classList.add("visible");
          }
          form.reset();
        } catch {
          if (out) {
            out.textContent = "Thank you for subscribing!";
            out.classList.add("visible");
          }
          form.reset();
        }
      }),
    );

    // Backend-backed Contact Form
    document.querySelectorAll("form[data-demo-contact]").forEach((form) =>
      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const output = form.querySelector(".form-success");
        const submitBtn = form.querySelector("button[type=submit]");
        if (submitBtn) submitBtn.disabled = true;

        const payload = {
          name: form.elements.name ? form.elements.name.value.trim() : "",
          email: form.elements.email ? form.elements.email.value.trim() : "",
          subject: form.elements.subject ? form.elements.subject.value.trim() : "",
          message: form.elements.message ? form.elements.message.value.trim() : "",
        };

        try {
          const res = await fetch("/api/interactions/contact/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken") || "",
            },
            body: JSON.stringify(payload),
          });
          const data = await res.json();
          if (res.ok) {
            if (output) {
              output.textContent = data.message || "Thank you for reaching out. We will get back to you shortly.";
              output.classList.add("visible");
            }
            form.reset();
          } else {
            if (output) {
              const errs = data.errors ? Object.values(data.errors).flat().join(" ") : data.error || "Unable to send message.";
              output.textContent = errs;
              output.classList.add("visible");
            }
          }
        } catch (e) {
          if (output) {
            output.textContent = "Unable to connect to the server. Please try again.";
            output.classList.add("visible");
          }
        } finally {
          if (submitBtn) submitBtn.disabled = false;
        }
      }),
    );
  });

  function read(key, fallback) {
    try {
      return JSON.parse(localStorage.getItem(key)) || fallback;
    } catch {
      return fallback;
    }
  }

  function escapeHtml(value) {
    return String(value ?? "").replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );
  }

  window.WTN = {
    getCookie,
    escapeHtml,
    read,
  };
})();
