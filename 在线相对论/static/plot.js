$(document).ready(function() {  
    $('#plotBtn').click(function() {  //这行代码为 ID 为 plotBtn 的按钮绑定了一个点击事件处理函数。当按钮被点击时，内部的代码将被执行。
        var speeds = $('#speeds').val();  
        var refSpeed = $('#ref_speed').val();
        var timeRange = $('#time_range').val();  
    //这两行代码分别获取 ID 为 speeds 和 time_range 的输入框的值，并将它们存储在变量 speeds 和 timeRange 中
        $.ajax({  //用于发送异步 HTTP 请求
            type: 'POST',  
            url: '/plot',  
            data: JSON.stringify({ speeds: speeds, time_range: timeRange ,ref_speed: refSpeed }),  //将 speeds 和 timeRange 变量转换为 JSON 字符串，并作为请求的数据发送。
            contentType: 'application/json',  
            success: function(response) {  //当请求成功时，执行这个回调函数。回调函数接收服务器的响应response
                $('#output').attr('src', 'data:image/png;base64,' + response.img_str);  
            },  //并将响应中的 img_str（一个 Base64 编码的图像字符串）设置为 ID 为 output 的元素的 src 属性，从而显示图像。
            error: function(error) {  
                console.error('Error:', error);  
            }  //当请求失败时，执行这个回调函数。回调函数接收错误信息 error，并在控制台输出错误信息
        });  
    });  
});

