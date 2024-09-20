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

    // Element name update ajax
    function updateElementName(id, newName) {
        $.ajax({
            url: `/admin/element/${id}/update-name`,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify({ name: newName }),
            success: function (response) {
                addMessage(response);
                if (response.success) {
                    console.log('Element name updated successfully.');
                }
            },
            error: function (xhr, status, error) {
                console.error('Error updating element name:', error);
                alert('Error updating element name. Please try again.');
            }
        });
    }

    // Event listener for name change
    $('#viewAllElementsForm').on('change', '.element-name-input', function () {
        const elementId = $(this).data('id');  // Assuming the input has a data-id attribute with the element ID
        const newName = $(this).val();

        if (newName.trim() !== "") {
            updateElementName(elementId, newName);
        } else {
            alert('Name cannot be empty.');
        }
    });

    // Open add form element modal
    $('#addFormElementBtn').on('click', function () {
        $('#addFormElementModal').modal('show');
    });

    // Show/hide dropdown options area based on selected input type
    $('#inputType').on('change', function () {
        if ($(this).val() == '5') {
            $('#dropdownOptionsArea').show();
        } else {
            $('#dropdownOptionsArea').hide();
        }
    });

    // Add new dropdown option
    $('#addDropdownOptionBtn').on('click', function () {
        const optionIndex = $('#dropdownOptionsContainer .dropdown-option').length;
        $('#dropdownOptionsContainer').append(`
            <div class="input-group mb-2 dropdown-option">
                <input type="text" class="form-control" name="dropdown_option_${optionIndex}" placeholder="Seçenek">
                <button class="btn btn-danger btn-sm remove-option-btn" type="button">&times;</button>
            </div>
        `);
    });

    // Remove a dropdown option
    $('#dropdownOptionsContainer').on('click', '.remove-option-btn', function () {
        $(this).closest('.dropdown-option').remove();
    });

    // Handle form submission for adding a new form element
    $('#addFormElementForm').on('submit', function (e) {
        e.preventDefault();

        const name = $('#elementName').val();
        const inputType = $('#inputType').val();
        const copyable = $('#copyableCheckbox').is(':checked');
        let options = [];

        // If the selected input type is Dropdown
        if (inputType == '5') {
            $('#dropdownOptionsContainer .dropdown-option input').each(function () {
                options.push($(this).val());
            });
        }

        $.ajax({
            url: '/admin/element/add',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                name: name,
                input_type: inputType,
                copyable: copyable,
                options: options
            }),
            success: function (response) {
                addMessage(response);
                if (response.success) {
                    $('#addFormElementModal').modal('hide');
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
