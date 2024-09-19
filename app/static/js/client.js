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
                                        <!-- Options will be added dynamically -->
                                    </select>
                                </div>`;
                                fetchDropdownOptions(element.id);
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

        fetchFormElements().then(() => {
            Object.keys(formValues).forEach(function (key) {
                const value = formValues[key];

                const inputField = $(`input[name='${key}'], select[name='${key}'], .form-check-input[name='${key}']`);

                if (inputField.length) {
                    if (inputField.is('input[type="checkbox"]')) {
                        inputField.prop('checked', value);
                    } else if (inputField.is('select')) {
                    setTimeout(() => {
                        inputField.val(value);
                    }, 100); // Add a small delay to ensure options are loaded
                    } else {
                        inputField.val(value);
                    }
                }
            });

            $('#formModal').modal('show');
        });
    }

    function fetchDropdownOptions(elementId) {
        $.ajax({
            url: `/dropdown/options/${elementId}`,
            type: 'GET',
            success: function (response) {
                if (response.success) {
                    const dropdown = $(`select[name='element-${elementId}']`);
                    dropdown.empty(); // Clear previous options

                    response.data.forEach(function (option) {
                        dropdown.append(`<option value="${option.id}">${option.option_name}</option>`);
                    });
                } else {
                    console.error('Failed to fetch dropdown options:', response.message);
                }
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
            }
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
                    location.reload();
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
