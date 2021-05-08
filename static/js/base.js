// controller
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



let login_form = document.getElementById("login-form");
login_form.addEventListener("submit", (event)=> {
    event.preventDefault();
    getLoginData();

});
function getLoginData() {
    let login_email = document.getElementById("email-login");
    let login_pwd = document.getElementById("pwd-login");
    let email = login_email.value;
    let pwd = login_pwd.value;
    fetchPatch(email, pwd);
};



let register_form = document.getElementById("register-form");
register_form.addEventListener("submit", (event)=> {
    event.preventDefault();
    getRegisterData();

});
function getRegisterData() {
    //註冊
    let register_name = document.getElementById("name")
    let register_email = document.getElementById("email-register");
    let register_pwd = document.getElementById("pwd-register");
    let name = register_name.value;
    let email = register_email.value;
    let pwd = register_pwd.value;
    fetchPost(name, email, pwd);
};

//model
function fetchPost(name, email, pwd) {
    let url = `http://127.0.0.1:3000/api/user`;
    let register_info = {"name":name, "email":email, "password":pwd};
    console.log(register_info);
    fetch(url, {
        method: "POST",
        body: JSON.stringify(register_info),
        headers: {
            "Content-Type": "application/json"
        }
        // credentials: "include", // 存取跨域cookie
        // mode: "no-cors",
    }).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        console.log(api_data);
        // 註冊完成要跳到首頁，讓使用者再自行登入

    }).catch(function(err) {
        console.log(err);
    });
};

function fetchPatch(email, pwd) {
    // 登入
    let url = `http://127.0.0.1:3000/api/user`
    let login_info = {"email": email, "password": pwd};
    fetch(url, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(login_info) // patch 用data 不是 body
    }).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        console.log(api_data);
        // 下面要跳轉 登入網頁之後的樣子
    }).catch(function(err) {
        console.log(err);
    })

};


// 以下兩個未完成
function fetchDelete() {
    // 要做一個登出按鈕 click事件 => 再呼叫這個函式
    // 登出使用者
    let url = `http://127.0.0.1:3000/api/user`;
    fetch(url, {
        method: "DELETE"
    })
    .then(function(res) {
        return res.json();
    }).then(function(api_data) {
        console.log(api_data);
    })

};

function fetchGet() {
    // 一開始進入這個網頁時，呼叫此函式判斷是否已登入，已登入的顯示畫面跟未登入顯示畫面不同
    // 已登入的使用者
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        console.log(api_data);
    })
};