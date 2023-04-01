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