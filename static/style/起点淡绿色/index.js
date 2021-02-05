
//预加载准备
var preloadHeight;
$(document).ready(function(){
    //加载设置
    path = $("#j-readPage").attr('path')
    $.post("/getBookSet",{path:path}, function(data) {
               initial_fontSize = data['fontSize'];
               initial_pageWidth = data['pageWidth'];
    		   $('#chapter-402733549').css('font-size',data['fontSize']);//字体大小
    		   $('#j_readMainWrap').css('width',data['pageWidth']);//页面宽度
               $('#j_leftBarList').attr('style', 'left:' + document.getElementById("j_chapterBox").offsetLeft + 'px');//左侧功能栏重新定位
			});
	settingFun();
});



//获取URL参数

function getQueryVariable(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return(false);
}

// 下拉上拉加载
var clientHeight = $(window).height() //当前可视的页面高度
var timestamp = Date.parse(new Date());
//滚动条到页面底部加载更多
$(window).scroll(function(){
    //下拉加载
     //var scrollTop = $('#j_readMainWrap').scrollTop(); //滚动条距离顶部的高度
     var scrollTop = (document.body.scrollTop || document.documentElement.scrollTop);//滚动条距离顶部的高度
     var scrollHeight = $(document).height(); //当前页面的总高度
     if(scrollTop >= scrollHeight-clientHeight){ //滚动到最低端
     dataLast = timestamp;//上次加载时间
     timestamp = Date.parse(new Date());//当前时间
     console.log('间隔时间',timestamp - dataLast);
     if (timestamp - dataLast>500){//且时间间隔大于15000加载下一章
        layer.msg('下章加载中请稍后！', {
  				    offset: 't',
  				    anim: 6
			    });
		path = $("#j-readPage").attr('path')
        $.post("/nextChapter",{path,path}, function(data) {
        	   $('#j_readMainWrap').append(data);
  			   //document.getElementById("j_readMainWrap").innerHTML = data;
  			   console.log($(".text-wrap"));
  			   console.log($(".text-wrap").length);
  			   if ($(".text-wrap").length >=5){
  			        $(".text-wrap")[0].remove();
  			        };
		        });

        }else{//太快提醒
        layer.msg('操作频繁请稍后再试！', {
  				    offset: 't',
  				    anim: 6
			    });
        }

      }

     //上拉加载
     if(scrollTop == 0){ //滚动到最低端
     dataLast = timestamp;//上次加载时间
     timestamp = Date.parse(new Date());//当前时间
     console.log('间隔时间',timestamp - dataLast);
     if (timestamp - dataLast>500){//且时间间隔大于15000加载下一章
        layer.msg('上章加载中请稍后！', {
  				    offset: 't',
  				    anim: 6
			    });
		path = $("#j-readPage").attr('path')
		if ($(".text-wrap").eq(0).attr('history') != "1" && $(".text-wrap").eq(0).attr('history') != "cover"){
		        console.log($("#j-readPage").attr('path'),String(1));
		       console.log('上一章');
		       var history = $(".text-wrap").eq(0).attr('history')
		       $.post("/lastChapter",{path:path,history:history}, function(data) {
        	   $('#j_readMainWrap').prepend(data);
  			   //document.getElementById("j_readMainWrap").innerHTML = data;
  			   console.log($(".text-wrap"));
  			   console.log($(".text-wrap").length);
  			   if ($(".text-wrap").length >=5){
  			        $(".text-wrap").eq(-1).remove();
  			        };
		        });

		    };
        }else{//太快提醒
        layer.msg('操作频繁请稍后再试！', {
  				    offset: 't',
  				    anim: 6
			    });
        }

      }
})


