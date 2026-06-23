document.addEventListener("DOMContentLoaded", () => {
  const button = document.querySelector("[data-menu]");
  const sidebar = document.querySelector(".sidebar");
  if (button && sidebar) button.addEventListener("click", () => sidebar.classList.toggle("open"));
  document.querySelectorAll(".message").forEach((item) => setTimeout(() => item.classList.add("fade"), 4500));
  document.querySelectorAll("[data-password-toggle]").forEach((toggle) => {
    toggle.addEventListener("click", () => {
      const input = toggle.closest("div")?.querySelector("input");
      if (!input) return;
      const visible = input.type === "text";
      input.type = visible ? "password" : "text";
      const icon = toggle.querySelector(".material-symbols-outlined");
      if (icon) icon.textContent = visible ? "visibility" : "visibility_off";
      toggle.setAttribute("aria-label", visible ? "Afficher le mot de passe" : "Masquer le mot de passe");
    });
  });
});
