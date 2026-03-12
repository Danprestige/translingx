fetch("/api/feed/")
.then(res => res.json())
.then(data => {

let container = document.getElementById("feed");

data.forEach(post => {

let div = document.createElement("div");

div.innerHTML = `
<h3>${post.username}</h3>
<p>${post.text}</p>
<p>${post.translated_text}</p>
`;

container.appendChild(div);

});

});