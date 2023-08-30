Vue.prototype.$setQueryString = function (key, value) {
    //用于更新URL中查询字符串参数
    var baseUrl = [location.protocol, '//', location.host, location.pathname].join('');
        urlQueryString = document.location.search,
        newParam = key + '=' + value,
        params = '?' + newParam;

    // If the "search" string exists, then build params from it
    if (urlQueryString) {
        var updateRegex = new RegExp('([\?&])' + key + '[^&]*');
        var removeRegex = new RegExp('([\?&])' + key + '=[^&;]+[&;]?');

        if (typeof value == 'undefined' || value == null || value == '') { // Remove param if value is empty
            params = urlQueryString.replace(removeRegex, "$1");
            params = params.replace(/[&;]$/, "");

        } else if (urlQueryString.match(updateRegex) !== null) { // If param exists already, update it
            params = urlQueryString.replace(updateRegex, "$1" + newParam);

        } else { // Otherwise, add it to end of query string
            params = urlQueryString + '&' + newParam;
        }
    }

    // no parameter was set so we don't need the question mark
    params = params == '?' ? '' : params;

    window.history.replaceState({}, "", baseUrl + params);
};

Vue.prototype.$getQueryString = function (name) {
    //用于获取URL中指定名称的查询字符串参数的值
    var url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);//使用正则表达式的exec方法在URL中查找与参数名匹配的部分
    if (!results) return null;//如果没有找到匹配的结果，返回null
    if (!results[2]) return '';//如果找到了匹配的结果但没有参数值，返回空字符串
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
    //如果找到了匹配的结果且有参数值，对参数值进行解码，并将+号替换为空格。
};

Vue.prototype.$fetch = function (url = ``, parameters = {}) {
    //发送一个HTTP请求并返回一个Promise对象，包含了请求的结果
    return fetch(url, parameters)
        .then(r => r.text().then(text => ({ ok: r.ok, status: r.status, statusText: r.statusText, text: text })))
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