(() => {
    window.addEventListener("beforeunload", function(event) {
        fetch(clearSessionUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            }
        });
    });
})();

(() => {
    const forms = document.querySelectorAll('.form-delete');
    for (const form of forms) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            let confirmed;
            if (currentLanguage == 'pt-br' || currentLanguage == 'pt_br') {
                confirmed = confirm('Tem certeza que deseja cancelar a consulta?');
            } else {
                confirmed = confirm('Are you sure you want to cancel the appointment?');
            }
            if(confirmed) {
                form.submit();
            }
        });
    }
})();