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

function frontend(){
    const id = document.getElementById("front_id").value;
    const url = `https://reqres.in/api/users/${id}`;
    fetch(url)
        .then(response => response.json())
        .then(value => {
            document.getElementById('user_span').innerHTML = `
            <h3>${value.data["first_name"]} ${value.data["last_name"]}</h3>
            <p>${value.data["email"]}</p>
            <img src="${value.data["avatar"]}" alt="avatar"/>
            `
        })
}