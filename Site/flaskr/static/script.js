function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}
  
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

document.addEventListener('keydown', function(event) {
  // Envoie une requête POST à l'URL '/appeler_fonction'
  // on peut envoyer plusieurs fois la meme commande 
  var xhr = new XMLHttpRequest();
  var url = '/commandes';
  xhr.open("POST",url,true);
  xhr.setRequestHeader('Content-Type','application/json');
  var send_data = {};
  send_data["key"] = event.key
  console.log(send_data)
  xhr.send(JSON.stringify(send_data));
});
