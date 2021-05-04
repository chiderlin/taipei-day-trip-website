let title_list = [];
let img_url = [];
let mrt_list = [];
let category_list = [];
let id_list = [];
let next_page;
let count_view = 0;
let next_page_count = 1;
let keyword_page = 0;
const loading = document.querySelector(".loading"); // for lazy loading
const attractions = document.getElementById('attractions'); // 為了createElement
const keyword_tag = document.getElementById("keyword"); // 為了抓keyword的值
let checkProcess = false;

init(); // => 接getNextPage



// controller
function init() {
    getData(0, "")
};


// 偵測輸入關鍵字時
var isClick = true;
const keyword_form = document.getElementById("keyword-form");
keyword_form.addEventListener("submit", (event)=> {
    event.preventDefault(); // 防止網頁重load
    attractions.innerHTML = ""; // 重新載入，把內容先取消掉
    keyword_page = 0; // 每次搜尋頁數歸零
    if(isClick) { //防止短時間重複提交
        isClick = false;
        setTimeout(getKeyWordData(), 1000);
        setTimeout(function() {
            isClick = true;
        }, 300);
    }
});

// 偵測滾輪事件
window.addEventListener("scroll", ()=> {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    if(clientHeight+scrollTop >= scrollHeight) {
        if(keyword_tag.value === "" && next_page !== null) { // next_page是null的話就不會再重複一直呼叫ajax執行
            getNextPage();
        }else {
            if(checkProcess === false && next_page !== null) {
                getKeyWordData();
            }
        }
    }
});

window.addEventListener("click", (e)=>{
    let id = parseInt(e.path[1].children[0].innerText);
    let check_id_value = isNaN(id);
    // console.log(check_id_value);
    if(check_id_value === false) {
        // exports = { id };
        location.replace(`http://127.0.0.1:3000/attraction/${id}`);
    }
});

// function test() {
//     let smallbox_tag = document.getElementsByClassName("smallbox");
//     for(let i=0; i<smallbox_tag.length; i++) {
//         let page_number = smallbox_tag[i].childNodes
//         console.log(page_number[0].innerText);
//     }
//     console.log(smallbox_tag);
// };

// Model
function getData(page, keyword) {
    let url;
    checkProcess = true;
    console.log(keyword_tag.value);
    if(keyword_tag.value === "") {
        url = `http://35.73.36.129:3000/api/attractions?page=${page}`
    } else {
        url = `http://35.73.36.129:3000/api/attractions?page=${page}&keyword=${keyword}`
    }
    fetch(url).then(function(res) {
        return res.json();
    }).then(function(api_data) {
        checkProcess = false;
        next_page = api_data.nextPage;
        let data = api_data.data;
        data.forEach(ele => {
            id_list.push(ele.id) // 紀錄id 
        })
        if(keyword_tag.value !== "") { // 關鍵字查詢
            if(page === 0 && data.length === 0) { // 完全0筆資料
                renderNoData();
            }
            if(data !== null) { // 如果新頁數沒資料就不會處理了
                console.log(keyword_page);
                title_list = []; // 重新搜尋要恢復空array
                img_url = [];
                mrt_list = [];
                category_list = [];
                count_view = 0
                etlData(data); // 再把資料推進去
                render(data); 
                keyword_page++; //要放這才不會多加
            }
        }else {
            if(page !== 0) { // 下一頁
                if(data !== null) {
                    etlData(data);
                    render(data);
                }
            } else { // init
                etlData(data);
                render(data);
            }
        }
    }).catch(function(err) {
        console.log(err);
    });

};

function getKeyWordData() {
    getData(keyword_page, keyword_tag.value)
};

function getNextPage() {
    loading.classList.add("show");
    getData(next_page_count, "")
    next_page_count++;
};

function etlData(data) {
    data.forEach(element => {
        let images = element.images;
        let title = element.name;
        let mrt = element.mrt;
        let category = element.category;
        images = images.replaceAll("\'", "").replace("[", "").replace("]", "");
        images = images.split(', ') // images陣列 object
        img_url.push(images[0]); // img_url 裡面有12張風景照各一張
        title_list.push(title);
        mrt_list.push(mrt);
        category_list.push(category);
    })
};


// view
function render(data) {
    let data_length = data.length;
    let container_block = Math.floor(data_length/4); //藝術:1
    let box_block = data_length % 4;
    if(box_block !== 0) { //一排不滿四筆
        for(let i=0; i<container_block; i++) {
            const container = render_container();
            const bigbox = document.createElement("div");
            bigbox.className = "bigbox";
            container.appendChild(bigbox);
            for(let j=0; j<4; j++) {
                render_box(bigbox);
            }
        }
        for(let i=0; i<1; i++) {
            const container = render_container();
            const bigbox = render_bigbox(container);
            for(let j=0; j<box_block; j++) {
                render_box(bigbox);
            }
        }
    }else { //一排滿四筆
        for(let i=0; i<container_block; i++) {
            const container = render_container();
            const bigbox = render_bigbox(container)
            for(let j=0; j<4; j++) {
                render_box(bigbox);
            }
        }
    }
    loading.classList.remove("show");
};  

function render_container() {
    const container = document.createElement("div");
    container.className = "container";
    attractions.appendChild(container);
    return container;
};

function render_bigbox(container) {
    const bigbox = document.createElement("div");
    bigbox.className = "bigbox";
    container.appendChild(bigbox);
    return bigbox;
};


function render_box(bigbox) {
    const smallbox = document.createElement("div");
    const img = document.createElement("img");
    const name = document.createElement("div");
    const att_about = document.createElement("div");
    const mrt = document.createElement("div");
    const category = document.createElement("div");
    const id = document.createElement("div");
    id.style.display="none";
    smallbox.className = "smallbox";
    name.className = "attraction-name";
    att_about.className = "att-about";
    mrt.className = "mrt";
    category.className = "category";
    id.appendChild(document.createTextNode(id_list[count_view]))
    img.setAttribute("src", img_url[count_view]);
    name.appendChild(document.createTextNode(title_list[count_view]));
    if(mrt_list[count_view] === "None") {
        mrt_list[count_view] = "";
    }
    mrt.appendChild(document.createTextNode(mrt_list[count_view]));
    category.appendChild(document.createTextNode(category_list[count_view]));
    smallbox.appendChild(id);
    smallbox.appendChild(img);
    smallbox.appendChild(name);
    smallbox.appendChild(att_about);
    att_about.appendChild(mrt);
    att_about.appendChild(category);
    bigbox.appendChild(smallbox);
    count_view++;
}

function renderNoData() {
    const no_result = document.createElement("div");
    no_result.className = "container";
    no_result.appendChild(document.createTextNode("沒有結果"));
    attractions.appendChild(no_result);
}