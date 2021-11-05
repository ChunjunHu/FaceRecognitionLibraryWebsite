// /*
// * 调用摄像头
// */
// function call_camera(){
//     var video=document.getElementById("video");    
//     var errocb=function(){  
//         console.log("sth srong");  
//     }  
//     //调用电脑摄像头并将画面显示在网页  
//     if(navigator.getUserMedia){  
//         navigator.getUserMedia({"video":true},function(stream){  
//             video.src=stream;  
//             video.play();  
//         },errocb);  
//     }else if(navigator.webkitGetUserMedia){  
//         navigator.webkitGetUserMedia({"video":true},function(stream){  
//             //video.src=window.webkitURL.createObjectURL(stream);
//             video.src=window.URL.createObjectURL(stream);  
//             video.play();  
//         },errocb);  
//     }
// }

var exArray = []; //存储设备源ID
// 调用资源开启摄像头
function call_camera() {  
    if (navigator.getUserMedia) {  
        navigator.getUserMedia({  
            'video': {  
                'optional': [{  
                    'sourceId': exArray[0] //0为前置摄像头，1为后置  
                }]  
            } 
        }, successFunc, errorFunc);    //success是获取成功的回调函数  
    }else {  
        alert('Native device media streaming (getUserMedia) not supported in this browser.');  
    }
}
      
// 成功后执行的函数
function successFunc(stream) {  
    //alert('Succeed to get media!');  
    if (video.mozSrcObject !== undefined) {  
        //Firefox中，video.mozSrcObject最初为null，而不是未定义的，我们可以靠这个来检测Firefox的支持  
        video.mozSrcObject = stream;  
    }  else {  
        video.src = window.URL && window.URL.createObjectURL(stream) || stream;  
    }            
} 
// 失败后执行的函数
function errorFunc(e) {  
    alert('Error！'+e);  
}
      
// 将视频帧绘制到Canvas对象上
function drawVideoAtCanvas(video,context) {  
    context.drawImage(video, 0, 0,90,120);
}