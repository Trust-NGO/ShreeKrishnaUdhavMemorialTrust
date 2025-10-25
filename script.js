// main.js – Shri Krishna Udhav Memorial Trust Website

document.addEventListener("DOMContentLoaded", () => {

  /* -------------------------------
     Smooth Scroll for Navigation
  --------------------------------*/
  const navLinks = document.querySelectorAll('a[href^="#"]');
  navLinks.forEach(link => {
    link.addEventListener("click", e => {
      const target = document.querySelector(link.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  /* -------------------------------
     Sticky Navbar on Scroll
  --------------------------------*/
  const header = document.querySelector("header");
  if (header) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 80) {
        header.classList.add("scrolled");
      } else {
        header.classList.remove("scrolled");
      }
    });
  }

  /* -------------------------------
     Animate on Scroll (Simple Fade-in)
  --------------------------------*/
  const fadeEls = document.querySelectorAll(".fade-in");
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      }
    });
  }, { threshold: 0.2 });
  fadeEls.forEach(el => observer.observe(el));

  /* -------------------------------
     Mobile Menu Toggle
  --------------------------------*/
  const menuBtn = document.querySelector(".menu-toggle");
  const navMenu = document.querySelector(".nav-menu");
  if (menuBtn && navMenu) {
    menuBtn.addEventListener("click", () => {
      navMenu.classList.toggle("active");
      menuBtn.classList.toggle("open");
    });
  }

  /* -------------------------------
     Contact / Donation Form Validation
  --------------------------------*/
  const form = document.querySelector("form.needs-validation");
  if (form) {
    form.addEventListener("submit", e => {
      e.preventDefault();
      let valid = true;

      form.querySelectorAll("input, textarea, select").forEach(input => {
        if (input.hasAttribute("required") && !input.value.trim()) {
          input.classList.add("is-invalid");
          valid = false;
        } else {
          input.classList.remove("is-invalid");
        }
      });

      if (valid) {
        alert("✅ Thank you for contacting Shri Krishna Udhav Memorial Trust. We will get back to you soon!");
        form.reset();
      } else {
        alert("⚠️ Please fill all required fields before submitting.");
      }
    });
  }

  /* -------------------------------
     Back to Top Button
  --------------------------------*/
  const backToTop = document.createElement("button");
  backToTop.innerText = "↑";
  backToTop.className = "back-to-top";
  document.body.appendChild(backToTop);

  window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
      backToTop.classList.add("show");
    } else {
      backToTop.classList.remove("show");
    }
  });

  backToTop.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  /* -------------------------------
     Dynamic Year in Footer
  --------------------------------*/
  const yearSpan = document.querySelector(".current-year");
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }

});
