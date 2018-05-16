$(function() {
	$('.calendar').datepicker({ // Classe calendário será um datepicker
		changeMonth:true, // Possibilita a modificação de mês de maneira simples
		changeYear: true, // Possibilita a modificação de ano de maneira simples
		yearRange: '2000:' + new Date().getFullYear(), // Especifica o período dos anos
		dateFormat: 'dd/mm/yy'})
});

function showDialog(){
	var calendar = $('#leave_date').val();
	if(calendar){
		$('#text-position').html('Preencher o campo Data de saída <b>impede</b> seu acesso a conta nesse site, ou seja, seu cadastro servirá apenas para registro documental. Deseja continuar?');
		$('#popUp').modal('show');
	}else{
		$('#form').submit();
	}
}

$(function(){
    $('#close').click(function() {
       $('#popUp').modal('hide'); 
    });

    $('#link').click(function() {
    	$('#popUp').modal('hide');
        $('#form').submit();
    });
});