/////get questions and answers from database
// const api_url = 'http://192.168.0.5:5000/api/';
// async function getQapi() {
// 	const response = await fetch(api_url);
// 	const data = await response.json();
// 	console.log(data);
// 	console.log(data.questions.length);

// 	for (var i = 0; i < data.questions.length; i++) {
// 		var question = data.questions[i];
// 		console.log(question);
// 		var phaslo = new Array(i)
// 		phaslo[i] = data.questions[i].answer;
// 	}
// }
// getQapi();
/////////////////////////////////////////////////////////////
var request = new XMLHttpRequest(),
	method = 'GET',
	url = 'http://192.168.0.5:5000/api/'
async = true;
request.open(method, url, async);
request.onload = function () {
	var data = JSON.parse(this.response);
	console.log(data.questions.length + ' nowe');
	if (request.status >= 200 && request.status < 400) {

		var phaslo = new Array()

		for (var i = 0; i < data.questions.length; i++) {
			var row = data.questions[i];
			phaslo.push(row);
			console.log(row.question + ' ' + row.answer + ' ' + row.week);
			console.log(phaslo[i].question)
		}
		//console.log(phaslo);
		// 	} else {
		// 		console.log('error');
		// 	}
		// }
		// request.send();
		/////////////////////////////////////////////////////////////
		var numer = Math.floor(Math.random() * data.questions.length) - 1;
		numer++; if (numer > data.questions.length) numer = 0;

		var password = phaslo[numer].answer;
		var question1 = phaslo[numer].question;
		/////////////////////////////////////////////////////////

		//document.getElementById("question").innerHTML = question11;
		//set up match.random
		//put the answer into variable 'password'

		/////////////////////////////////////////////////////////
		//var password = "example answer";
		password = password.toUpperCase();

		var lenght = password.length;
		var errors_number = 0;
		// add sound
		// var yes = new Audio("yes.wav");
		// var no = new Audio("no.wav");

		var password1 = "";

		for (i = 0; i < lenght; i++) {
			if (password.charAt(i) == " ") password1 = password1 + " ";
			else password1 = password1 + "-";
		}

		function write_password() {
			document.getElementById("lettersandnumbers").innerHTML = password1;
			document.getElementById("question").innerHTML = question1;
		}

		window.onload = start;

		var letters = new Array(35);

		letters[0] = "A";
		letters[1] = "B";
		letters[2] = "C";
		letters[3] = "D";
		letters[4] = "E";
		letters[5] = "F";
		letters[6] = "G";
		letters[7] = "H";
		letters[8] = "I";
		letters[9] = "J";
		letters[10] = "K";
		letters[11] = "L";
		letters[12] = "M";
		letters[13] = "N";
		letters[14] = "O";
		letters[15] = "P";
		letters[16] = "Q";
		letters[17] = "R";
		letters[18] = "S";
		letters[19] = "T";
		letters[20] = "U";
		letters[21] = "V";
		letters[22] = "W";
		letters[23] = "X";
		letters[24] = "Y";
		letters[25] = "Z";
		letters[26] = "1";
		letters[27] = "2";
		letters[28] = "3";
		letters[29] = "4";
		letters[30] = "5";
		letters[31] = "6";
		letters[32] = "7";
		letters[33] = "8";
		letters[34] = "9";
		letters[35] = "0";

		//24 

		function start() {

			var divs_content = "";

			for (i = 0; i <= 35; i++) {
				var element = "lit" + i;
				divs_content = divs_content + '<div class="litera" onclick="sprawdz(' + i + ')" id="' + element + '">' + letters[i] + '</div>';
				if ((i + 1) % 9 == 0) divs_content = divs_content + '<div style="clear:both;"></div>';
			}

			document.getElementById("alfabet").innerHTML = divs_content;


			write_password();
		}

		String.prototype.ustawZnak = function (miejsce, znak) {
			if (miejsce > this.length - 1) return this.toString();
			else return this.substr(0, miejsce) + znak + this.substr(miejsce + 1);
		}


		function sprawdz(nr) {

			var trafiona = false;

			for (i = 0; i < lenght; i++) {
				if (password.charAt(i) == letters[nr]) {
					password1 = password1.ustawZnak(i, letters[nr]);
					trafiona = true;
				}
			}

			if (trafiona == true) {
				// yes.play();
				var element = "lit" + nr;
				document.getElementById(element).style.background = "#f8f9fa";
				document.getElementById(element).style.color = "#ef920c";
				document.getElementById(element).style.border = "3px solid #ef920c";
				document.getElementById(element).style.cursor = "default";

				write_password();
			}
			else {
				// no.play();
				var element = "lit" + nr;
				document.getElementById(element).style.background = "#cccccc";
				document.getElementById(element).style.color = "#fff";
				document.getElementById(element).style.border = "3px solid #fff";
				document.getElementById(element).style.cursor = "default";
				document.getElementById(element).setAttribute("onclick", ";");

				//wrong answer
				errors_number++;
				var picture = "img/s" + errors_number + ".png";
				document.getElementById("stars").innerHTML = '<img src="static/' + picture + '" alt="" />';
			}

			//Correct
			if (password == password1)
				document.getElementById("alfabet").innerHTML = 'Yes, that is correct! <br/><br /><br /><span class="reset" onclick="location.reload()">Next Question</span>';

			//Incorrect
			if (errors_number >= 9)
				document.getElementById("alfabet").innerHTML = "Game Over! Correct answer is: <br/>" + password + '<br /><br /><span class="reset" onclick="location.reload()">Next Question</span>';
		}

	} else {
		console.log('error');
	}
}
request.send();