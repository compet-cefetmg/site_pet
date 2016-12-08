

$(function() {
    var table = $('#posts').DataTable({
        'sAjaxSource': '/blog/all',
        'dom': 'ftp',
        'language': {
            'url': 'https://cdn.datatables.net/plug-ins/1.10.13/i18n/Portuguese-Brasil.json'
        },
        // Renders title row with anchor tag
        'columnDefs': [
            {
                'targets': 1,
                'render': function (data, type, row, meta) {
                    return '<a href="/blog/post/' + row[0] + '">' + data + '</a>';
                }
            },
        // Renders edit and remove buttons
            {
                "targets": -1,
                "data": null,
                'render': function (data, type, row, meta) {
                    return `
                        <button class="btn btn-xs btn-primary edit-btn" class="edit-btn">
                            <i class="fa fa-pencil"></i> Editar
                        </button>
                        <button class="btn btn-xs btn-danger remove-btn"href="/blog/post/' + row[0] + '/delete">
                            <i class="fa fa-trash"></i> Remover
                        </button>
                        `;
                }
            }
        ]
    });

    $('#posts tbody').on('click', '.edit-btn', function() {
        var data = table.row($(this).parents('tr')).data();
        window.location.href = '/blog/post/' + data[0] + '/edit';
    });

    $('#posts tbody').on('click', '.remove-btn', function() {
        var data = table.row($(this).parents('tr')).data();
        swal({
            'type': 'warning',
            'title': 'Atenção!',
            'text': 'Tem certeza que deseja remover o post "' + data[1] + '"?',
            showCancelButton: true,
            confirmButtonText: 'Sim, remover!',
            confirmButtonColor: '#DD6B55',
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        }, function() {
            $.ajax({
                type: 'DELETE',
                data: data[0],
                url: '/blog/post/delete',
                sucess: function() {
                    swal('Sucesso!', 'O post selecionado foi removido com sucesso.', 'success');
                },
                error: function() {
                    swal('Erro!', 'Não foi possível remover o post selecionado.', 'error');
                }
            });
        });
    });

});
