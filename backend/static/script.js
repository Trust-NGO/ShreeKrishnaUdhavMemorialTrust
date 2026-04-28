// script.js – Shri Krishna Udhav Memorial Trust Website

document.addEventListener("DOMContentLoaded", () => {

  /* ============================================================
     NAVBAR SCROLL EFFECTS
     ============================================================ */
  const siteHeader = document.getElementById("siteHeader");
  const SCROLL_THRESHOLD = 60;

  function updateNavbarOnScroll() {
    if (!siteHeader) return;
    if (window.scrollY > SCROLL_THRESHOLD) {
      siteHeader.classList.add("site-header--scrolled");
    } else {
      siteHeader.classList.remove("site-header--scrolled");
    }
  }

  window.addEventListener("scroll", updateNavbarOnScroll, { passive: true });
  updateNavbarOnScroll(); // Initial check on load

  /* ============================================================
     MOBILE MENU
     ============================================================ */
  const mobileToggle = document.getElementById("mobileToggle");
  const mobileClose = document.getElementById("mobileClose");
  const mobileNav = document.getElementById("mobileNav");
  const mobileBackdrops = document.querySelectorAll(".mobile-nav-backdrop");

  function openMobileMenu() {
    if (!mobileNav || !mobileToggle) return;
    mobileNav.classList.add("is-open");
    mobileNav.setAttribute("aria-hidden", "false");
    mobileToggle.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden"; // Prevent background scroll
    // Focus first link for accessibility
    const firstLink = mobileNav.querySelector(".mobile-link");
    if (firstLink) firstLink.focus();
  }

  function closeMobileMenu() {
    if (!mobileNav || !mobileToggle) return;
    mobileNav.classList.remove("is-open");
    mobileNav.setAttribute("aria-hidden", "true");
    mobileToggle.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
    mobileToggle.focus(); // Return focus to toggle button
  }

  if (mobileToggle) {
    mobileToggle.addEventListener("click", () => {
      if (mobileNav.classList.contains("is-open")) {
        closeMobileMenu();
      } else {
        openMobileMenu();
      }
    });
  }

  if (mobileClose) {
    mobileClose.addEventListener("click", closeMobileMenu);
  }

  // Close on backdrop click
  mobileBackdrops.forEach(backdrop => {
    backdrop.addEventListener("click", closeMobileMenu);
  });

  // Close on Escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && mobileNav && mobileNav.classList.contains("is-open")) {
      closeMobileMenu();
    }
  });

  /* ============================================================
     MOBILE ACCORDION SUBMENUS
     ============================================================ */
  const accordionToggles = document.querySelectorAll(".mobile-link--accordion");

  accordionToggles.forEach(toggle => {
    toggle.addEventListener("click", () => {
      const isExpanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!isExpanded));
    });
  });

  /* ============================================================
     DESKTOP DROPDOWN KEYBOARD ACCESSIBILITY
     ============================================================ */
  const dropdownParents = document.querySelectorAll(".nav-item--has-dropdown");

  dropdownParents.forEach(parent => {
    const toggle = parent.querySelector(".nav-link--toggle");
    const dropdown = parent.querySelector(".nav-dropdown");

    if (toggle && dropdown) {
      // Open dropdown on Enter, Space, or ArrowDown
      toggle.addEventListener("keydown", (e) => {
        const isOpen = toggle.getAttribute("aria-expanded") === "true";
        const links = Array.from(dropdown.querySelectorAll(".dropdown-link"));

        if (e.key === "Enter" || e.key === " " || e.key === "ArrowDown") {
          e.preventDefault();
          if (!isOpen) {
            toggle.setAttribute("aria-expanded", "true");
          }
          // Move focus to first link if ArrowDown
          if (e.key === "ArrowDown" && links.length > 0) {
            links[0].focus();
          }
        } else if (e.key === "Escape" && isOpen) {
          toggle.setAttribute("aria-expanded", "false");
          toggle.focus();
        }
      });

      // Handle keyboard navigation within dropdown
      dropdown.addEventListener("keydown", (e) => {
        const links = Array.from(dropdown.querySelectorAll(".dropdown-link"));
        const currentIndex = links.indexOf(document.activeElement);

        if (e.key === "ArrowDown") {
          e.preventDefault();
          const nextIndex = (currentIndex + 1) % links.length;
          links[nextIndex].focus();
        } else if (e.key === "ArrowUp") {
          e.preventDefault();
          if (currentIndex === 0) {
            // Move focus back to toggle
            toggle.setAttribute("aria-expanded", "false");
            toggle.focus();
          } else {
            const prevIndex = (currentIndex - 1 + links.length) % links.length;
            links[prevIndex].focus();
          }
        } else if (e.key === "Escape") {
          toggle.setAttribute("aria-expanded", "false");
          toggle.focus();
        }
      });

      // Collapse when focus leaves the dropdown area
      parent.addEventListener("focusout", (e) => {
        if (!parent.contains(e.relatedTarget)) {
          toggle.setAttribute("aria-expanded", "false");
        }
      });
    }
  });

  /* ============================================================
     ACTIVE SECTION HIGHLIGHT ON SCROLL (for anchor links)
     ============================================================ */
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".nav-link[href^='#'], .nav-link[href='/']");

  function highlightActiveSection() {
    let current = "";
    const scrollPos = window.scrollY + 120;

    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.clientHeight;
      if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
        current = section.getAttribute("id");
      }
    });

    navLinks.forEach(link => {
      link.classList.remove("nav-link--active");
      const href = link.getAttribute("href");
      if (href === `/#${current}` || href === `/#` && current === "") {
        link.classList.add("nav-link--active");
      }
    });
  }

  if (sections.length > 0) {
    window.addEventListener("scroll", highlightActiveSection, { passive: true });
  }

  /* ============================================================
     SMOOTH SCROLL FOR NAVIGATION LINKS
     ============================================================ */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href");
      if (targetId === "#") return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
        // Close mobile menu if open
        if (mobileNav && mobileNav.classList.contains("is-open")) {
          closeMobileMenu();
        }
      }
    });
  });

  /* ============================================================
     ANIMATE ON SCROLL (Fade-in)
     ============================================================ */
  const fadeElements = document.querySelectorAll(".fade-in");
  const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      }
    });
  }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });

  fadeElements.forEach(el => fadeObserver.observe(el));

  /* ============================================================
     FORM VALIDATION
     ============================================================ */
  const forms = document.querySelectorAll("form.needs-validation");
  forms.forEach(form => {
    form.addEventListener("submit", (e) => {
      let valid = true;
      form.querySelectorAll("input, textarea, select").forEach(input => {
        if (input.hasAttribute("required")) {
          if (input.type === "checkbox") {
            if (!input.checked) {
              input.classList.add("is-invalid");
              valid = false;
            } else {
              input.classList.remove("is-invalid");
            }
          } else if (!input.value.trim()) {
            input.classList.add("is-invalid");
            valid = false;
          } else {
            input.classList.remove("is-invalid");
          }
        }
      });
      if (!valid) {
        e.preventDefault();
        alert("Please fill all required fields and agree to the terms before submitting.");
      }
    });
  });

  /* ============================================================
     BACK TO TOP BUTTON
     ============================================================ */
  const backToTop = document.getElementById("backToTop");
  if (backToTop) {
    window.addEventListener("scroll", () => {
      backToTop.style.display = window.scrollY > 400 ? "block" : "none";
      backToTop.classList.toggle("show", window.scrollY > 400);
    }, { passive: true });

    backToTop.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ============================================================
     DYNAMIC YEAR IN FOOTER
     ============================================================ */
  const yearSpans = document.querySelectorAll(".current-year, #footerYear");
  yearSpans.forEach(span => {
    span.textContent = new Date().getFullYear();
  });

  /* ============================================================
     GALLERY LIGHTBOX
     ============================================================ */
  document.querySelectorAll(".gallery-img").forEach(img => {
    img.style.cursor = "pointer";
    img.addEventListener("click", () => {
      const lightbox = document.createElement("div");
      lightbox.id = "lightbox";
      Object.assign(lightbox.style, {
        position: "fixed",
        top: "0",
        left: "0",
        width: "100vw",
        height: "100vh",
        background: "rgba(0,0,0,0.85)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: "9999",
        cursor: "zoom-out"
      });
      const imgClone = document.createElement("img");
      imgClone.src = img.src;
      Object.assign(imgClone.style, {
        maxWidth: "90%",
        maxHeight: "90%",
        borderRadius: "12px",
        boxShadow: "0 20px 60px rgba(0,0,0,0.5)"
      });
      lightbox.appendChild(imgClone);
      document.body.appendChild(lightbox);

      const closeLightbox = () => {
        if (lightbox.parentNode) lightbox.parentNode.removeChild(lightbox);
      };
      lightbox.addEventListener("click", closeLightbox);
      document.addEventListener("keydown", function escHandler(e) {
        if (e.key === "Escape") {
          closeLightbox();
          document.removeEventListener("keydown", escHandler);
        }
      });
    });
  });

  /* ============================================================
     COUNTER ANIMATION
     ============================================================ */
  const counters = document.querySelectorAll(".counter");
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const counter = entry.target;
        const target = parseInt(counter.getAttribute("data-target"), 10);
        const duration = 2000;
        const startTime = performance.now();

        function updateCounter(currentTime) {
          const elapsed = currentTime - startTime;
          const progress = Math.min(elapsed / duration, 1);
          // Ease out cubic
          const ease = 1 - Math.pow(1 - progress, 3);
          counter.textContent = Math.floor(ease * target);

          if (progress < 1) {
            requestAnimationFrame(updateCounter);
          }
        }

        requestAnimationFrame(updateCounter);
        counterObserver.unobserve(counter);
      }
    });
  }, { threshold: 0.4 });

  counters.forEach(counter => counterObserver.observe(counter));

  /* ============================================================
     GALLERY CAROUSEL AUTO-SCROLL
     ============================================================ */
  const galleryTrack = document.querySelector(".gallery-track");
  const gallerySlides = document.querySelectorAll(".gallery-slide");

  if (galleryTrack && gallerySlides.length > 0) {
    let slideWidth = gallerySlides[0].offsetWidth;
    let currentIndex = 0;

    function moveSlide() {
      currentIndex++;
      if (currentIndex > gallerySlides.length - 4) {
        currentIndex = 0;
      }
      galleryTrack.style.transform = `translateX(-${slideWidth * currentIndex}px)`;
    }

    let autoSlide = setInterval(moveSlide, 3000);

    window.addEventListener("resize", () => {
      slideWidth = gallerySlides[0].offsetWidth;
      galleryTrack.style.transform = `translateX(-${slideWidth * currentIndex}px)`;
    });

    // Pause on hover
    const galleryContainer = document.querySelector(".gallery-container");
    if (galleryContainer) {
      galleryContainer.addEventListener("mouseenter", () => clearInterval(autoSlide));
      galleryContainer.addEventListener("mouseleave", () => {
        autoSlide = setInterval(moveSlide, 3000);
      });
    }
  }
});
