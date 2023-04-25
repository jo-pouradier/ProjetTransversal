function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
  }
  
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }

  document.addEventListener('keydown', function(event) {
    // Envoie une requête POST à l'URL '/appeler_fonction'
    var xhr = new XMLHttpRequest();
    var url = '/deplacements';
    xhr.open("POST",url,true);
    xhr.setRequestHeader('Content-Type','application/json');
    var send_data = {key:event.key};
    xhr.send(JSON.stringify(send_data));
  

    //fetch('/appeler_fonction', {
      //  method: 'POST' ,
        //headers: {
          //"key": event.key
          // 'Content-Type': 'application/x-www-form-urlencoded',
        //},
      //});
  });

  
  const touchElement = document.getElementById('touch-element');
  touchElement.addEventListener('touchend', handleToucheEnd);
  function handleToucheEnd(event) {
    const touches = event.touches.length;
    if (touches === 0){
        console.log("no touch press, stop all")
        var xhr = new XMLHttpRequest();
        var url = '/stop';
        xhr.open("POST",url,true);
        xhr.setRequestHeader('Content-Type','application/json');
        var send_data = {key:event.key};
        xhr.send(JSON.stringify(send_data));
  
    }

  }