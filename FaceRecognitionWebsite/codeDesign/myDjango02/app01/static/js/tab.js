window.onload=function(){
	// var a=document.getElementById("a");
	// a.onclick=function(){
	// 	//location.href="index.html";
	// }

	//选项卡逻辑：当前显示其它隐藏

	//获取title值  获取title下面的li
	var titles=document.getElementById("title").getElementsByTagName("li");
	//获取content值  获取content下面的li
	var cons=document.getElementById("content").getElementsByTagName("li");
	//获取长度
	var len=titles.length;
	//获取元素内容
	//console.log(titles[0].innerHTML)

	for(var i=0;i<len;i++){
		//console.log(i)
		titles[i].index=i;
		titles[i].onclick=function(){
			//没有找到当前索引，显示的是最后一个
			//console.log(i);
			for(var j=0;j<len;j++){
				cons[j].style.display="none";
				titles[j].style.background="orange";
				titles[j].style.color="#000";
			}
			//改变当前
			//console.log(this.index)
			cons[this.index].style.display="block";
			titles[this.index].style.background="red";
			titles[this.index].style.color="#fff";
		}
	}

	//点击第2个
	// titles[1].onclick=function(){
	// 	cons[0].style.display="none";
	// 	cons[1].style.display="block";

	// 	titles[1].style.background="red";
	// 	titles[1].style.color="#fff";

	// 	titles[0].style.background="orange";
	// 	titles[0].style.color="#000";
	// }
}