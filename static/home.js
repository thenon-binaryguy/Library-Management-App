

function submitted(event) {
    const f = document.getElementById('formsearch');
    const q = document.getElementById('search-input');
const base = 'http://127.0.0.1:8000/search?q=';
        event.preventDefault();
        const url = base + q.value;
        const win = window.open(url,"_blank");
        win.focus();
      }
f.addEventListener('submit', submitted);
