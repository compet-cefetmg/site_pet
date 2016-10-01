$(function() {
    $('.panel-body a i.fa.fa-envelope-o').mouseover(function() {
        $(this)
            .addClass('fa-envelope')
            .removeClass('fa-envelope-o');
    });

    $('.panel-body a i.fa.fa-envelope-o').mouseout(function() {
        $(this)
            .addClass('fa-envelope-o')
            .removeClass('fa-envelope');
    });
});