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
    Admin.setAttribute("Class", "active");
    Adoctor.setAttribute("Class", "");
    Analytics.setAttribute("Class", "");

    Vdoctor.setAttribute("Class", "");
    Aclinic.setAttribute("Class", "");
    Vclinic.setAttribute("Class", "");

}

Adoctor.onclick = function () {
    Admin.setAttribute("Class", "");
    Adoctor.setAttribute("Class", "active");
    Analytics.setAttribute("Class", "");

    Vdoctor.setAttribute("Class", "");
    Aclinic.setAttribute("Class", "");
    Vclinic.setAttribute("Class", "");

}

Vdoctor.onclick = function () {
    Admin.setAttribute("Class", "");
    Adoctor.setAttribute("Class", "");
    Analytics.setAttribute("Class", "");

    Vdoctor.setAttribute("Class", "active");
    Aclinic.setAttribute("Class", "");
    Vclinic.setAttribute("Class", "");

}

Analytics.onclick = function () {
    Admin.setAttribute("Class", "");
    Adoctor.setAttribute("Class", "");
    Analytics.setAttribute("Class", "active");

    Vdoctor.setAttribute("Class", "");
    Aclinic.setAttribute("Class", "");
    Vclinic.setAttribute("Class", "");

}
Aclinic.onclick = function () {
    Admin.setAttribute("Class", "");
    Adoctor.setAttribute("Class", "");
    Analytics.setAttribute("Class", "");

    Vdoctor.setAttribute("Class", "");
    Aclinic.setAttribute("Class", "active");
    Vclinic.setAttribute("Class", "");
}
Vclinic.onclick = function () {
    Admin.setAttribute("Class", "");
    Adoctor.setAttribute("Class", "");
    Analytics.setAttribute("Class", "");

    Vdoctor.setAttribute("Class", "");
    Aclinic.setAttribute("Class", "");
    Vclinic.setAttribute("Class", "active");
}


