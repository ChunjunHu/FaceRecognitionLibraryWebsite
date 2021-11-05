// 定义函数实现Ajax照片上传服务器
function photo_ajax(){
    // 获取Canvas中的图片数据
    var image_data = document.getElementById("canvas").toDataURL();
    // 截取前22个字符（前22个字符为base64的图像编码）
    image_data = image_data.substring(22);
    // 将数据转换成json数据格式{"data": base64json字符串}
    var data = {data: JSON.stringify({"data": image_data}),}
    console.log(data)  // 测试浏览器日志输出    
    // JQuery Ajax提交数据
    $.ajax({
        url: "/face_sluice/upload", // 提交地址
        type: "post", // 提交方式
        headers:{"X-CSRFToken":$.cookie("csrftoken")}, // 获取cookies中的csrftoken一并提交服务器
        dataType: "json", // 提交数据类型
        data: data, // 提交数据
        success: function(res){ // 提交成功后接受服务器返回数据,自动保存在res参数中
            console.log(res);  // 测试浏览器日志输出
            alert(res["result"]["age"]); // 网页弹出响应结果对话框
        }
    });
}