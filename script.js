/* Typing effect */
const phrases = [
  "Empowering Communities, Inspiring Change",
  "Education • Health • Skills • Dignity",
  "In memory of Udho Yadav — serving Deoria"
];
let curPhrase = 0, char = 0, deleting = false;
const typedEl = document.getElementById('typed');

function typeTick() {
  const p = phrases[curPhrase];
  if (!deleting) {
    typedEl.textContent = p.slice(0, ++char);
    if (char === p.length) {
      deleting = true;
      setTimeout(typeTick, 1500);
      return;
    }
  } else {
    typedEl.textContent = p.slice(0, --char);
    if (char === 0) {
      deleting = false;
      curPhrase = (curPhrase + 1) % phrases.length;
    }
  }
  setTimeout(typeTick, deleting ? 50 : 90);
}
typeTick();

/* Back-to-top button */
const backToTop = document.getElementById("backToTop");
window.addEventListener("scroll", () => {
  if (window.scrollY > 300) backToTop.style.display = "block";
  else backToTop.style.display = "none";
});
backToTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

/* Animated counters */
const counters = document.querySelectorAll(".counter");
const speed = 150;
const animateCounters = () => {
  counters.forEach(counter => {
    const target = +counter.getAttribute("data-target");
    const updateCount = () => {
      const count = +counter.innerText;
      const inc = target / speed;
      if (count < target) {
        counter.innerText = Math.ceil(count + inc);
        setTimeout(updateCount, 20);
      } else {
        counter.innerText = target;
      }
    };
    updateCount();
  });
};
const statsSection = document.getElementById("stats");
let statsTriggered = false;
window.addEventListener("scroll", () => {
  const top = statsSection.getBoundingClientRect().top;
  if (top < window.innerHeight && !statsTriggered) {
    animateCounters();
    statsTriggered = true;
  }
});

/* Gallery Lightbox */
$('.gallery-img').on('click', function() {
  $('#lightboxImage').attr('src', $(this).data('large'));
  $('#lightboxModal').modal('show');
});

/* Razorpay Integration */
$('#payBtn').on('click', function() {
  const options = {
    key: "rzp_test_yourapikeyhere", // replace with your Razorpay key
    amount: 50000, // donation in paise (₹500)
    currency: "INR",
    name: "Udho Yadav Foundation",
    description: "Donation Support",
    image: "images/logo.png",
    handler: function(response) {
      alert("Thank you for your donation! Payment ID: " + response.razorpay_payment_id);
    },
    theme: { color: "#007bff" }
  };
  const rzp = new Razorpay(options);
  rzp.open();
});

/* Dark Mode Toggle */
const toggleBtn = document.getElementById('darkModeToggle');
toggleBtn.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
  const icon = toggleBtn.querySelector('i');
  icon.classList.toggle('fa-moon');
  icon.classList.toggle('fa-sun');
});

/* Active navbar highlighting on scroll */
const sections = document.querySelectorAll("section");
const navLinks = document.querySelectorAll(".nav-link");
window.addEventListener("scroll", () => {
  let current = "";
  sections.forEach(section => {
    const sectionTop = section.offsetTop - 80;
    if (scrollY >= sectionTop) current = section.getAttribute("id");
  });
  navLinks.forEach(link => {
    link.classList.remove("active");
    if (link.getAttribute("href").includes(current)) link.classList.add("active");
  });
});
