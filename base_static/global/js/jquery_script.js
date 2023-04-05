$(document).ready(function() {
    let dateField = $('#id_date');
    let timeField = $('#id_time');
    let selectedDate = dateField.val();
    dateField.change(function() {
        console.log('date changed', $(this).val());
        selectedDate = $(this).val();
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
            dateField.val(selectedDate);
        });
    });
});