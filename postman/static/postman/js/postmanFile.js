var listItems = document.querySelectorAll('li');
var i;

for(i = 0; i<listItems.length; i++){
	if(i % 2 == 0){
		listItems[i].className = 'cool';
	} else {
		listItems[i].className = 'complete';
	}
}
		


