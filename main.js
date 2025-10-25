// ==========================
// Back to Top Button
// ==========================
const backToTopBtn = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
  if (window.scrollY > 200) {
    backToTopBtn.style.display = "block";
  } else {
    backToTopBtn.style.display = "none";
  }
});

backToTopBtn.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// ==========================
// JSON-LD Structured Data
// ==========================
const ngoSchema = {
  "@context": "https://schema.org",
  "@type": "NGO",
  "name": "Shri Krishna Udhav Memorial Trust",
  "alternateName": "SKU Memorial Trust",
  "url": "https://trust-ngo.github.io/ShreeKrishnaUdhavTrust/",
  "logo": "https://github.com/Trust-NGO/ShreeKrishnaUdhavTrust/blob/main/Images/logo.jpg",
  "foundingDate": "2020-01-01",
  "founders": [
    {
      "@type": "Person",
      "name": "Shri Udho Yadav"
    }
  ],
  "foundingLocation": {
    "@type": "Place",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "Deoria",
      "addressRegion": "Uttar Pradesh",
      "postalCode": "274001",
      "addressCountry": "IN"
    }
  },
  "email": "krishnaudhavtrust@gmail.com",
  "telephone": "+91-9918640455",
  "sameAs": [
    "https://facebook.com/yourpage",
    "https://twitter.com/yourhandle",
    "https://instagram.com/yourhandle"
  ],
  "description": "Shri Krishna Udhav Memorial Trust works to empower communities in Deoria through education, healthcare, and rural development programs.",
  "areaServed": {
    "@type": "AdministrativeArea",
    "name": "Deoria, Uttar Pradesh"
  },
  "nonprofitStatus": "https://schema.org/Nonprofit501c3"
};

// Inject JSON-LD into the head
const script = document.createElement('script');
script.type = 'application/ld+json';
script.text = JSON.stringify(ngoSchema, null, 2);
document.head.appendChild(script);

// ==========================
// Optional: Dynamic Links (if needed)
// ==========================
const policyLinks = {
  privacy: "privacy.html",
  refund: "refund.html",
  terms: "terms.html",
  disclaimer: "disclaimer.html"
};

// Example: dynamically set footer links if you want to manage from JS
document.querySelectorAll('footer a').forEach(link => {
  const text = link.textContent.trim().toLowerCase();
  if(policyLinks[text]){
    link.href = policyLinks[text];
  }
});
