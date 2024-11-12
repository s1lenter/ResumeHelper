function addField(type) {
    const form = document.getElementById(`${type}-form`);

    if (type === 'work-experience') {
        const newFieldBlock = document.createElement('div');
        newFieldBlock.className = 'main-fields work-experience';

        const newProfession = document.createElement('div');
        newProfession.className = 'main-field work-experience';
        newProfession.innerHTML = `
            <form>
                <label for="profession" class="main-field-header">Профессия</label>
                <input type="text" class="main-input-field" name="profession" required>
            </form>
        `;
        
        const newCompany = document.createElement('div');
        newCompany.className = 'main-field work-company';
        newCompany.innerHTML = `
            <form>
                <label for="company" class="main-field-header">Компания</label>
                <input type="text" class="main-input-field" name="company" required>
            </form>
        `;
        
        const newStartDate = document.createElement('div');
        newStartDate.className = 'main-field work-startdate';
        newStartDate.innerHTML = `
            <form>
                <label for="startdate" class="main-field-header">Дата начала работы</label>
                <input type="date" class="main-input-field" name="startdate" required>
            </form>
        `;
        
        const newEndDate = document.createElement('div');
        newEndDate.className = 'main-field work-enddate';
        newEndDate.innerHTML = `
            <form>
                <label for="enddate" class="main-field-header">Дата окончания работы</label>
                <input type="date" class="main-input-field" name="enddate" required>
            </form>
        `;
        
        const separator = document.createElement('hr');
        separator.className = 'field-separator';
        newFieldBlock.appendChild(separator);

        newFieldBlock.appendChild(newProfession);
        newFieldBlock.appendChild(newCompany);
        newFieldBlock.appendChild(newStartDate);
        newFieldBlock.appendChild(newEndDate);

        form.appendChild(newFieldBlock);
    } else {
        const newInput = document.createElement('input');
        newInput.className = 'main-input-field';
        if (type === 'achievements') {
            newInput.type = 'file';
            newInput.name = 'achievements';
        } else if (type === 'abilities') {
            newInput.type = 'text';
            newInput.name = 'abilities';
            newInput.placeholder = 'Введите навык';
        }
        newInput.style.marginTop = '10px';
        form.appendChild(newInput);
    }

    const addButton = form.querySelector('.add-button');
    form.appendChild(addButton);
}
