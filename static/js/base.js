// login 事件處理

// 登入/註冊按鈕
let item = document.querySelectorAll(".item");
item[1].addEventListener("click", ()=> { // item[1]登入按鈕
    let overlay = document.querySelector(".overlay-login");
    overlay.style.display = "block";
})

// 登入關閉
let login_close_btn = document.getElementById("close-btn-for-img-login");
let overlay_login = document.querySelector(".overlay-login");

login_close_btn.addEventListener("click", ()=> {
    overlay_login.style.display = "none";
})

// 註冊關閉
let register_close_btn = document.getElementById("close-btn-for-img-register");
let overlay_register = document.querySelector(".overlay-register");

register_close_btn.addEventListener("click", ()=> {
    overlay_register.style.display = "none";
})


// 切換註冊
let register_link = document.getElementById("register");
register.addEventListener("click", ()=>{
    overlay_login.style.display = "none";
    overlay_register.style.display = "block";
});

// 切換登入畫面
let login_link = document.getElementById("login");
login_link.addEventListener("click", ()=> {
    overlay_register.style.display = "none";
    overlay_login.style.display = "block";
});