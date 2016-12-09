function initDataTable(tableId, urlPrefix) {
    var table = $('#'+tableId).DataTable({
        'sAjaxSource': urlPrefix + 'all',
        'dom': 'ftp',
        'language': {
            'url': 'https://cdn.datatables.net/plug-ins/1.10.13/i18n/Portuguese-Brasil.json'
        },
        // Renders title row with anchor tag
        'columnDefs': [
        // Renders edit and remove buttons
            {
                "targets": -1,
                "data": null,
                'render': function (data, type, row, meta) {
                    return `
                        <button class="btn btn-xs btn-primary edit-btn" class="edit-btn">
                            <i class="fa fa-pencil"></i> Editar
                        </button>
                        <button class="btn btn-xs btn-danger remove-btn">
                            <i class="fa fa-trash"></i> Remover
                        </button>
                        `;
                }
            }
        ]
    });

    $('#'+tableId +' tbody').on('click', '.edit-btn', function() {
        var data = table.row($(this).parents('tr')).data();
        window.location.href = urlPrefix + data[0] + '/edit';
    });

    $('#'+tableId +' tbody').on('click', '.remove-btn', function() {
        var data = table.row($(this).parents('tr')).data();
        swal({
            'type': 'warning',
            'title': 'Atenção!',
            'text': 'Você tem certeza disso?',
            showCancelButton: true,
            confirmButtonText: 'Sim, remover!',
            confirmButtonColor: '#DD6B55',
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        }, function() {
            $.ajax({
                type: 'DELETE',
                data: data[0],
                url: urlPrefix + 'delete',
                sucess: function() {
                    swal('Sucesso!', 'Removido com sucesso.', 'success');
                },
                error: function() {
                    swal('Erro!', 'Não foi possível remover.', 'error');
                }
            });
        });
    });
}

$(function() {
    initDataTable('tutors', '/members/tutor/');
})
