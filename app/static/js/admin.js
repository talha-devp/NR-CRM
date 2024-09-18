$(document).ready(function () {
    // Logout functionality
    $('#logoutBtn').on('click', function () {
        $.ajax({
            url: '/admin/logout',
            type: 'POST',
            success: function () {
                window.location.href = '/';
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
                alert('Çıkış yapılamadı. Lütfen tekrar deneyin.');
            }
        });
    });

    // Open add form element modal
    $('#addFormElementBtn').on('click', function () {
        $('#addFormElementModal').modal('show');
    });

    // Handle form submission for adding a new form element
    $('#addFormElementForm').on('submit', function (e) {
        e.preventDefault();

        const name = $('#elementName').val();
        const inputType = $('#inputType').val();

        $.ajax({
            url: '/admin/element/add',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ name: name, input_type: inputType }),
            success: function (response) {
                addMessage(response);
                if (response.success) {
                    $('#addFormElementModal').modal('hide');
                    // Optionally reload the page or refresh the table
                    location.reload();
                }
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
                alert('Form elemanı eklenirken bir hata oluştu.');
            }
        });
    });

    // Handle delete button click
    $('#viewAllElementsForm').on('click', '.delete-btn', function () {
        if (confirm('Bu ürünü silmek istediğinize emin misiniz?')) {
            deleteElement($(this).data('id'));
        }
    });

    function deleteElement(id) {
        $.ajax({
            url: `/admin/element/delete/${id}`,
            type: 'DELETE',
            success: function (response) {
                if (response.success) {
                    // Refresh the page or reload the table if needed
                    location.reload();
                }
                addMessage(response);
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
                alert('Ürün silinirken bir hata oluştu.');
            }
        });
    }

    function addMessage(response) {
        $('#addResultMessage').html(`<div class="alert alert-${response.success ? 'success' : 'danger'}">${response.message}</div>`).fadeIn().delay(1000).fadeOut();
    }
});
