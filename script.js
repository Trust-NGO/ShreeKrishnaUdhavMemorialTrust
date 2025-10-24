// Mobile Navbar Toggle
const navToggle = document.querySelector(".nav-toggle");
const navMenu = document.querySelector(".nav-menu");

navToggle.addEventListener("click", () => {
  navMenu.classList.toggle("active");
});

// Tabs in About Section
const tabButtons = document.querySelectorAll(".tab-button");
const tabContents = document.querySelectorAll(".tab-content");

tabButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    tabButtons.forEach((b) => b.classList.remove("active"));
    tabContents.forEach((c) => (c.hidden = true));
    btn.classList.add("active");
    const tabId = btn.getAttribute("aria-controls");
    document.getElementById(tabId).hidden = false;
  });
});

// Volunteer Form Handler
const form = document.getElementById("volunteer-form");
if (form) {
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    document.getElementById("form-msg").textContent =
      "धन्यवाद! आपका विवरण सफलतापूर्वक प्राप्त हुआ है। / Thank you for joining!";
    form.reset();
  });
}
