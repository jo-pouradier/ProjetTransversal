function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}
  
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

// let lastJson = {};
// let jsonData = event.key;
// if (JSON.stringify(jsonData) !== '{}' || JSON.stringify(lastJSON) !== '{}'){
document.addEventListener('keydown', function(event) {
  // Envoie une requête POST à l'URL '/appeler_fonction'
  // on peut envoyer plusieurs fois la meme commande 
  var xhr = new XMLHttpRequest();
  var url = '/deplacements';
  xhr.open("POST",url,true);
  xhr.setRequestHeader('Content-Type','application/json');
  var send_data = {key:event.key};
  xhr.send(JSON.stringify(send_data));
  lastJson = jsonData;
});
