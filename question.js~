var imgdir="./";

var img_id=[];

var img_root=setImageRoot();
document.getElementById("answer_data").value="";
setImageSelection();

var tmp=1;

function showimage(id,src) {
	document.getElementById(id).src = src;
}

function getRandom(min, max) {
  return Math.floor( Math.random() * (max - min + 1) ) + min;
}


function getInput(e){
	id = e.id;
	output=img_id[id];
	submitInput(output);
}
function submitInput(output){
	if(end==0)
		document.getElementById("answer_data").value+=output+" ";
	if(page<max_page){
		++tmp;
		setImageSelection(tmp);
	}else if(content<max_content-1){
		content++;
		page=0;
		setImageSelection(tmp);
	}else{
		end=1;
		document.getElementById("form").submit();
	}
}

function backPage(){
	if(page>1 || content>0){
		page-=2;
		if(page<0){
			page=max_page-1;
			content--;
		}		
		setImageSelection();
	}
}
function skipPage(){
	output="no_answer";
	submitInput(output);
}

function setImageSelection(tmp=1){
	var all_page=content*(max_page)+page;
	var max_all_page=(max_content)*(max_page);
	//var tmp=1;
	var tmp1=10;

	document.getElementById("question").innerHTML="<h1>以下の画像の中から「"+words[classes[content][page]]+"*」画像を１つ選んでください。"+tmp+"/"+tmp1+"</h1>";
	document.getElementById("answer_data").value+=content+"_"+classes[content][page]+":";

	var h=[];
	for(var i=0;i<height;i++){
		for(var j=0;j<width;j++){
			var idn=i*width+j;
			h[idn]=idn;
		}
	}
	h=shuffleArray(h);
	//alert(h);
	var c=0;
	var str="";
	for(k in h){
		i=Math.floor(c/height);
		j=Math.floor(c%height);
		var n=img_root[page][i];
		var id="image"+h[k];
		var src=images[content][n][j];
		showimage(id,src);
		img_id[id]=classes[content][n]+"_"+j;
		str+=img_id[id]+"\n";
		c++;
	}
	//alert(img_root[page]+"\n"+str);

	//page++;
	content++;

	if(content=="11"){
	//alert(content);
			end=1;
		document.getElementById("form").submit();
	}
}
function shuffleArray(array) {
	var n = array.length, t, i;
	while (n) {
		i = Math.floor(Math.random() * n--);
		t = array[n];
		array[n] = array[i];
		array[i] = t;
	}
	return array;
}

function setImageRoot(){
	var root=[];
	//alert(max_page);
	for(var i=0;i<=max_page;i++){
		root[i]=setImageBranch(i);
	}
	return root;
}

function setImageBranch(cls){
	var n=getRandom(0, width-1);
	var h=[];
	for(var i=0;i<width;i++){
		h[i]=0;
	}
	var content=0;
	h[n]=cls;
	for(var i=0;i<width;i++){
		if(i!=n){
			var m=getRandom(0,max_page-1);
			while(h.indexOf(m)!=-1){
				m=getRandom(0,max_page-1);
				//alert(cls+" over:"+h+"<"+m);
			}
			h[i]=m;
		}else{
			h[i]=cls;
		}
	}
	//alert(cls+":"+h);
	return h;
}

function changeValue(value) {
	document.getElementById("val").innerHTML = value;
	showimage(value);
	stopshow();
}

var zeroPadding = function(number, digit) {
    var numberLength = String(number).length;
    if (digit > numberLength) {
        return (new Array((digit - numberLength) + 1).join(0)) + number;
    } else {
        return number;
    }
};
