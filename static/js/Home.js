var home = document.getElementById("home");
var specialities = document.getElementById("specialities");
var contact = document.getElementById("contact");
var login = document.getElementById("login");
var about = document.getElementById("about");

home.onclick = function () {
    home.setAttribute("Class", "active");
    specialities.setAttribute("Class", "");
    contact.setAttribute("Class", "");
    login.setAttribute("Class", "");
    about.setAttribute("Class", "");

}

specialities.onclick = function () {
    home.setAttribute("Class", "");
    specialities.setAttribute("Class", "active");
    contact.setAttribute("Class", "");
    login.setAttribute("Class", "");
    about.setAttribute("Class", "");

}

contact.onclick = function () {
    home.setAttribute("Class", "");
    specialities.setAttribute("Class", "");
    contact.setAttribute("Class", "active");
    login.setAttribute("Class", "");
    about.setAttribute("Class", "");

}

login.onclick = function () {
    home.setAttribute("Class", "");
    specialities.setAttribute("Class", "");
    contact.setAttribute("Class", "");
    login.setAttribute("Class", "active");
    about.setAttribute("Class", "");

}
about.onclick = function () {
    home.setAttribute("Class", "");
    specialities.setAttribute("Class", "");
    contact.setAttribute("Class", "");
    login.setAttribute("Class", "");
    about.setAttribute("Class", "active");
}

