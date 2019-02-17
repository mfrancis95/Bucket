$(document).ready(() => {
    const table = $('#table').DataTable({
        columnDefs: [{
            className: 'select-checkbox',
            orderable: false,
            targets: 0
        }],
        select: {
            selector: 'td:first-child',
            style: 'os'
        }
    });
    let selected = [];
    $('#copy-modal').on('show.bs.modal', () => {
        selected = $.map(table.rows({selected: true}).data(), row => row[1]);
        $('#copy-objects').html(selected.map(key => `<p>${key}</p>`));
    });
    $('#copy').click(() => {
        $.ajax({
            contentType: 'application/json',
            data: JSON.stringify(selected),
            failure: data => $('#copy-modal').modal('hide'),
            success: data => location.reload(),
            type: 'POST',
            url: '/copy'
        });
    });
});