//目录被点击事件
function catalogFun(){
//发送请求请求数据

//发送请求
path = $("#j-readPage").attr('path')
$.post("/catalog",{path,path}, function(data) {
		catalogUpdateFun(data[1])//加载目录html
		});

}
function catalogUpdateFun(catalogData){
var a = `
<body class ='layui-bg-gray' style="background-color:#ebe5d8;">
<fieldset class="layui-elem-field">
  <legend style='font-size:20px;'><em>目录</em></legend>
  <div id="catalog" class="layui-field-box" style='font-size:16px;'></div>
</fieldset>
</body>
`;

var openIndex = layer.open({
  type: 1,
  title:'Liview-Reader',
  skin: 'layui-layer-rim', //加上边框
  area: ['800px', '700px'], //宽高
  content: a
});

function treeClick(){
var checkData = tree.getChecked('demoId');
layer.msg(checkData, {
  				offset: 't',
  				anim: 6
  				});
};

//树组件：
layui.use('tree', function(){
    var tree = layui.tree;

    //渲染
    var inst1 = tree.render({
      elem: '#catalog'  //绑定元素
      ,id: 'demoId' //定义索引
      ,accordion: true
      ,showLine:false
      ,data: catalogData
       ,click: function(obj){
    		console.log(obj.data['id']);//获取id
    		var id = obj.data['id'];
    		path = $("#j-readPage").attr('path')
    		$.post("/catalogClick",{id:id,path:path}, function(data) {
    		    $('#j_readMainWrap').html("");
        		$('#j_readMainWrap').append(data);
			});
			layer.close(openIndex);//关闭弹出层
  		}
    });
  });
}

//设置被点击事件
function settingFun(){
    path = $("#j-readPage").attr('path')
    $.post("/getResList",{path:path}, function(data) {//获取coption
               console.log(data);
    		   styleOption = data['styleStr'];
    		   fontOption = data['fontStr']
    		   console.log(styleOption,fontOption);
    });
    setHtml = `
<body>
    <div class="layui-tab">
        <ul class="layui-tab-title">
            <li class="layui-this">页面设置</li>
            <li>主题设置</li>
            <li>阅读方式</li>
            <li>字体设置</li>
        </ul>
            <div class="layui-tab-content">
                <div class="layui-tab-item layui-show">
                    <fieldset class="layui-elem-field">
                        <form class="layui-form" action="">
                            <div class="layui-form-item">
                                <div class="layui-row">
                                    <div class="layui-col-md2">
                                        <label class="layui-form-label">字体大小</label>
                                    </div>
                                    <div class="layui-col-md10">
                                        </br>
                                        <div id="fontSize"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="layui-form-item">
                                    <div class="layui-row">
                                        <div class="layui-col-md2">
                                            <label class="layui-form-label">页面宽度</label>
                                        </div>
                                        <div class="layui-col-md10">
                                            </br>
                                            <div id="pageWidth"></div>
                                        </div>
                                    </div>
                            </div>
                        </form>
                        <button id="pageSetButton" class="layui-btn layui-btn-fluid">保存</button>
                    </fieldset>
            </div>
            <div class="layui-tab-item">
                <fieldset class="layui-elem-field">
                    <form class="layui-form" action="">
                        <div class="layui-form-item">
                            <label class="layui-form-label">主题</label>
                            <div class="layui-input-block">
                                <select  lay-verify="required" lay-search id="style">
                                    <!--
                                    <option>起点黄</option>
                                    <option>起点绿</option>
                                    <option>起点黑</option>
                                    <option>简约白</option>
                                    <option>简约黄</option>
                                    <option>简约绿</option>
                                    -->
                                    styleOption
                                </select>
                            </div>
                        </div>

                        <div class="layui-form-item">
                            <div class="layui-input-block">
                                <button type="reset" class="layui-btn layui-btn-primary" id="reset">重置</button>
                            </div>
                        </div>
                    </form>
                    <button class="layui-btn layui-btn-fluid" id="styleSetButton">保存</button>
                </fieldset>
            </div>
            <div class="layui-tab-item">
                开发中，下个版本再来看看吧!
            </div>
            <div class="layui-tab-item">
                <fieldset class="layui-elem-field">
                    <form class="layui-form" action="">
                        <div class="layui-form-item">
                            <label class="layui-form-label">字体设置</label>
                            <div class="layui-input-block">
                                <select  lay-verify="required" lay-search id="font">
                                    <!--
                                    <option>起点黄</option>
                                    <option>起点绿</option>
                                    <option>起点黑</option>
                                    <option>简约白</option>
                                    <option>简约黄</option>
                                    <option>简约绿</option>
                                    -->
                                    fontOption
                                </select>
                            </div>
                        </div>

                        <div class="layui-form-item">
                            <div class="layui-input-block">
                                <button type="reset" class="layui-btn layui-btn-primary" id="reset">重置</button>
                            </div>
                        </div>
                    </form>
                    <button class="layui-btn layui-btn-fluid" id="fontSetButton">保存</button>
                </fieldset>
            </div>
        </div>
    </div>
</body>
    <script>
    var fontSize
    $("#reset").click();
    layui.use('slider', function(){
        var slider = layui.slider;

        //渲染
        slider.render({
        elem: '#fontSize'  //绑定元素
        ,min:10
        ,max:40
        ,value:initial_fontSize
        ,input:true
        ,change: function(value){
            console.log(value); //动态获取滑块数值
            $('#chapter-402733549').css('font-size',value);
            fontSize = value;
            //setFontSize(value);
            }
         });
    });
    layui.use('slider', function(){
        var slider = layui.slider;

        //渲染
        slider.render({
        elem: '#pageWidth'  //绑定元素
        ,min:600
        ,max:2000
        ,value:initial_pageWidth
        ,input:true
        ,change: function(value){
            $('#j_readMainWrap').css('width',value);
            $('#j_leftBarList').attr('style', 'left:' + document.getElementById("j_chapterBox").offsetLeft + 'px');
            path = $("#j-readPage").attr('path')
    		pageWidth = value;
            }
         });
    });
    </script>;`.replace('styleOption',styleOption);

    setHtml = setHtml.replace('fontOption',fontOption);


    //左侧功能栏点击事件
    var openIndex = layer.open({
        type: 1,
        title:'Liview-Reader',
        skin: 'layui-layer-rim', //加上边框
        area: ['600px', '360px'], //宽高
        content: setHtml
    });
  }//settingFun()结束



