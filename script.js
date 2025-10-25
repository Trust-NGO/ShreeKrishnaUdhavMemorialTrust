// script.js – Shri Krishna Udhav Memorial Trust Website

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
  const observerFade = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      }
    });
  }, { threshold: 0.2 });
  fadeEls.forEach(el => observerFade.observe(el));

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
  const backToTop = document.getElementById('backToTop');
  window.addEventListener("scroll", () => {
    if (backToTop) {
      backToTop.style.display = window.scrollY > 300 ? 'block' : 'none';
    }
  });
  if(backToTop){
    backToTop.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* -------------------------------
     Dynamic Year in Footer
  --------------------------------*/
  const yearSpan = document.querySelector(".current-year");
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }

  /* -------------------------------
     Gallery Lightbox
  --------------------------------*/
  const galleryImages = document.querySelectorAll('.gallery-img');
  galleryImages.forEach(img => {
    img.addEventListener('click', () => {
      const lightbox = document.createElement('div');
      lightbox.id = 'lightbox';
      lightbox.style.position = 'fixed';
      lightbox.style.top = 0;
      lightbox.style.left = 0;
      lightbox.style.width = '100vw';
      lightbox.style.height = '100vh';
      lightbox.style.background = 'rgba(0,0,0,0.8)';
      lightbox.style.display = 'flex';
      lightbox.style.justifyContent = 'center';
      lightbox.style.alignItems = 'center';
      lightbox.style.zIndex = 9999;

      const imgClone = img.cloneNode();
      imgClone.style.maxWidth = '90%';
      imgClone.style.maxHeight = '90%';
      lightbox.appendChild(imgClone);
      document.body.appendChild(lightbox);

      lightbox.addEventListener('click', () => document.body.removeChild(lightbox));
    });
  });

  /* -------------------------------
     Counters Animation (IntersectionObserver)
  --------------------------------*/
  const counters = document.querySelectorAll(".counter");
  const speed = 200;

  const counterObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if(entry.isIntersecting){
        const counter = entry.target;
        const updateCount = () => {
          const target = +counter.getAttribute("data-target");
          const count = +counter.innerText;
          const increment = Math.ceil(target / speed);

          if(count < target){
            counter.innerText = count + increment;
            setTimeout(updateCount, 20);
          } else {
            counter.innerText = target;
          }
        };
        updateCount();
        counterObserver.unobserve(counter);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(counter => counterObserver.observe(counter));
});

// UPI QR Code Modal
const upiBtn = document.getElementById('upiBtn');
const upiModal = document.getElementById('upiModal');
const closeUpi = document.getElementById('closeUpi');

if(upiBtn && upiModal && closeUpi){
  upiBtn.addEventListener('click', () => upiModal.style.display = 'flex');
  closeUpi.addEventListener('click', () => upiModal.style.display = 'none');
  window.addEventListener('click', e => { if(e.target === upiModal) upiModal.style.display = 'none'; });
}

const sections = document.querySelectorAll("section");
const navLinks = document.querySelectorAll(".navbar-nav .nav-link");

window.addEventListener("scroll", () => {
  let current = "";
  sections.forEach(section => {
    const sectionTop = section.offsetTop - 80;
    const sectionHeight = section.clientHeight;
    if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
      current = section.getAttribute("id");
    }
  });

  navLinks.forEach(link => {
    link.classList.remove("active");
    if (link.getAttribute("href").includes(current)) {
      link.classList.add("active");
    }
  });
});


$(document).ready(function() {
  $('#noticeModal').modal('show');
});




document.addEventListener("DOMContentLoaded", () => {
  const track = document.querySelector(".gallery-track");
  const slides = document.querySelectorAll(".gallery-slide");
  const slideWidth = slides[0].offsetWidth;
  let index = 0;

  const moveSlide = () => {
    index++;
    if (index > slides.length - 4) { // 4 images per view
      index = 0; // loop back
    }
    track.style.transform = `translateX(-${slideWidth * index}px)`;
  };

  setInterval(moveSlide, 3000); // slide every 3 seconds

  // Adjust slideWidth on window resize
  window.addEventListener("resize", () => {
    const newSlideWidth = slides[0].offsetWidth;
    track.style.transform = `translateX(-${newSlideWidth * index}px)`;
  });
});
