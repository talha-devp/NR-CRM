$(document).ready(function () {
    $('#openFormModal').on('click', function () {
        $.ajax({
            url: '/form/elements',
            type: 'GET',
            success: function (response) {
                if (response.success) {
                    let formElements = response.data;
                    let formContainer = $('#formElementsContainer');
                    formContainer.empty(); // Clear existing content

                    formElements.forEach(function (element) {
                        let inputField;
                        switch (element.input_type) {
                            case 1: // Text
                                inputField = `<div class="mb-3">
                                    <label class="form-label">${element.name}</label>
                                    <input type="text" class="form-control" name="element-${element.id}">
                                </div>`;
                                break;
                            case 2: // Number
                                inputField = `<div class="mb-3">
                                    <label class="form-label">${element.name}</label>
                                    <input type="number" class="form-control" name="element-${element.id}">
                                </div>`;
                                break;
                            case 3: // Date Picker
                                inputField = `<div class="mb-3">
                                    <label class="form-label">${element.name}</label>
                                    <input type="date" class="form-control" name="element-${element.id}">
                                </div>`;
                                break;
                            case 4: // Checkbox
                                inputField = `<div class="mb-3">
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" name="element-${element.id}">
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
                        formContainer.append(inputField);
                    });

                    $('#formModal').modal('show');
                } else {
                    console.error('Failed to fetch form elements:', response.message);
                }
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
            }
        });

        // Handle form submission
        $('#formContentForm').on('submit', function (event) {
            event.preventDefault();

            let formData = $(this).serialize();

            $.ajax({
                url: '/form/add',
                type: 'POST',
                data: formData,
                success: function (response) {
                    if (response.success) {
                        alert('Form başarıyla eklendi.');
                        $('#formModal').modal('hide');
                    } else {
                        alert('Form eklenirken bir hata oluştu.');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error:', error);
                    alert('Form eklenirken bir hata oluştu.');
                }
            });
        });
    });
});
