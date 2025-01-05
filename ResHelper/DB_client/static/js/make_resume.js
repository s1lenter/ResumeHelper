function addField(type) {
    const form = document.querySelector('.main-fields.personal-info');

    const newFieldBlock = document.createElement('div');
    newFieldBlock.className = `main-fields ${type}`;
    newFieldBlock.style.marginTop = '10px';

    const separator = document.createElement('div');
    separator.className = 'separator';
    separator.style.margin = '10px 0 0 0';
    separator.style.borderTop = '3px solid black';
    form.appendChild(separator);

    if (type === 'achievements') {
        const newInput = document.createElement('input');
        newInput.className = 'main-input-field';
        newInput.type = 'file';
        newInput.name = 'achievements';
        newFieldBlock.appendChild(newInput);
    } else if (type === 'abilities') {
        const newInput = document.createElement('input');
        newInput.className = 'main-input-field';
        newInput.type = 'text';
        newInput.name = 'abilities';
        newInput.placeholder = 'Введите навык';
        newFieldBlock.appendChild(newInput);
    } else if (type === 'work-experience') {
        const newProfession = document.createElement('div');
        newProfession.className = 'main-field work-experience';
        newProfession.innerHTML = `
            <label for="profession" class="main-field-header">Профессия</label>
            <input type="text" class="main-input-field" name="profession" required>
        `;

        const newCompany = document.createElement('div');
        newCompany.className = 'main-field work-company';
        newCompany.innerHTML = `
            <label for="company" class="main-field-header">Компания</label>
            <input type="text" class="main-input-field" name="company" required>
        `;

        const newStartDate = document.createElement('div');
        newStartDate.className = 'main-field work-startdate';
        newStartDate.innerHTML = `
            <label for="startdate" class="main-field-header">Дата начала работы</label>
            <input type="date" class="main-input-field" name="startdate" required>
        `;

        const newEndDate = document.createElement('div');
        newEndDate.className = 'main-field work-enddate';
        newEndDate.innerHTML = `
            <label for="enddate" class="main-field-header">Дата окончания работы</label>
            <input type="date" class="main-input-field" name="enddate" required>
        `;

        newFieldBlock.appendChild(newProfession);
        newFieldBlock.appendChild(newCompany);
        newFieldBlock.appendChild(newStartDate);
        newFieldBlock.appendChild(newEndDate);
    }

    form.appendChild(newFieldBlock);

    const deleteButton = form.querySelector('.delete-button');
    deleteButton.hidden = false;

    const addButton = form.querySelector('.add-button');
    form.appendChild(addButton);
    form.appendChild(deleteButton);
}

function deleteField() {
    const form = document.querySelector('.main-fields.personal-info');
    const fields = form.querySelectorAll('.main-fields');
    const separators = form.querySelectorAll('.separator');

    if (fields.length > 0) {
        const lastField = fields[fields.length - 1];
        lastField.remove();
    }

    if (separators.length > 0) {
        const lastSeparator = separators[separators.length - 1];
        lastSeparator.remove();
    }

    if (fields.length === 1) {
        const deleteButton = form.querySelector('.delete-button');
        deleteButton.hidden = true;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const today = new Date().toISOString().split('T')[0];
    const startDateInputs = document.querySelectorAll('input[type="date"][name="startdate"]');
    const endDateInputs = document.querySelectorAll('input[type="date"][name="enddate"]');

    startDateInputs.forEach(input => input.setAttribute('max', today));
    endDateInputs.forEach(input => input.setAttribute('max', today));
});
