// login 按鈕事件處理
let item = document.querySelectorAll(".item");
item[1].addEventListener("click", ()=> {
    let overlay = document.querySelector(".overlay");
    overlay.style.display = "block";
})

// 關閉事件
let close_btn = document.getElementById("close-btn-for-img");
close_btn.addEventListener("click", ()=> {
    let overlay = document.querySelector(".overlay");
    overlay.style.display = "none";
})