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
    let dateField = $('#id_date');
    let timeField = $('#id_time');
    let firstDate = $(this).val()
    dateField.change(function() {
        console.log('date changed', $(this).val());
        let selectedDate = $(this).val();
        $.get('/schedule/app_times/', {date: selectedDate}, function(data) {
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
        console.log('time changed', $(this).val());
        let selectedTime = $(this).val();
        $.get('/schedule/app_dates/', {time: selectedTime}, function(data) {
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