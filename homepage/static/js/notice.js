var msg = '<div class=\"header\"><a id=\"close\" href="#">close X</a></div>';
    msg += '<ul><div><h2 id=\"topic\">Important Notice</h2></div><br>';
	msg += '<li>converse.com will not be liable for any content authored by individual.</li><hr>';
	msg += '<li>converse.com abhor enthnocentric content, hate speech, racism and ethnic bashing.</li><hr>';
	msg += '<li>Discussions by Forum members should be devoid of abuses. </li></ul>';
	
//Adding this message to the page
var page = document.getElementById("notice");
var elNote = document.createElement('div');
    elNote.setAttribute('id', 'note');
	
	elNote.innerHTML = msg;
	page.appendChild(elNote);
	
//function to close the notification
function dismissNote(){
    document.getElementById("note").style.display="none";
	}
	
//Adding the event to the function
var elClose = document.getElementById('close');
    elClose.addEventListener('click', dismissNote, false);
