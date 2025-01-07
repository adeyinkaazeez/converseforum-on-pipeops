var today = new Date();
var year = today.getFullYear();

var est = new Date('Apr 01, 2023 15:45:55');
var difference = today.getTime() - est.getTime();
difference = (difference/31556900000);

var el = document.getElementById('copyrightt');
    el.innerHTML = '<P> Copyright &copy;' + year  + ' ' + '-' +  'All right reserved by Converse' + '</p>';
	                  
	
var elest = document.getElementById('estt');
    elest.textContent = Math.floor(difference) + 'Year of online publishing';