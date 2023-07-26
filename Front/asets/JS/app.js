const profileViewModel = document.querySelector(".profile-view");

profileViewModel.addEventListener("mouseenter", (e) => {
    const modulePro = document.querySelector(".profile-view-module");
    modulePro.style.display = "flex";
});
profileViewModel.addEventListener("mouseleave", (e) => {
    const modulePro = document.querySelector(".profile-view-module");
    modulePro.style.display = "none";
});


