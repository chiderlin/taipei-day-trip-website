let fixed = document.querySelector(".fixed");
let layout = document.querySelector(".layout");
let order = {};
let attrId;
let userId;
init();

/* *controller* */ 
function init() {
    getBookingApi();
    getUserInfo();
};

// 刪除預定行程 (我做兩個垃圾桶按鈕，在RWD時顯示不同個)
let trash_img = document.getElementById("trash-img");
let inside_trash_img = document.getElementById("inside-trash-img");
trash_img.addEventListener("click", ()=> {
    if(window.confirm("確定要刪除此預定行程嗎?") == true) {
        dropBooking();
    }
});

inside_trash_img.addEventListener("click", ()=> {
    if(window.confirm("確定要刪除此預定行程嗎?") == true) {
        dropBooking();
    }
});


// payment onclick按鈕
function checkAndPay(event) {
    event.preventDefault();
    //const tappaystatus = TPDirect.card.getTappayFieldsStatus();
    //console.log(tappaystatus);
    TPDirect.card.getPrime(function(result) {
        //console.log(result); //status:0, msg:succrss
        if(result.status !== 0) {
            renderError("信用卡資訊輸入錯誤");
            return;
        }
        let prime = result.card.prime;
        let phone = document.getElementById("client-phonenum");
        let email = document.getElementById("client-email");
        let name = document.getElementById("client-name");
        makeaPayment(prime, phone, email, name);
    });
};

// 把order存到全域變數再給makeapayment用
function cleanup_order_json(api_data) {
    order = {
        "price": api_data.data.price,
        "trip": {
            "attraction": api_data.data.attraction
        },
        "date": api_data.data.date,
        "time": api_data.data.time
    };
};

// 串接金流取prime
//(appID, appKey, serverType)
TPDirect.setupSDK(20343, "app_PxPSoHZCppMvxjkyNzFnuRmqtgvENcu1rDkYKxl8ZOZHjJfKOkCtAxpmKKbW", "Sandbox");
//PDirect.setupSDK(11327, "app_whdEWBH8e8Lzy4N6BysVRRMILYORF6UxXbiOFsICkz0J9j1C0JUlCHv1tVJC", "Sandbox");
let fields = {
    number: {
        element: "#card-number",
        placeholder: " **** **** **** ****"
    },
    expirationDate: {
        element: "#card-expiration-date",
        placeholder: " MM / YY"
    },
    ccv: {
        element: "#card-ccv",
        placeholder: " CCV"
    }
};

TPDirect.card.setup({
    fields: fields,
    styles: {
        'input': {
            'color': 'gray'
        },
        'input.ccv': {
            'font-size': '16px'
        },
        'input.expiration-date': {
            'font-size': '16px'
        },
        'input.card-number': {
            'font-size': '16px'
        },
        ':focus': {
            'color': 'black'
        },
        '.valid': {
            'color': 'green'
        },
        '.invalid': {
            'color': 'red'
        },
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    }
});



/* *model* */
function getBookingApi() {
    let url = "/api/booking";
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        if(api_data.data === null) {
            renderNoBooking();
        } else {
            cleanup_order_json(api_data); // 產生order物件
            const data = api_data.data;
            attrId = data.attraction.id;
            const attraction = data.attraction;
            const name = attraction.name;
            const image = attraction.image;
            const address = attraction.address;
            const date = data.date;
            const price = data.price;
            const time = data.time;
            layout.style.display = "block";
            renderPage(name, image, address, date, price, time);
        }
        checkRender();
    });
};

function getUserInfo() {
    let url = "api/user";
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(user_info) {
        if(user_info.data !== null) {
            userId = user_info.data.id;
            let username = user_info.data.name;
            let email = user_info.data.email;
            renderTitle(username);
            renderclientInfo(username, email);
        } else { // 直接進入/booking網址 沒登入直接導回首頁
            window.location.href = "/";
        }
    })
};

