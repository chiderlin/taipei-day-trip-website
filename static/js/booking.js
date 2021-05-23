let fixed = document.querySelector(".fixed");
let layout = document.querySelector(".layout");
let order = {};

init();

// controller
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


//model
function getBookingApi() {
    let url = "/api/booking";
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        cleanup_order_json(api_data); // 產生order物件

        if(api_data.data === null) {
            renderNoBooking();
        } else {
            const data = api_data.data;
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
    });
};

function getUserInfo() {
    let url = "api/user";
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(user_info) {
        if(user_info.data !== null) {
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

    // last-block
    const price_check = document.querySelector(".price-check");

    if(time === "morning") {
        time = "早上9點到下午4點";
    } else if (time === "afternoon") {
        time = "下午2點到晚上9點";
    }

    booking_img.className = "booking-img";
    price_check.className = "price-check";
    booking_img.setAttribute("src", image);
    booking_title.appendChild(document.createTextNode(`台北一日遊:${name}`));
    booking_date.appendChild(document.createTextNode(date));
    booking_time.appendChild(document.createTextNode(time));
    booking_price.appendChild(document.createTextNode(`新台幣${price}元`));
    booking_address.appendChild(document.createTextNode(address));
    price_check.appendChild(document.createTextNode(`新台幣${price}元`));
    img_block.appendChild(booking_img);
};

function renderNoBooking() {
    let footer = document.querySelector("footer");
    footer.style.height = "100vh";
    let nobooking = document.createElement("div");
    nobooking.className = "nobooking";
    nobooking.appendChild(document.createTextNode("目前沒有任何待預定的行程"));
    fixed.appendChild(nobooking);
};


// 串接金流取prime
TPDirect.setupSDK(20343, "app_PxPSoHZCppMvxjkyNzFnuRmqtgvENcu1rDkYKxl8ZOZHjJfKOkCtAxpmKKbW", "sandbox");
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
    style: {
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

function checkAndPay(event) {
    event.preventDefault();
    const tappaystatus = TPDirect.card.getTappayFieldsStatus();
    // console.log(tappaystatus);
    TPDirect.card.getPrime(function(result) {
        if(result.status !== 0) {
            console.log("getPrime錯誤"+result.status);
            return;
        }
        let prime = result.card.prime;
        // console.log(result);
        let phone = document.getElementById("client-phonenum");
        let email = document.getElementById("client-email");
        let name = document.getElementById("client-name");
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
        // console.log(build_order);
        fetch(url, {
            method: "POST",
            body: JSON.stringify(build_order),
            headers: {
                "Content-Type": "application/json"
            }
        }).then(function(res){
            return res.json();
        }).then(function(api_data){
            console.log(api_data);
        })
    });
};

function cleanup_order_json(api_data) {
    //儲存order 全域變數
    order = {
        "price": api_data.data.price,
        "trip": {
            "attraction": api_data.data.attraction
        },
        "date": api_data.data.date,
        "time": api_data.data.time
    };
};

