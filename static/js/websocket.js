const socket = new WebSocket(
"ws://localhost:8000/ws/translate/global/"
);

socket.onmessage = function(event){

const data = JSON.parse(event.data)

document.getElementById("chat").innerHTML +=
"<p>"+data.message+"</p>"

}

function sendMessage(){

const msg = document.getElementById("message").value

const lang = document.getElementById("language").value

socket.send(JSON.stringify({

text: msg,
language: lang

}))

}