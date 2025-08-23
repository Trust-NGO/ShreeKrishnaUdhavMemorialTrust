// Volunteer Form alert
const form = document.querySelector('.volunteer-form');
if(form) {
form.addEventListener('submit',function(e){e.preventDefault();alert('Thank you for showing interest / आपके सहयोग के लिए धन्यवाद!');form.reset();});
}