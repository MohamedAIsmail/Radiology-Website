let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");
let searchBtn = document.querySelector(".bx-search");

closeBtn.addEventListener("click", () => {
    sidebar.classList.toggle("open");
    menuBtnChange();
});

searchBtn.addEventListener("click", () => { // Sidebar open when you click on the search iocn
    sidebar.classList.toggle("open");
    menuBtnChange();
});
Admin.onclick = function () {
    home.setAttribute("Class", "active");
    specialities.setAttribute("Class", "");
    contact.setAttribute("Class", "");
    login.setAttribute("Class", "");
    about.setAttribute("Class", "");

}

Adoctor.onclick = function () {
    home.setAttribute("Class", "");
    specialities.setAttribute("Class", "active");
    contact.setAttribute("Class", "");
    login.setAttribute("Class", "");
    about.setAttribute("Class", "");

}

Vdoctor.onclick = function () {
    home.setAttribute("Class", "");
    specialities.setAttribute("Class", "");
    contact.setAttribute("Class", "active");
    login.setAttribute("Class", "");
    about.setAttribute("Class", "");

}

Analytics.onclick = function () {
    home.setAttribute("Class", "");
    specialities.setAttribute("Class", "");
    contact.setAttribute("Class", "");
    login.setAttribute("Class", "active");
    about.setAttribute("Class", "");

}
Aclinic.onclick = function () {
    home.setAttribute("Class", "");
    specialities.setAttribute("Class", "");
    contact.setAttribute("Class", "");
    login.setAttribute("Class", "");
    about.setAttribute("Class", "active");
}
Vclinic.onclick = function () {
    home.setAttribute("Class", "");
    specialities.setAttribute("Class", "");
    contact.setAttribute("Class", "");
    login.setAttribute("Class", "");
    about.setAttribute("Class", "active");
}


