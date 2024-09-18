$(document).ready(function () {
    // Open the modal to add a new form
    $('.openFormModal').on('click', function () {
        openFormModal();
    });

    // Open the modal to edit an existing form
    $('.list-group').on('click', '.form-item', function () {
        const formId = $(this).data('id');
        openFormModal(formId);
    });

    function openFormModal(formId = null) {
        $('#formElementsContainer').empty();
        $('input[name="formName"]').val('');

        if (formId) {
            // Fetch the existing form data
            $.ajax({
                url: `/form/${formId}`,
                type: 'GET',
                success: function (response) {
                    if (response.success) {
                        populateModal(response.data);
                        $('#formModal').modal('show');
                    } else {
                        console.error('Failed to fetch form data:', response.message);
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error:', error);
                }
            });
        } else {
            fetchFormElements();
            $('#formModalLabel').text('Yeni Form Ekle');
            $('#formContentForm').data('formId', null);
            $('#formModal').modal('show');
        }
    }

    function fetchFormElements() {
        return $.ajax({
            url: '/form/elements',
            type: 'GET',
            success: function (response) {
                if (response.success) {
                    $('#formElementsContainer').empty(); // Clear previous inputs
                    response.data.forEach(function (element) {
                        let inputField;
                        switch (element.input_type) {
                            case 1: // Text
                                inputField = `<div class="mb-3">
                                    <label class="form-label">${element.name}</label>
                                    <input type="text" autocomplete="off" class="form-control" name="element-${element.id}" ${element.compulsory ? 'required' : ''}>
                                </div>`;
                                break;
                            case 2: // Number
                                inputField = `<div class="mb-3">
                                    <label class="form-label">${element.name}</label>
                                    <input type="number" class="form-control" name="element-${element.id}" ${element.compulsory ? 'required' : ''}>
                                </div>`;
                                break;
                            case 3: // Date Picker
                                inputField = `<div class="mb-3">
                                    <label class="form-label">${element.name}</label>
                                    <input type="date" class="form-control" name="element-${element.id}" ${element.compulsory ? 'required' : ''}>
                                </div>`;
                                break;
                            case 4: // Checkbox
                                inputField = `<div class="mb-3">
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" name="element-${element.id}" ${element.compulsory ? 'required' : ''}>
                                        <label class="form-check-label">${element.name}</label>
                                    </div>
                                </div>`;
                                break;
                            case 5: // Dropdown
                                inputField = `<div class="mb-3">
                                    <label class="form-label">${element.name}</label>
                                    <select class="form-select" name="element-${element.id}">
                                        <!-- Add dropdown options here -->
                                    </select>
                                </div>`;
                                break;
                        }
                        $('#formElementsContainer').append(inputField);
                    });
                } else {
                    console.error('Failed to fetch form elements:', response.message);
                }
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
            }
        });
    }

    function populateModal(formData) {
        $('#formModalLabel').text('Formu Düzenle');
        $('#formContentForm').data('formId', formData.id);

        const formValues = JSON.parse(formData.value);

        $('input[name="formName"]').val(formData.name);

        // Fetch form elements first
        fetchFormElements().then(() => {
            // Now that the inputs are generated, set their values
            Object.keys(formValues).forEach(function (key) {
                const value = formValues[key];

                // Find the corresponding input field
                const inputField = $(`input[name='${key}'], select[name='${key}'], .form-check-input[name='${key}']`);

                // Set the value accordingly
                if (inputField.length) {
                    if (inputField.is('input[type="checkbox"]')) {
                        inputField.prop('checked', value);
                    } else {
                        inputField.val(value);
                    }
                }
            });

            // Show the modal after populating it
            $('#formModal').modal('show');
        });
    }

    $('#formContentForm').on('submit', function (event) {
        event.preventDefault();

        const formId = $(this).data('formId');
        const url = formId ? `/form/update/${formId}` : '/form/add';

        let formData = $(this).serialize();

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            success: function (response) {
                if (response.success) {
                    alert('Form başarıyla kaydedildi.');
                    $('#formModal').modal('hide');
                    // Optionally, refresh the list or update UI without refresh
                } else {
                    alert('Form kaydedilirken bir hata oluştu.');
                }
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
                alert('Form kaydedilirken bir hata oluştu.');
            }
        });
    });
});
