function initBlogDataTable() {
    var table = $('#posts').DataTable({
        'sAjaxSource': '/blog/all',
        'dom': 'ft',
        'language': {
            'url': 'https://cdn.datatables.net/plug-ins/1.10.13/i18n/Portuguese-Brasil.json'
        },
        'columnDefs': [
            {
                "targets": 1,
                "data": null,
                'render': function (data, type, row, meta) {
                    var postLink = $($.parseHTML('<a></a>'));
                    postLink.attr('href', '/blog/' + data[0])
                    postLink.html(data[1])
                    return postLink[0].outerHTML;
                }
            },
            {
                "targets": 3,
                "data": null,
                'render': function (data, type, row, meta) {
                    var editPostBtn = $($.parseHTML('<a></a>'));
                    editPostBtn
                        .attr('href', '/blog/' + data[0] + '/edit')
                        .attr('title', 'Editar post')
                        .addClass('edit-btn')
                        .append($.parseHTML('<i class="fa fa-pencil"></i>'));
                    var deletePostBtn = $($.parseHTML('<a></a>'));
                    deletePostBtn
                        .attr('title', 'Remover post')
                        .attr('href', '#')
                        .addClass('remove-btn')
                        .append($.parseHTML('<i class="fa fa-trash-o"></i>'));
                    return data[3] + editPostBtn[0].outerHTML + deletePostBtn[0].outerHTML;
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
                .attr('href', '/blog/' + 'add');
            addBtn.appendTo($('#posts_filter'))
        }
    });

    $('#posts tbody').on('click', '.remove-btn', function() {
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
                url: '/blog/delete/',
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
