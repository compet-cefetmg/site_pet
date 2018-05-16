$(document).ready(function() {
    $('.table-custom').DataTable({
		language: {
			url: '//cdn.datatables.net/plug-ins/1.10.13/i18n/Portuguese-Brasil.json',
			emptyTable: 'Não há registros'
			},
        searching: false
    });
} );