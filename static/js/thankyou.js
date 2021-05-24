let get_query_string = location.search;
let ordernum = "";
if(get_query_string === "") {
    window.location.href="/"
}else {
    for(let i=8; i<get_query_string.length; i++) {
        ordernum += get_query_string[i];
    }
};

init();
function init() {
    getOrderInfo(ordernum);
};

function getOrderInfo(ordernum) {
    let url = `api/order/${ordernum}`;
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        if(api_data.data === null){ // 直接進入thankyou頁面，但是order無資料
            // renderError(); 

        } else if(api_data.error === true) { // 沒有登入
            window.location.href = "/";

        }else { // 有資料
            let bank_transaction = api_data.data.bank_transaction;
            let price = api_data.data.price;
            renderPaymentDetail(ordernum, bank_transaction, price);
        }
    })
};

function renderPaymentDetail(number, bank_transaction, price) {
    let container = document.querySelector(".container");
    let payment_state = document.querySelector(".payment-state");
    let order_num = document.getElementById("order_number");
    let bank_num= document.getElementById("bank_number");
    let order_price = document.getElementById("order_price");
    let footer = document.querySelector("footer");
    container.style.display = "block";
    payment_state.appendChild(document.createTextNode("付款成功"));
    order_num.appendChild(document.createTextNode(number));
    bank_num.appendChild(document.createTextNode(bank_transaction));
    order_price.appendChild(document.createTextNode(`新台幣 ${price} 元`));

    footer.style.height="100vh";
};

function renderError() {
    let container = document.querySelector(".container");
    let payment_state = document.querySelector(".payment-state");
    container.style.display = "block";
    payment_state.appendChild(document.createTextNode("付款失敗"));

};