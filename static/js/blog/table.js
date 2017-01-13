function initBlogDataTable(tableId, urlPrefix) {
    var table = $('#'+tableId).DataTable({
        'sAjaxSource': urlPrefix + 'all',
        'dom': 'ft',
        'language': {
            'url': 'https://cdn.datatables.net/plug-ins/1.10.13/i18n/Portuguese-Brasil.json'
        },
        'columnDefs': [
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
            },
            {
                "targets": 0,
                "visible": false,
                "searchable": false
            }  
        ],
        initComplete: function(){
            var addBtn = $($.parseHTML('<a>Adicionar</a>'));
            addBtn
                .addClass('btn btn-primary add-btn')
                .attr('href', urlPrefix + 'add');
            addBtn.appendTo($('#'+tableId+'_filter'))
        }
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
                type: 'POST',
                data: {'id': data[0]},
                url: urlPrefix + 'delete/',
                success: function() {
                    swal('Sucesso!', 'Removido com sucesso.', 'success');
                    table.ajax.reload();
                },
                error: function() {
                    swal('Erro!', 'Não foi possível remover.', 'error');
                }
            });
        });
    });
}
