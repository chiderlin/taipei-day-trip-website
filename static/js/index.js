
window.onload = function() {
    // init
    // for clean data.
    let title_list = [];
    let img_url = [];
    let mrt_list = [];
    let category_list = [];
    let count_view = 0;
    let next_page_count = 1;
    let keyword_page = 0;
    const loading = document.querySelector(".loading"); // for lazy loading
    const attractions = document.getElementById('attractions'); // 為了createElement
    const keyword = document.getElementById("keyword"); // 為了抓keyword的值
    
    init();

    function init() {
        const url = `http://35.73.36.129:3000/api/attractions?page=0`
        fetch(url).then(function(res) {
            return res.json();
        }).then(function(api_data) {
            let data = api_data.data;
            etlData(data);
            render(data);
        }).catch(function(err) {
            console.log(err);
        });
    };


    // controller
    // 偵測輸入關鍵字時
    const keyword_search = document.getElementById("keyword-form");
    keyword_search.addEventListener("submit", (event)=> {
        event.preventDefault(); // 防止網頁重load
        attractions.innerHTML = ""; // 重新載入，把內容先取消掉
        keyword_page = 0
        getKeyWordData();
    })
    
    // 偵測滾輪事件
    window.addEventListener("scroll", ()=> {
        const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
        if(clientHeight+scrollTop >= scrollHeight) {
            if(keyword.value === "") {
                getNextPage();
            }else {
                getKeyWordData();
            }
        }
    });


    // Model
    function getKeyWordData() {
        const url = `http://35.73.36.129:3000/api/attractions?page=${keyword_page}&keyword=${keyword.value}`
        fetch(url).then(function(res) {
            return res.json();
        }).then(function(api_data) {
            console.log(api_data);
            const data = api_data.data;
            if(keyword_page === 0 && data.length === 0) {
                renderNoData();
            }
            if(data !== null) {
                etlData(data);
                render(data); // render新畫面
                keyword_page++;
            }

        }).catch(function(err) {
            console.log(err);
        });
    };

    function getNextPage() {
        loading.classList.add("show");
        const url = `http://35.73.36.129:3000/api/attractions?page=${next_page_count}`
        fetch(url)
        .then(function(res) {
            return res.json();
        }).then(function(api_data) {
            let data = api_data.data;
            if(data !== null) {
                etlData(data);
                render(data);
                next_page_count++;
            }
        }).catch(function(err) {
            console.log(err);
        })
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
        let box_block = data_length%4; //藝術:1

        for(let i=0; i<container_block; i++) {
            const container = render_container();
            for(let j=0; j<4; j++) {
                render_box(container);
            }
        }
        if(box_block !== 0) {
            for(let i=0; i<1; i++) {
                const container = render_container();
                for(let j=0; j<box_block; j++) {
                    render_box(container);
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

    function render_box(container) {
        const box = document.createElement("div");
        const img = document.createElement("img");
        const name = document.createElement("div");
        const att_about = document.createElement("div");
        const mrt = document.createElement("div");
        const category = document.createElement("div");
        box.className = "box";
        name.className = "attraction-name";
        att_about.className = "att-about";
        mrt.className = "mrt";
        category.className = "category";
        img.setAttribute("src", img_url[count_view]);
        name.appendChild(document.createTextNode(title_list[count_view]));
        mrt.appendChild(document.createTextNode(mrt_list[count_view]));
        category.appendChild(document.createTextNode(category_list[count_view]));
        att_about.appendChild(mrt);
        att_about.appendChild(category);
        box.appendChild(img);
        box.appendChild(name);
        box.appendChild(att_about);
        container.appendChild(box);
        count_view++;
    }

    function renderNoData() {
        const no_result = document.createElement("div");
        no_result.className = "container";
        no_result.appendChild(document.createTextNode("沒有結果"));
        attractions.appendChild(no_result);
    }

};