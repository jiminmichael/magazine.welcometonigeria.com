(function () {
  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".global-search").forEach((form) =>
      form.addEventListener("submit", (event) => {
        event.preventDefault();
        const term = form.querySelector('input[type="search"]')?.value.trim();
        if (term) location.href = `stories.html?q=${encodeURIComponent(term)}`;
      }),
    );
  });
})();
