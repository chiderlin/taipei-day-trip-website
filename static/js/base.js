//TODO: 預定行程要檔未登入的使用者

let url = `/api/user`;
let item = document.querySelectorAll(".item");
let overlay_login = document.querySelector(".overlay-login");
let login_status = false;
init()

// controller
function init() {
    getUserStatus();
    
};

//預定行程
item[0].addEventListener("click", ()=> {
    if(login_status === false) {
        //沒登入 => 跳到登入畫面
        overlay_login.style.display = "block";
    }else {
        // 有登入 => 先判斷 有無uncheck的booking資料 =>有才跳轉
        // 無 => 跳通知 預定流程
        // getBookingStatus();
        window.location.href = `/booking`
    }
});


//使用者登入
item[1].addEventListener("click", ()=> {
    overlay_login.style.display = "block";
});

//使用者登出
item[2].addEventListener("click", ()=> {
    loginOut();
    item[1].classList.remove("hide");
    item[2].classList.add("hide");
});


// 登入關閉
let login_close_btn = document.getElementById("close-btn-for-img-login");
login_close_btn.addEventListener("click", ()=> {
    overlay_login.style.display = "none";
});


// 註冊關閉
let register_close_btn = document.getElementById("close-btn-for-img-register");
let overlay_register = document.querySelector(".overlay-register");
register_close_btn.addEventListener("click", ()=> {
    overlay_register.style.display = "none";
});


// 切換註冊畫面
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


// 提交登入表單
let login_form = document.getElementById("login-form");
login_form.addEventListener("submit", (event)=> {
    event.preventDefault(); // 要重新載入所以不用防
    let login_email = document.getElementById("email-login");
    let login_pwd = document.getElementById("pwd-login");
    let email = login_email.value;
    let pwd = login_pwd.value;
    logIn(email, pwd);

});


// 提交註冊表單
let register_form = document.getElementById("register-form");
register_form.addEventListener("submit", (event)=> {
    event.preventDefault();
    let register_name = document.getElementById("name")
    let register_email = document.getElementById("email-register");
    let register_pwd = document.getElementById("pwd-register");
    let name = register_name.value;
    let email = register_email.value;
    let pwd = register_pwd.value;
    userRegister(name, email, pwd);

});

function loginProcess(api_data) {
    // 跳轉 登入網頁之後的樣子
    if(api_data.ok === true) {
        loginedRender(); 

    } else if(api_data.error === true) {
        loginErrorRender(api_data);
    }
};

function bookingProcess(api_data) { 
    // 為了預定行程
    // 判斷有無登入
    if(api_data.data === null) {
        login_status = false;
    } else {
        login_status = true;
    }
}


//model
function getUserStatus() {
    // 一開始進入這個網頁時，呼叫此函式判斷是否已登入
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        initRenderItem(api_data);
        bookingProcess(api_data);
    })
};

// function getBookingStatus() { 
//     處理 有無booking資料
//     const url = `/api/booking`;
//     fetch(url).then(function(res) {
//         return res.json();
//     }).then(function(api_data) {
//         跳轉booking頁面
//         if(api_data.data !== null) {
//             window.location.href = `/booking`
//         }

//     }).catch(function(err) {
//         console.log(err);
//     });
// };



function userRegister(name, email, pwd) {
    let register_info = {"name":name, "email":email, "password":pwd};
    fetch(url, {
        method: "POST",
        body: JSON.stringify(register_info),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        renderRegister(api_data);
    }).catch(function(err) {
        console.log(err);
    });
};

function logIn(email, pwd) {
    let login_info = {"email": email, "password": pwd};
    fetch(url, {
        method: "PATCH",
        // credentials: "include",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(login_info)
    }).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        loginProcess(api_data);

    }).catch(function(err) {
        console.log(err);
    })

};

function loginOut() {
    fetch(url, {
        method: "DELETE",
        // credentials: 'include'
    })
    .then(function(res) {
        return res.json();
    }).then(function(api_data) {
        if(api_data.ok === true) {
            // window.location.reload();
            window.location.href = "/";
        } 
    })
};





