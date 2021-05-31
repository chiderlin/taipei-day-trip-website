// let login_status = false; // base.js已經有了
let get_route = location.pathname
let images;  //click也抓images
let attraction_id;

init();
//controller
function init() {
    getData(get_route); // 取得網頁編號 => 進行attraction的render page
    getUserStatus(); // 看有無登入
    disableDayBefore(); // 過去日期不要讓使用者做booking
};

function bookingProcess(user_info) { //true false切換登入狀態
    if(user_info.data !== null) {
        login_status = true;
    } else {
        login_status = false;
    }
};

function disableDayBefore() {
    let date_cal = document.getElementById("date");
    let today = new Date().toISOString().split('T')[0]; // ["2021-05-18", "06:06:54.157Z"]
    date_cal.setAttribute("min", today);
};


// 輪播效果切換
let left_arrow = document.getElementById("left-arrow");
let right_arrow = document.getElementById("right-arrow");
let count = 1;
left_arrow.addEventListener("click",()=> {
    count--;
    if(count === 0) {
        count = images.length;
    }
    document.querySelector(`#control-${count}`).checked = true;
});

right_arrow.addEventListener("click",()=> {
    count++;
    if(count === images.length+1) {
        count = 1;
    }
    document.querySelector(`#control-${count}`).checked = true;
});

function autoSlide() {
    setInterval(function() {
        count++;
        if(count === images.length+1) {
            count = 1;
        }
        document.querySelector(`#control-${count}`).checked = true;
    },5000);
};


// 按上半天 下半天 => 按字就可以觸發效果
let morning_block = document.getElementById("morning");
let afternoon_block = document.getElementById("afternoon");
let morning_btn = document.getElementById("morning-btn");
let afternoon_btn = document.getElementById("afternoon-btn");
let fee_block = document.getElementById("fee-block");
let show_price = document.getElementById("price");

morning_block.addEventListener("click", ()=> {
    morning_btn.style.background = "#448899";
    morning_btn.style.border = "2px solid #fff";
    afternoon_btn.style = "none";
    show_price.innerHTML = "";
    show_price.appendChild(document.createTextNode("新台幣2000元"));
    fee_block.appendChild(show_price);
});

afternoon_block.addEventListener("click", ()=> {
    afternoon_btn.style.background = "#448899";
    afternoon_btn.style.border = "2px solid #fff";
    morning_btn.style = "none";
    show_price.innerHTML = "";
    show_price.appendChild(document.createTextNode("新台幣2500元"));
    fee_block.appendChild(show_price);
});


// 提交預定行程
let date = document.getElementById("date");
let price_tag = document.getElementById("price");
let booking_trip_btn = document.getElementById("booking-trip-btn");
booking_trip_btn.addEventListener("click", ()=>{
    if(login_status === false) {
        let overlay_login = document.querySelector(".overlay-login");
        overlay_login.style.display = "block";

    } else if(login_status === true) {
        let price = "";
        let time = "";
        for(let i=3; i<price_tag.innerText.length-1; i++) {
            price = price + price_tag.innerText[i]; //擷取數字部分
        }
        if(date.value === "") {
            renderMessage("日期");
            return;
        }
    
        if(price === "") {
            renderMessage("時間");
            return;
        }
    
        price = parseInt(price);
        if(price === 2000) {
            time = "morning";
        }else if(price === 2500){
            time = "afternoon";
        }
    
        startBooking(date.value, price, time);
    }
    
});


// model
function getData(path) { // path => /attraction/num
    let url = `/api${path}`
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        // getData
        let data = api_data.data;
        attraction_id = data.id;
        images = data.images;
        const name = data.name;
        const category = data.category;
        const mrt = data.mrt;
        const desc = data.description;
        const address = data.address;
        let transport = data.transport;
        if(transport === "None") {
            transport = " ";
        };
        images = images.replaceAll("\'", "").replace("[", "").replace("]", "");
        images = images.split(', ') // images陣列 object

        renderUpperBlock(images, name, category, mrt);
        renderDownerBlock(desc, address, transport);
        checkRender();
    })
};

function getUserStatus() {
    let url = "/api/user"
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(user_info) {
        bookingProcess(user_info);
    })
};

function startBooking(date, price, time) {
    let url = `/api/booking`;
    let new_booking = {"attractionId": attraction_id, "date": date, "time": time, "price": price}
    fetch(url, {
        method: "POST",
        body: JSON.stringify(new_booking),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        if(api_data.ok === true) {
            window.location.href = `/booking`
        }
    })
};


//view
function renderUpperBlock(images, name, category, mrt) {
    const booking_block = document.querySelector(".booking-block");
    const booking_area = document.querySelector(".booking-area");
    const atte_name = document.querySelector(".attr-name");
    const about = document.querySelector(".about");
    imageSlider(images);
    atte_name.appendChild(document.createTextNode(name));
    about.appendChild(document.createTextNode(`${category} at ${mrt}`)); 
    booking_block.appendChild(atte_name);
    booking_block.appendChild(about);
    booking_block.insertBefore(atte_name, booking_area); // (先,後)
    booking_block.insertBefore(about, booking_area);
};

function renderDownerBlock(desc, address, transport) {
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

function imageSlider() {
    if(images.length > 10) {
        images.length = 10;
    }
    for(let i=0; i<images.length; i++) { //看長度，限定最多10張照片
        const image_block = document.querySelector(`.slide${i+1}`);
        const dots_block = document.querySelector(`.control-dots`);   
        if(image_block === null) { // 預設html一個標籤 如果圖片超過一張在這裡新增
            // 新增.slide
            const slider = document.getElementById("slider");
            const slide_slide1 = document.querySelector(".slide.slide1");
            const slide = document.createElement("div");
            const radio_input = document.createElement("input");
            const dot_control = document.createElement("label");
            slide.className = `slide`; 
            slide.style.left = `${i}00%`; //後面新增的就不用給slide3,4,5 直接加%給它
            const img = document.createElement("img");
            img.className = "attaction-img";
            img.setAttribute("src", images[i]);
            radio_input.setAttribute("type", "radio");
            radio_input.setAttribute("id", `control-${i+1}`);
            radio_input.setAttribute("name","control");
            dot_control.setAttribute("for",`control-${i+1}`)
            slide.appendChild(img);
            slider.appendChild(radio_input);
            slider.appendChild(slide);
            dots_block.appendChild(dot_control);
            slider.insertBefore(radio_input, dots_block);
            slider.insertBefore(slide, radio_input);
            slider.insertBefore(radio_input, slide_slide1);
        } else { // 照片只有一張
            const img = document.createElement("img");
            img.className = "attaction-img";
            img.setAttribute("src", images[i]);
            image_block.appendChild(img);
        }
    }
    autoSlide();
};


function renderMessage(msg) { //提示訊息
    let booking_area = document.querySelector(".booking-area");
    let booking_message = document.querySelector(".booking-message");
    if(booking_message !== null) {
        booking_message.remove();
    }
    let message = document.createElement("div");
    message.className = "booking-message";
    message.appendChild(document.createTextNode(`請選擇${msg}`))
    booking_area.appendChild(message);
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