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


$(document).ready(function() {
    console.log('Date and Time dropdowns');
    let dateField = $('#id_date');
    let timeField = $('#id_time');
    dateField.change(function() {
        let selectedDate = $(this).val();
        $.get('/app_times/', {date: selectedDate}, function(data) {
            timeField.empty();
            $.each(data.available_times, function(index, time) {
                timeField.append($('<option>', {
                    value: time,
                    text: time
                }));
            });
        });
    });
    timeField.change(function() {
        let selectedTime = $(this).val();
        $.get('/app_dates/', {time: selectedTime}, function(data) {
            dateField.empty();
            $.each(data.available_dates, function(index, date) {
                dateField.append($('<option>', {
                    value: date,
                    text: date
                }));
            });
        });
    });
});