function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
  }
  
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }

  document.addEventListener('keydown', function(event) {
    // Vérifie si la touche appuyée est la touche "a"
    if (event.key === 'a') {
      // Envoie une requête POST à l'URL '/appeler_fonction'
      fetch('/appeler_fonction', {
        method: 'POST'
      });
    }
  });


  