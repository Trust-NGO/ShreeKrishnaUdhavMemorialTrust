// Mobile nav toggle
document.addEventListener('DOMContentLoaded', function () {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function () {
            navMenu.classList.toggle('show');
            this.setAttribute('aria-expanded', navMenu.classList.contains('show'));
        });
    }

    // Tabs logic
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(tc => tc.hidden = true);
            this.classList.add('active');
            const tabId = this.getAttribute('aria-controls');
            document.getElementById(tabId).hidden = false;
        });
    });

    // Footer tab links (for accessibility)
    document.querySelectorAll('.footer-tab-link').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            document.getElementById('tab-policies').click();
            window.scrollTo({top: document.getElementById('about').offsetTop - 60, behavior: 'smooth'});
        });
    });

    // Volunteer form validation
    const vForm = document.getElementById('volunteer-form');
    if (vForm) {
        vForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const name = vForm.name.value.trim();
            const email = vForm.email.value.trim();
            const msg = document.getElementById('form-msg');
            msg.textContent = '';
            msg.className = 'form-msg';
            let valid = true;
            // Simple validation
            if (!name) {
                msg.textContent = 'Name is required.';
                msg.classList.add('error');
                vForm.name.focus();
                valid = false;
            } else if (!validateEmail(email)) {
                msg.textContent = 'Valid email is required.';
                msg.classList.add('error');
                vForm.email.focus();
                valid = false;
            }
            if (valid) {
                msg.textContent = 'Thank you for volunteering! We will contact you soon.';
                msg.classList.add('success');
                vForm.reset();
            }
        });
    }

    function validateEmail(email) {
        // Simple email regex
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
});