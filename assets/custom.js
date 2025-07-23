const observer = new MutationObserver(() => {
    const toggleBtn = document.querySelector('button.show-hide');
    if (toggleBtn && toggleBtn.innerHTML !== 'Colunas') {
        toggleBtn.innerHTML = "Colunas";
    }
});

observer.observe(document.body, { childList: true, subtree: true });