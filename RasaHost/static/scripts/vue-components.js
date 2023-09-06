Vue.prototype.$setQueryString = function (key, value) {
    //Vue.prototype 扩展了 Vue 实例的原型，使其可在所有组件中访问。
    //用于更新URL中查询字符串参数
    var baseUrl = [location.protocol, '//', location.host, location.pathname].join('');//构建 baseUrl 变量，它包含了当前页面的协议、主机名和路径。
    urlQueryString = location.search;
    newParam = key + '=' + value,
    params = '?' + newParam;
    //location 是代表当前文档的 JavaScript 对象，它包含有关当前页面 URL 的信息。
    //location.search 是一个 JavaScript 属性，用于获取当前页面 URL 中的查询字符串部分（不包括问号 ?）。
    //查询字符串通常用于传递参数给网页，它是一系列键值对的形式，以 key=value 的方式组织，多个键值对之间使用 & 符号分隔。
    //在 JavaScript 中，可以使用逗号运算符（,）将多个表达式合并成一个表达式，这些表达式按顺序执行，最后一个表达式的值将成为整个表达式的值。

    // If the "search" string exists, then build params from it
    if (urlQueryString) {
        var updateRegex = new RegExp('([\?&])' + key + '[^&]*');//只匹配参数键名，这个正则表达式的目的是找到要更新的参数。
        //‘([\?&])’匹配一个问号 ? 或者一个 & 符号
        //’[^&]*‘匹配零个或多个非 & 字符
        var removeRegex = new RegExp('([\?&])' + key + '=[^&;]+[&;]?');//匹配整个键值，这个正则表达式的目的是找到要删除的参数。

        if (typeof value == 'undefined' || value == null || value == '') { // Remove param if value is empty
            params = urlQueryString.replace(removeRegex, "$1");//replace接受两个参数：要匹配的正则表达式和要替换匹配内容的字符串。
            //$1 在这里表示正则表达式中的第一个捕获组--([\?&])，也就是参数键名前面的 ? 或 & 符号。
            params = params.replace(/[&;]$/, "");//为了确保删除参数后，不会在查询字符串末尾留下不必要的分隔符。

        } else if (urlQueryString.match(updateRegex) !== null) { // If param exists already, update it
            params = urlQueryString.replace(updateRegex, "$1" + newParam);

        } else { // Otherwise, add it to end of query string
            params = urlQueryString + '&' + newParam;
        }
    }

    // no parameter was set so we don't need the question mark
    params = params == '?' ? '' : params;

    window.history.replaceState({}, "", baseUrl + params);//用于操作浏览器的历史记录。
    //它允许你在不刷新页面的情况下更改浏览器的 URL 和历史状态。
};

Vue.prototype.$getQueryString = function (name) {
    //用于获取URL中指定名称的查询字符串参数的值
    var url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');//正则表达式中的 [ 和 ] 需要使用反斜杠 \ 进行转义
    ///[\[\]]/g -- /['\[''\]']/ g--全局匹配修饰符，表示查找所有匹配而不是在找到第一个匹配后停止。
    // \\$& -- \\--转译反斜杠 
    //$&--这是一个特殊的标记，用于表示正则表达式匹配到的文本（也就是被替换的文本）。在替换操作中，$& 会被匹配到的文本所替代。
    //所以'[',']'会被替代为'\[','\]'
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);//如果匹配成功，它会返回一个包含匹配信息的数组。
        //数组的第一个元素是整个匹配结果，后续元素是捕获组的匹配结果（例如参数名称和参数值）。
    if (!results) return null;
    if (!results[2]) return '';//如果找到了匹配的结果但没有参数值，返回空字符串
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
    //如果找到了匹配的结果且有参数值，对参数值进行解码，并将+号替换为空格。
};

