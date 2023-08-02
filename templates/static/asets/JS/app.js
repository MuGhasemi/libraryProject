const profileViewModel = document.querySelector(".profile-view");
const hamMenuBTN = document.querySelector(".ham-menu-icon");
const hanMenuItem = document.querySelector(".ham-menu-item");
const hamMenuCloseBTN = document.querySelector(".close-ham-menu");

hamMenuCloseBTN.addEventListener("click", () => {
    hanMenuItem.style.animation = "fadeInUp 0.25s forwards";
});
hamMenuBTN.addEventListener("click", () => {
    hanMenuItem.style.animation = "fadeInDown 0.25s forwards";
});

profileViewModel.addEventListener("mouseenter", (e) => {
    const modulePro = document.querySelector(".profile-view-module");
    modulePro.style.display = "flex";
});
profileViewModel.addEventListener("mouseleave", (e) => {
    const modulePro = document.querySelector(".profile-view-module");
    modulePro.style.display = "none";
});
