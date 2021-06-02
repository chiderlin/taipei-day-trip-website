init();

/* *controller* */
function init() {
    let get_query_string = location.search;
    let ordernum = "";
    if(get_query_string === "") {
        // thankyou後面沒有?number 就會直接被導回首頁
        window.location.href="/"
    }else {
        // 取number號碼
        for(let i=8; i<get_query_string.length; i++) {
            ordernum += get_query_string[i];
        }
    };
    getOrderInfo(ordernum);
};

/* *model* */
function getOrderInfo(ordernum) {
    let url = `api/order/${ordernum}`;
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        if(api_data.data === null){ // 直接進入thankyou頁面，但是無此number
            renderNoOrder(); 

        } else if(api_data.error === true) { // 沒有登入
            window.location.href = "/";

        }else { // 有資料
            let bank_transaction = api_data.data.bank_transaction;
            let price = api_data.data.price;
            let attraction_name = api_data.data.trip.attraction.name;
            let attractionId = api_data.data.trip.attraction.id;
            let trip_date = api_data.data.date;
            let trip_time = api_data.data.time;
            renderPaymentDetail(ordernum, bank_transaction, price, attraction_name, attractionId, trip_date, trip_time);
        }
        checkRender();
    })
};

/* *view* */
function renderPaymentDetail(number, bank_transaction, price, attraction, attractionId, date, time) {
    let container = document.querySelector(".container");
    let payment_state = document.querySelector(".payment-state");
    let order_num = document.getElementById("order_number");
    let bank_num= document.getElementById("bank_number");
    let order_price = document.getElementById("order_price");
    let link_attraction = document.createElement("a");
    let attraction_name = document.getElementById("attraction_name");
    let trip_date = document.getElementById("trip_date");
    let trip_time = document.getElementById("trip_time");
    let footer = document.querySelector("footer");
    let format_time = timeSetting(time);
    container.style.display = "block";
    link_attraction.style.color = "#66AABB";
    payment_state.appendChild(document.createTextNode("付款成功"));
    order_num.appendChild(document.createTextNode(number));
    bank_num.appendChild(document.createTextNode(bank_transaction));
    order_price.appendChild(document.createTextNode(`新台幣 ${price} 元`));
    link_attraction.setAttribute("href", `/attraction/${attractionId}`)
    link_attraction.appendChild(document.createTextNode(attraction));
    attraction_name.appendChild(link_attraction);
    trip_date.appendChild(document.createTextNode(date));
    

    trip_time.appendChild(document.createTextNode(format_time));
    footer.style.height="100vh";
};

function renderNoOrder() {
    let fixed = document.querySelector(".fixed");
    let payment_state = document.createElement("div");
    let footer = document.querySelector("footer");
    payment_state.style.fontSize = "19px";
    payment_state.style.fontWeight = "bold";
    payment_state.style.margin = "20px";
    payment_state.appendChild(document.createTextNode("查無此訂單資訊"));
    fixed.appendChild(payment_state);
    footer.style.height="100vh";
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
    let fixed = document.querySelector(".fixed");
    let footer = document.querySelector("footer");
    loading_circle.style.display = "none";
    flexbox.style.display = "flex";
    fixed.style.display = "flex";
    footer.style.display = "flex";
};