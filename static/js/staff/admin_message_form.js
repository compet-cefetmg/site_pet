$(function() {
    $('form select').select2({'multiple': true, 'language': 'pt-BR'});

    $('form').submit(function(){
        $('form').fadeOut();
        $('.loading').fadeIn();
    });
});
