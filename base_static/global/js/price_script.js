window.onload = function() {
    const procedureField = document.getElementById('procedure');
    const priceField = document.getElementById('price');

    if (priceField){
        procedureField.addEventListener('change', () => {
            const selectedProcedure = procedureField.options[procedureField.selectedIndex];
            const procedureId = selectedProcedure.value;
            fetch(`/schedule/get_price/${procedureId}/`)
                .then(response => response.json())
                .then(data => {
                    const price = data.price;
                    const formatter = new Intl.NumberFormat('pt-BR', {style: 'currency', currency: 'BRL'});
                    const formattedPrice = formatter.format(price);
                    console.log(selectedProcedure, formattedPrice);
                    priceField.value = formattedPrice;
                });
        });
    }
};