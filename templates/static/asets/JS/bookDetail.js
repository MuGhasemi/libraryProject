//NOTE modal 

const showModalBtn = document.querySelector(".book-borrow-btn");
const modal = document.querySelector(".modal-book-det");
const backdrop = document.querySelector(".backdrop-book-det");
const close = document.querySelector(".close-modal-det");
const confirm = document.querySelector(".confirm-modal-det");

showModalBtn.addEventListener("click", () => {
    
   modal.style.opacity = "1";
   modal.style.transform = "translateY(10vh)";
   backdrop.style.display = "block";
});
function closeM() {
   modal.style.opacity = "0";
   modal.style.transform = "translateY(-100vh)";
   backdrop.style.display = "none";
}

close.addEventListener("click", (e)=>{
   e.preventDefault();
   closeM();
});
backdrop.addEventListener("click", closeM);
confirm.addEventListener("click", () => {
   closeM();
});

