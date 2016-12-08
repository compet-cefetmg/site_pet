

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

});
