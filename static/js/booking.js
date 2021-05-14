const url = `http://127.0.0.1:3000/api/booking`;
init();
function init() {
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        console.log(api_data);
        const data = api_data.data;
        const attraction = data.attraction;
        // const id = attraction.id;
        const name = attraction.name;
        const image = attraction.image;
        const address = attraction.address;
        const date = data.date;
        const price = data.price;
        const time = data.time;
        renderUpperBlock(name, image, address, date, price, time);

    })
}

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

let trash_img = document.getElementById("trash-img");
let inside_trash_img = document.getElementById("inside-trash-img");
trash_img.addEventListener("click", ()=> {
    dropBooking();

});
inside_trash_img.addEventListener("click", ()=> {
    dropBooking();

});

function dropBooking() {
    fetch(url, {
        method: "DELETE",
    }).then(function(res) {
        return res.json()
    }).then(function(api_data) {
        console.log(api_data);
    })

};