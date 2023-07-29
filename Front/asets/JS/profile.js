const editBTN = document.querySelector(".profile-edit-edit-btn")
const doneBTN = document.querySelector(".profile-edit-done-btn")
const cancelBTN = document.querySelector(".profile-edit-cancel-btn");
const changeIMG = document.querySelector(".change-profile-img")

function editFun(e){
    e.preventDefault();
    doneBTN.style.display = "block";
    cancelBTN.style.display = "block";
    changeIMG.style.visibility = "visible";
    e.target.style.display="none";
}

editBTN.addEventListener("click",editFun)

cancelBTN.addEventListener("click", (e) => {
    e.preventDefault();
    window.location.reload();
});
