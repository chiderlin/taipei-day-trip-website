init()
/* *controller* */
function init() {
    getHistoryOrder();
};



/* *model* */
function getHistoryOrder() {
    let url = "api/orders/history"
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(order_list) {
        if(order_list.error === true) {
            window.location.href = "/";
            return;
        }
        if(order_list.data !== null) {
            ProcessList(order_list.data);
            // 有資料 才讓table_block打開
            let table_block = document.querySelector(".table-block");
            table_block.style.display = "block";
        } else {
            renderNoHistory();
        }

    })
};

function ProcessList(data_dict) { // 新增多少列資料&多少塊資料
    for(let i=data_dict.length-1; i>=0; i--) { // 最新的資料在最上面
        const create_time = data_dict[i].create_time;
        const number = data_dict[i].number;
        const order_price = data_dict[i].order_price;
        const status = data_dict[i].status;
        renderCells(create_time, number, order_price, status);
        renderSmallContainer(create_time, number, order_price, status);
        
    }
};



/* *view* */
function renderCells(create_time, number, order_price, status) {
    let tbody = document.querySelector("tbody");
    let order_info = document.createElement("tr");
    let footer = document.querySelector("footer");
    for(let i=0; i<4; i++) { // 每列資料有四個欄位
        let detail_data = document.createElement("td");
        order_info.appendChild(detail_data);
    }
    let link_num = document.createElement("a");
    link_num.style.color = "#66AABB";
    link_num.setAttribute("href", `/thankyou?number=${number}`)
    
    // input data
    link_num.appendChild(document.createTextNode(number))
    order_info.children[0].appendChild(link_num);
    order_info.children[1].appendChild(document.createTextNode(create_time));
    order_info.children[2].appendChild(document.createTextNode(`台幣 ${order_price} 元`));
    format_status = status_format(status);
    order_info.children[3].appendChild(document.createTextNode(format_status));
    tbody.appendChild(order_info);
    footer.style.height = "75vh";
};

function renderSmallContainer(create_time, number, order_price, status) {
    let small_container = document.querySelector(".small-container");
    let small_table_block = document.createElement("div");
    let small_table = document.createElement("table");
    let tr;
    let td;
    small_table_block.className = "small-table-block";
    small_table.className = "small";
    format_status = status_format(status);
    
    // 一個table
    for(let i=0; i<4; i++) {
        tr = document.createElement("tr");
        small_table.appendChild(tr);
        for(let j=0; j<2; j++) {
            if(i===0 && j===1) { // 抓number做超連結
                let link_num = document.createElement("a");
                link_num.style.color = "#66AABB";
                link_num.setAttribute("href", `/thankyou?number=${number}`);
                link_num.appendChild(document.createTextNode(number));
                td = document.createElement("td");
                tr.append(td);
                td.appendChild(link_num);
            } else {
                td = document.createElement("td");
                tr.appendChild(td);
            }
        };
        tr.children[0].style.color = "#ffffff";
        if(i===0) {
            tr.children[0].appendChild(document.createTextNode("訂單編號"));
        } else if(i === 1) {
            tr.children[0].appendChild(document.createTextNode("訂單時間"));
            tr.children[1].appendChild(document.createTextNode(create_time));
        } else if(i === 2) {
            tr.children[0].appendChild(document.createTextNode("訂單金額"));
            tr.children[1].appendChild(document.createTextNode(`台幣 ${order_price} 元`));
        } else if(i === 3) {
            tr.children[0].appendChild(document.createTextNode("訂單狀態"));
            tr.children[1].appendChild(document.createTextNode(format_status));
        };
    }
    small_table_block.appendChild(small_table);
    small_container.appendChild(small_table_block);

};

function renderNoHistory() {
    let container = document.querySelector(".container"); // 大的畫面
    let small_container = document.querySelector(".small-container"); //小畫面
    let big_state = document.createElement("div");
    let small_state = document.createElement("div");
    let footer = document.querySelector("footer");
    big_state.className = "no-payment-state";
    small_state.className = "no-payment-state";
    big_state.appendChild(document.createTextNode("目前沒有歷史紀錄"));
    small_state.appendChild(document.createTextNode("目前沒有歷史紀錄"));
    
    container.appendChild(big_state);
    small_container.appendChild(small_state);
    footer.style.height = "90vh";
};

function status_format(status) {
    let format;
    if(status === 0) {
        format = "已付款"
    } else if(status === 1) {
        format = "付款失敗"
    }
    return format;
};