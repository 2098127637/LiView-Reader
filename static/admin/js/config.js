const menu =
[{
    "name": "阅读记录",
    "icon": "&#xe609;",
    "url": "",
    "hidden": true,
    "list": [{
        "name": "栏目管理",
        "url": "type_index.html"
    }, {
        "name": "文章管理",
        "url": "article_index.html"
    }]
}, {
    "name": "书库",
    "icon": "&#xe68e;",
    "url": "/",
    "hidden": false,
    "list": []
}, {
    "name": "添加书籍",
    "icon": "&#xe61f;",
    "url": "addBook",
    "hidden": false,
    "list": []
}, {
    "name": "设置",
    "icon": "&#xe620;",
    "url": "/set",
    "hidden": false,
    "list": []
}, {
    "name": "开发文档",
    "icon": "&#xe655;",
    "url": "http://docs.qadmin.net/",
    "target": "_blank",
    "list": []
}];

const config = {
    name: "LiView",
    menu: menu,
};

// module.exports.name = "Qadmin";
// module.exports.menu = menu;
