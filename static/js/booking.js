
getBookingApi();
// model
function getBookingApi() {
    const url = `/api/booking`;
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        console.log(api_data);
        for(let i=0; i<api_data.data.length; i++) {
            const data = api_data.data[i];
            const attraction = data.attraction;
            const name = attraction.name;
            const image = attraction.image;
            const address = attraction.address;
            const date = data.date;
            const price = data.price;
            const time = data.time;
            renderUpperBlock(name, image, address, date, price, time);
        }
    });
}

function dropBooking() {
    const url = `/api/booking`;
    fetch(url, {
        method: "DELETE",
    }).then(function(res) {
        return res.json()
    }).then(function(api_data) {
        console.log(api_data);
    })

};

getUserInfo();
function getUserInfo() {
    const url = `/api/user`;
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        let email = api_data.data.email;
        let name = api_data.data.name;
        renderBookingStatus(name, email);

    });
};



// controller 
let trash_img = document.getElementById("trash-img");
let inside_trash_img = document.getElementById("inside-trash-img");
trash_img.addEventListener("click", ()=> {
    if(window.confirm("確定要刪除此預定行程嗎?") == true) {
        dropBooking();
        window.location.href = "/";
    }

});

inside_trash_img.addEventListener("click", ()=> {
    if(window.confirm("確定要刪除此預定行程嗎?") == true) {
        dropBooking();
        window.location.href = "/";
    }

});


//view
function renderUpperBlock(name, image, address, date, price, time) {
    let booking_title = document.querySelector(".booking-title");
    let booking_date = document.getElementById("booking-date");
    let booking_time = document.getElementById("booking-time");
    let booking_price = document.getElementById("booking-price");
    let booking_address = document.getElementById("booking-address");
    let img_block = document.querySelector(".img-block");
    let booking_img = document.createElement("img");

    booking_img.className = "booking-img";
    booking_img.setAttribute("src", image);
    booking_title.appendChild(document.createTextNode(`台北一日遊:${name}`))
    booking_date.appendChild(document.createTextNode(date));
    booking_time.appendChild(document.createTextNode(time));
    booking_price.appendChild(document.createTextNode(`新台幣${price}元`));
    booking_address.appendChild(document.createTextNode(address));

    img_block.appendChild(booking_img);
};

function renderBookingStatus(name, email) {
    // upper
    let booking_status = document.querySelector(".booking-status");
    
    // middle
    let client_name = document.getElementById("client-name");
    let client_email = document.getElementById("client-email");
    
    booking_status.appendChild(document.createTextNode(`您好，${name}，待預訂的行程如下:`))
    client_name.setAttribute("value", name);
    client_email.setAttribute("value", email);

};

