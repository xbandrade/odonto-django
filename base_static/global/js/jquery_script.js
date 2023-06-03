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
                    text: time,
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
                let originalDate = date[0];
                let formattedDate = date[1];
                dateField.append($('<option>', {
                    value: originalDate,
                    text: formattedDate,
                }));
            });
            dateField.val(selectedDate);
        });
    });
    setTimeout(function() {
        dateField.val("03-08-2023").trigger('change');
        console.log("Here");
    }, 0);
});