function dropBooking() {
    const url = `/api/booking`;
    fetch(url, {
        method: "DELETE",
    }).then(function(res) {
        return res.json()
    }).then(function(api_data) {
        if(api_data.ok === true) {
            window.location.reload();
        }
    })
};

function makeaPayment(prime, phone, email, name) {
    let url = "api/orders"
    let build_order = {
        "prime": prime,
        "order": order,
        "contact": {
            "name":name.value,
            "email":email.value,
            "phone":phone.value
        }
    }
    if(name.value === "") {
        renderError("請輸入姓名");
        return;
    };
    if(email.value === "") {
        renderError("請輸入email");
        return;
    };
    if(phone.value === "") {
        renderError("請輸入手機號碼");
        return;
    }else if(phone.value.length !== 10) {
        renderError("手機號碼格式錯誤");
        return;
    };
    fetch(url, {
        method: "POST",
        body: JSON.stringify(build_order),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res){
        return res.json();
    }).then(function(api_data){
        if(api_data.error === true) {
            // 付款失敗
            return;
        }
        if(api_data.data.payment.status === 0) { //付款成功，轉到thankyou page 顯示訂單資料
            let ordernum = api_data.data.number;
            window.location.href = `/thankyou?number=${ordernum}`;
        }
    }).catch(function(err){
        console.log(err);
    });
};



//view
function renderTitle(username) {
    const booking_status = document.querySelector(".booking-status");
    booking_status.appendChild(document.createTextNode(`您好，${username}，待預訂的行程如下:`));
};

function renderclientInfo(username, email) {
    const name_block = document.getElementById("name-block");
    const email_block = document.getElementById("email-block");
    const client_name = document.getElementById("client-name");
    const client_email = document.getElementById("client-email");
    client_name.setAttribute("value", username);
    client_email.setAttribute("value", email);
    name_block.appendChild(client_name);
    email_block.appendChild(client_email);

};

function renderPage(name, image, address, date, price, time) {
    const booking_title = document.querySelector(".booking-title");
    const booking_date = document.getElementById("booking-date");
    const booking_time = document.getElementById("booking-time");
    const booking_price = document.getElementById("booking-price");
    const booking_address = document.getElementById("booking-address");
    const img_block = document.querySelector(".img-block");
    const booking_img = document.createElement("img");
    const format_time = timeSetting(time);

    // last-block
    const price_check = document.querySelector(".price-check");
    
    booking_img.className = "booking-img";
    price_check.className = "price-check";
    booking_img.setAttribute("src", image);
    booking_title.appendChild(document.createTextNode(`台北一日遊:${name}`));
    booking_date.appendChild(document.createTextNode(date));
    booking_time.appendChild(document.createTextNode(format_time));
    booking_price.appendChild(document.createTextNode(`新台幣${price}元`));
    booking_address.appendChild(document.createTextNode(address));
    price_check.appendChild(document.createTextNode(`新台幣${price}元`));
    img_block.appendChild(booking_img);
};

function renderError(msg) {
    let error_msg = document.querySelector(".error-msg");
    error_msg.innerHTML = "";
    error_msg.appendChild(document.createTextNode(msg));
    error_msg.style.display = "block";

};

function renderNoBooking() {
    let footer = document.querySelector("footer");
    footer.style.height = "100vh";
    let nobooking = document.createElement("div");
    nobooking.className = "nobooking";
    nobooking.appendChild(document.createTextNode("目前沒有任何待預定的行程"));
    fixed.appendChild(nobooking);
};

function timeSetting(time) {
    if(time === "morning") {
        time = "早上9點到下午4點";
    } else if(time === "afternoon") {
        time = "下午2點到晚上9點"
    };
    return time;
};

function checkRender() {
    let loading_circle = document.querySelector(".loading-circle");
    let flexbox = document.querySelector(".flexbox");
    let head = document.querySelector(".head");
    let footer = document.querySelector("footer");
    loading_circle.style.display = "none";
    flexbox.style.display = "flex";
    head.style.display = "flex";
    footer.style.display = "flex";
};
