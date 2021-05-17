let fixed = document.querySelector(".fixed");
let layout = document.querySelector(".layout");

init();
function init() {
    getBookingApi();
    getUserInfo();
};


//model
function getBookingApi() {
    let url = "/api/booking";
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(api_data) {
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
        let username = user_info.data.name;
        let email = user_info.data.email;
        renderTitle(username);
        renderclientInfo(username, email);
    })
};
function dropBooking() {
        const url = `/api/booking`;
        fetch(url, {
            method: "DELETE",
        }).then(function(res) {
            return res.json()
        }).then(function(api_data) {
            console.log(api_data);
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
    booking_title.appendChild(document.createTextNode(`台北一日遊:${name}`))
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




// controller 
let trash_img = document.getElementById("trash-img");
let inside_trash_img = document.getElementById("inside-trash-img");
trash_img.addEventListener("click", ()=> {
    if(window.confirm("確定要刪除此預定行程嗎?") == true) {
        dropBooking();
        window.location.reload();
    }

});

inside_trash_img.addEventListener("click", ()=> {
    if(window.confirm("確定要刪除此預定行程嗎?") == true) {
        dropBooking();
        window.location.reload();
    }

});