//窗口大小改变事件
window.onresize = function(){
        //左侧功能栏重新定位
       $('#j_leftBarList').attr('style', 'left:' + document.getElementById("j_chapterBox").offsetLeft + 'px');
};


//左侧功能栏书页点击事件
$(document).on("click", "#page",function () {
    window.location.href="/";
});

//页面设置保存按钮被点击
$(document).on("click", "#pageSetButton",function () {//页面设置保存按钮被点击
        if("undefined" == typeof fontSize){
                fontSize = null
            }else{
            initial_fontSize = fontSize;
            }
        if("undefined" == typeof pageWidth){
                pageWidth = null
            }else{
            initial_pageWidth = pageWidth;
            }
        path = $("#j-readPage").attr('path')
    	$.post("/bookSet",{path:path,fontSize:fontSize,pageWidth:pageWidth}, function(data) {
    		   console.log('fontsize',fontSize,path);
			});
    });


$(document).on("click", "#styleSetButton",function () {//主题设置保存按钮被点击
        var options=$('#style option:selected')
        styleName = options.text()
        path = $("#j-readPage").attr('path')
    	$.post("/bookSet",{path:path,styleName:styleName}, function(data) {
    		   console.log('styleName',styleName,path);
			});
		settingFun();
		layer.confirm('立即更新主题？', {
            btn: ['更新','稍后'] //按钮
            }, function(){
                    window.location.href="/loadingBook?path=%s".replace('%s',path);
            }, function(){
                    console.log('稍后更新主题');
            });
        });

$(document).on("click", "#fontSetButton",function () {//字体设置保存按钮被点击
        var options=$('#font option:selected')
        fontName = options.text()
        path = $("#j-readPage").attr('path')
    	$.post("/bookSet",{path:path,fontName:fontName}, function(data) {
    		   console.log('styleName',fontName,path);
			});
		settingFun();
		layer.confirm('立即更新字体？', {
            btn: ['更新','稍后'] //按钮
            }, function(){
                    window.location.href="/loadingBook?path=%s".replace('%s',path);
            }, function(){
                    console.log('稍后更新字体');
            });
        });