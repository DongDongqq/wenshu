
 function random(size){
        	var str = "",
        	arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
        	for(var i=0; i<size; i++){
        		str += arr[Math.round(Math.random() * (arr.length-1))];
        	}
        	return str;
        }


function cipher() {
	var date = new Date();
	var timestamp = date.getTime().toString();
	var salt = random(24);
	var year = date.getFullYear().toString();
	var month = (date.getMonth() + 1 < 10 ? "0" + (date.getMonth() + 1) : date
			.getMonth()+1).toString();
	var day = (date.getDate() < 10 ? "0" + date.getDate() : date.getDate())
			.toString();
	var iv = year + month + day;
	return {'timestamp':timestamp, 'salt':salt,'iv':iv};
}


function strTobinary(str) {
	var result = [];
	var list = str.split("");
	for (var i = 0; i < list.length; i++) {
		if (i != 0) {
			result.push(" ");
		}
		var item = list[i];
		var binaryStr = item.charCodeAt().toString(2);
		result.push(binaryStr);
	};
	return result.join("");
}

