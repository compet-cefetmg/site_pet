$(document).ready(function() {

    var eventsJson = [];
    events.forEach(function(event) {
        eventsJson.push({
            'start' : event[0], 
            'end': event[1],
            'title': event[2],
            'backgroundColor': event[3],
            'borderColor': event[3],
            'url': event[4]
        });
    });

    // Inits calendar
    $('#calendar').fullCalendar({
//        dayRender: function (date, cell) {
//            var today = new Date();
//            var cellDate = new Date(date);

//            if (cellDate.getDate()+1 === today.getDate() && cellDate.getMonth() === today.getMonth()){
//                cell.css("background-color", "orange");
//            }
//        },
        header: {
            left: 'title',
            center: 'pt-br',
            right:  'today, prev, next'
        },
        timeFormat: 'H:mm',
        locale: 'pt-br',
        height: 500,
        events: eventsJson,
    });
});