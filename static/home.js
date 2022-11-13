

function searched() {   
  var q = document.getElementById('search-input').innerHTML;
    console.log(q)
    const base = 'http://127.0.0.1:8000/search?q=percy';
        const url = base ;
        const win = window.open(url,"_blank");
        win.focus();
      }
