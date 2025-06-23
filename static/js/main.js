// static/js/main.js
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("job-filter-form");
  const sourceSelect = document.getElementById("source-select");

  if (form && sourceSelect) {
    sourceSelect.addEventListener("change", () => {
      const params = new URLSearchParams(new FormData(form));

      // Replace the current URL query string
      const baseUrl = new URL(window.location.href);
      window.location.href = `${baseUrl.pathname}?${params.toString()}`;
    });
  }
});
