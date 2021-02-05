layui.use(['form', 'layedit', 'laydate','upload'], function(){
  var form = layui.form
  ,layer = layui.layer
  ,layedit = layui.layedit
  ,laydate = layui.laydate;
  var name = layui.upload;
  var upload = layui.upload;

  var type ='';//书籍类型
  var novelName;//书籍名称
  var switchButton;//开关
  switchButton = true;
  //执行实例
  var uploadInst = upload.render({
    elem: '#uploadPicButton' //绑定元素
    ,url: '/addBook' //上传接口
    ,acceptMime: 'image/jpg, image/png'//（只显示 jpg 和 png 文件）
    ,data:{
            name:function(){return document.getElementById("name").value;},
            type:function(){var options=$('#type option:selected'); return options.text()},
            switchButton:function(){return switchButton;}
        }
    ,auto:false
    ,bindAction:'#submitBUtton'
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
      var demoText = $('#demoText');
      demoText.html('<span style="color: #FF5722;">上传失败</span>');
    }
  });
  form.on('switch(switchTest)', function(data){
    if(this.checked ? true : false){
        layer.msg('评论：开', {
            offset: '6px'
        });
    }else{
        layer.msg('评论：关', {
        offset: '6px'
        });
    }
    switchButton = (this.checked ? true : false)
  });
});
/*
<div class="layui-form-item">
                    <label class="layui-form-label">TXT文件</label>

                    <div class="layui-upload">
                            <button type="button" class="layui-btn" id="uploadTXTButton">
                            <i class="layui-icon">&#xe67c;</i>上传TXT文档
                            </button>
                            <nobr id="demoText"></nobr>
                    </div>
                </div>
*/

