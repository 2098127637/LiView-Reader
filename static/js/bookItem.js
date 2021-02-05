$(document).on("click", "#readButton",function () {
    if($(this).attr('new') == "True"){
        newBook(this);
    }else{
        read($(this).attr('path'));
    }
});
/*var upload = `
            <div class="layui-upload" >
                <button type="button" class="layui-btn layui-btn-fluid" id="uploadTXTButton">
                    <i class="layui-icon">&#xe67c;</i>上传文件
                </button>
                <nobr id="demoText"></nobr>
            </div>`*/
var upload = `
            <div class="layui-upload-drag" id="uploadTXTButton" path = str0>
                <i class="layui-icon"></i>
                <p>点击上传，或将文件拖拽到此处</p>
                <div class="layui-hide" id="uploadDemoView">
                    <hr>
                    <img src="" alt="上传成功后渲染" style="width: 300px">
                </div>
            </div>
            <script>
              //拖拽上传
                layui.use('upload', function(){
                console.log(this)
                    var $ = layui.jquery
                        ,upload = layui.upload;
                    layui.upload;
                    upload.render({
                        elem: '#uploadTXTButton'
                        ,accept:'file'
                        ,exts: 'txt'
                        ,url: '/uploadTXT' //改成您自己的上传接口
                        ,data:{
                                path:function(){ return $('#uploadTXTButton').attr('path');}
                              }
                        ,done: function(data){
                            //上传完毕回调
                            if (data['success']==true){

                                window.location.href="/";
                            }else{
                                layer.msg(data['success'], {
                                offset: '6px'
                             });
                            }
                        }
                        ,error: function(){
                            //请求异常回调
                            //演示失败状态，并实现重传
                            layer.msg('异常，上传失败！', {
                                offset: '6px'
                                });
                               }
                        });
                     });

            </script>
            `
function newBook(arg){
    var path = $(arg).attr('path');
    console.log(upload.replace('str0',path));
    layer.open({
        type: 1,
        title:'上传TXT',
        skin: 'layui-layer-rim', //加上边框
        area: ['250px', '200px'], //宽高
        content: upload.replace('str0',path)
});
}

function read(path){
    //window.location.href="/loadingBook?path=%s".replace('%s',path);
    window.open("/loadingBook?path=%s".replace('%s',path));
}