//view
function initRenderItem(api_data) {
    //[0]預定行程 [1]登入/註冊 [2]登出系統
    if(api_data.data !== null) { //登入狀態
        item[2].classList.remove("hide");
        item[1].classList.add("hide");
    } else { //未登入狀態
        item[1].classList.remove("hide");
        item[2].classList.add("hide");

    }
};

function openLoginPage() {
    overlay_login.style.display = "block";
};

function renderRegister(api_data) {
    let register_page = document.querySelector(".register-page");
    let register_state = document.querySelector(".register-state");
    let register_msg = document.getElementById("register-msg");
    if(register_msg !== null) { // 如果有顯示過訊息 => 把tag清除掉 下面重製一個
        register_msg.remove();
    }
    if(api_data.ok === true) {
        register_msg = document.createElement("div");
        register_msg.className = "login-msg";
        register_msg.id = "register-msg";
        register_msg.style.color = "green";
        register_msg.appendChild(document.createTextNode("註冊成功"));
        register_page.appendChild(register_msg);
        register_page.insertBefore(register_msg, register_state)
        let register_name = document.getElementById("name")
        let register_email = document.getElementById("email-register");
        let register_pwd = document.getElementById("pwd-register");
        register_name.value = ""; // 註冊成功清空input
        register_email.value = "";
        register_pwd.value = "";

    } else if(api_data.error === true) {
        register_msg = document.createElement("div");
        register_msg.className = "login-msg";
        register_msg.id = "register-msg";
        register_msg.appendChild(document.createTextNode(api_data.message));
        register_page.appendChild(register_msg);
        register_page.insertBefore(register_msg, register_state)
    }
    
};

function loginedRender() {
    overlay_login.style.display = "none";
    item[1].classList.add("hide")
    item[2].classList.remove("hide")
    window.location.reload();
};

function loginErrorRender(api_data) {
    let login_page = document.querySelector(".login-page");
    let login_state = document.querySelector(".login-state");
    let login_msg = document.querySelector(".login-msg");
    if(login_msg !== null) { // 如果有顯示過訊息 => 把tag清除掉 下面重製一個
        login_msg.remove();
    }
    login_msg = document.createElement("div");
    login_msg.className = "login-msg";
    login_msg.appendChild(document.createTextNode(api_data.message));
    login_page.appendChild(login_msg);
    login_page.insertBefore(login_msg, login_state)
};

function renderNodata() {
    let shopping_cart = document.querySelector(".shopping-cart");
    let none_booking = document.createElement("div");
    none_booking.className = "null-block";
    none_booking.appendChild(document.createTextNode("尚無預定"));
    shopping_cart.appendChild(none_booking);
};

function renderBookingList(attraction_name) {
    let shopping_cart = document.querySelector(".shopping-cart");
    let booking = document.createElement("li");
    let booking_link = document.createElement("a");
    booking_link.setAttribute("href", "/booking");
    booking.appendChild(document.createTextNode(attraction_name));
    booking_link.appendChild(booking);
    shopping_cart.appendChild(booking_link);

};


// ==================================================


// 預定行程
// let checkbox = document.querySelector("input[name=booking]");
// checkbox.addEventListener("change",()=> {
//     let shopping_cart = document.querySelector(".shopping-cart");

//     if(checkbox.checked === true) {
//         shopping_cart.style.display = "block";
//     }else {
//         shopping_cart.style.display = "none";
//     }

// });



// function getBookingStatus() {
//     const url = `/api/booking`;
//     fetch(url).then(function(res) {
//         return res.json();
//     }).then(function(api_data) {
//         console.log(api_data.data);
//         if(api_data.data === null) {
//             renderNodata();
//         } else {
//             for(let i=0; i<api_data.data.length; i++) {
//                 let attraction_name = api_data.data[i].attraction.name;
//                 renderBookingList(attraction_name);
//             }
//         }
//     }).catch(function(err) {
//         console.log(err);
//     });
// };