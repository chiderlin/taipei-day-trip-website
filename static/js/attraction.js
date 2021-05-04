// import {id} from "./index.js";
// const { id } = require('./index');


getData();

// model
function getData(id) {
    // let url = `http://35.73.36.129:3000/api/attraction/${id}`
    let url = `http://35.73.36.129:3000/api/attraction/1`
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        // getData
        let data = api_data.data;
        let images = data.images;
        const name = data.name;
        const category = data.category;
        const mrt = data.mrt;
        const desc = data.description;
        const address = data.address;
        const transport = data.transport;
        images = images.replaceAll("\'", "").replace("[", "").replace("]", "");
        images = images.split(', ') // images陣列 object

        renderUpperBlock(images, name, category, mrt);
        renderDownerBlock(desc, address, transport);
    })
};




//controller
//view
function renderUpperBlock(images, name, category, mrt) {
        //上
        const upper_block = document.querySelector(".upper-block");
        const image_block = document.querySelector(".image");
        const booking_block = document.querySelector(".booking-block");
        const booking_area = document.querySelector(".booking-area");
        const atte_name = document.querySelector(".attr-name");
        const about = document.querySelector(".about");
        const img = document.createElement("img");
        img.setAttribute("src", images[0]);
        atte_name.appendChild(document.createTextNode(name));
        about.appendChild(document.createTextNode(`${category} at ${mrt}`));

        image_block.appendChild(img);
        booking_block.appendChild(atte_name);
        booking_block.appendChild(about);
        booking_block.insertBefore(atte_name, booking_area); // (先,後)
        booking_block.insertBefore(about, booking_area);
};


function renderDownerBlock(desc, address, transport) {
        
    // 下
    const downer_block = document.querySelector(".downer-block");
    const desc_tag = document.querySelector(".desc");
    const address_class = document.querySelector(".address");
    const transport_class = document.querySelector(".transport");  
    const address_content = document.createElement("div")
    const transport_content = document.createElement("div")
    address_content.className = "content";
    transport_content.className = "content";
    desc_tag.appendChild(document.createTextNode(desc));
    address_content.appendChild(document.createTextNode(address));
    transport_content.appendChild(document.createTextNode(transport));
    address_class.appendChild(address_content);
    transport_class.appendChild(transport_content);
    downer_block.appendChild(desc_tag);
    downer_block.insertBefore(desc_tag, transport_class);
    downer_block.insertBefore(desc_tag, address_class);
};