Vue.prototype.$fetch = function (url = ``, parameters = {}) {
    //发送一个HTTP请求并返回一个Promise对象，包含了请求的结果
    return fetch(url, parameters)
        .then(r => r.text().then(text => ({ ok: r.ok, status: r.status, statusText: r.statusText, text: text })))
        //返回了一个新的对象，该对象包含以下属性：
        //ok：表示 HTTP 响应是否成功。
        //status：表示 HTTP 响应的状态码。
        //statusText：表示 HTTP 响应的状态消息。
        //text：表示 HTTP 响应的文本内容。
        .then(r => {
            if (r.text) {
                try {
                    r.json = JSON.parse(r.text) 
                } catch (e) {
                    console.log("Response from server the server: " + r.text)
                }
                return r;
            }
            return r;
         })
        .then(response => {
            if (response.json && response.json.error)
                throw Error(response.json.error);
            if (!response.ok)
                throw Error(response.status + ': ' + response.statusText);
            return response.json;
        })
};

Vue.component('text-editor', {
    //一个名为'text-editor'的自定义组件定义，接受一个名为'value'的属性，并在内部
    //使用CodeMirror实现一个文本编辑器
    props: ['value'],
    watch: {
        value: function (val) {
            if (val != this.textEditor.getValue()) {
                this.textEditor.setValue(val ? val : '');
            }
        },
    },
    mounted: function () {
        var scope = this;
        this.textEditor = CodeMirror.fromTextArea(document.getElementById('text_editor'), {
            lineNumbers: true
        });
        this.textEditor.on('change', function (cm) {
            scope.textEditor.save();
            scope.$emit('input', cm.getValue())
            //var info = this.textEditor.getScrollInfo();
            //document.getElementsByClassName("CodeMirror")[0].style.minWidth = info.width + "px";
        });
        this.textEditor.setValue(this.value ? this.value : '');
        this.textEditor.setSize("100%", "100%");

        //var info = this.textEditor.getScrollInfo();
        //document.getElementsByClassName("CodeMirror")[0].style.minWidth = info.width + "px";
    },
    template: '<textarea id="text_editor"></textarea>'
});

Vue.component('files-list', {
    //一个名为'files-list'的自定义组件定义，用于显示文件列表并支持搜索功能
    //接受一个名为'module'的属性，通过发送异步请求获取文件列表数据
    template: `
        <div>
            {{error}}
            <div class="input-group">
                <input v-model="query" v-on:keyup.enter="search" type="text" class="form-control form-control-sm" placeholder="Search...">
                <div class="input-group-append">
                    <button v-on:click="search" class="btn btn-sm btn-outline-secondar" type="button">Search <div v-if="isSearching" class="loader"></div></button>
                </div>
            </div>
            <ul class="ul-items">
                <li v-for="(item, index) in items" @click="selectItem(item, index)">
                    <a v-on:click.prevent="" v-bind:href="'/' + module +'?path='+item.path" v-bind:class="{'active': item == selectedItem}" class="nav-link">{{item.name}}</a>
                </li>
            </ul>
        </div>
    `,
    props: ['module'],
    data: function () {
        return {
            query: '',
            items: [],
            noItems: false,
            isSearching: false,
            error: '',
            selectedItem: null
        }
    },
    mounted: function () {
        this.query = this.$getQueryString("q") || '';
        this.search();
    },
    methods: {
        selectItem: function (item, index) {
            this.selectedItem = item;
            this.$emit('selected-item', { 'item': this.selectedItem })
        },
        search: function () {
            if (this.isSearching) {
                return;
            }
            this.isSearching = true;
            this.error = '';
            this.$setQueryString("q", this.query);
            fetch(`/api/${this.module}?q=${encodeURIComponent(this.query)}`)
                .then(function (response) {
                    if (!response.ok)
                        throw Error(response.status + ': ' + response.statusText);
                    return response.json();
                })
                .then(res => {
                    if (res.error)
                        throw Error(res.error);
                    this.isSearching = false;
                    this.items = res;
                    this.noItems = this.items.length === 0;
                })
                .catch(error => {
                    this.isSearching = false;
                    this.items = [];
                    this.noItems = false;
                    this.error = "Error: " + error.message;
                });
        }
    }
});