const activePge = window.location.href;
const navList = document.querySelectorAll('nav a').
    forEach(link => {
        if (link.href == activePge) {
            link.classList.add('active');
        }
    });

var i = 0;
var txt = 'כאן תוכלו למצוא את כל החדשות החמות והעדכונים השווים ';
var speed = 50;

function typeWriter() {
    if (i < txt.length) {
        document.getElementById("demo").innerHTML += txt.charAt(i);
        i++;
        setTimeout(typeWriter, speed);
    }
}
window.onload = typeWriter();

