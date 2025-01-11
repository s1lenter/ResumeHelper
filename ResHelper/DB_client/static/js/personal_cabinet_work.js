document.addEventListener('DOMContentLoaded', () => {
    const editButton = document.querySelector('.edit-info-data-button');
    const fnameElement = document.querySelector('.info-fname');
    const lnameElement = document.querySelector('.info-lname');
    const hiddenInputs = document.querySelectorAll('.hidden-input');

    editButton.addEventListener('click', () => {
        if (editButton.textContent === 'Редактировать') {
            enableEditing(fnameElement);
            enableEditing(lnameElement);
            editButton.textContent = 'Сохранить';
        } else {
            saveEditing(fnameElement, 'fn');
            saveEditing(lnameElement, 'ln');
            editButton.textContent = 'Редактировать';
        }
    });

    function enableEditing(element) {
        const currentText = element.textContent;
        const input = document.createElement('input');
        input.type = 'text';
        input.value = currentText;
        input.classList.add('edit-input');
        element.textContent = '';

        element.appendChild(input);
    }

    function saveEditing(element, name) {
        const input = element.querySelector('.edit-input');
        if (input) {
            if (name === 'fn'){
                element.textContent = input.value;
                hiddenInputs[0].value = input.value;
            }
            else if (name === 'ln'){
                element.textContent = input.value;
                hiddenInputs[1].value = input.value;
            }
        }
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const logo = document.querySelector('.personal-cabinet-work-logo').querySelector('img');
    const imageLink = document.querySelector('.info-image');
    const imageElement = imageLink.querySelector('img');
    const fileInput = document.querySelector('.upload-image-input');
    const hiddenInput = document.querySelector('.hidden-input-file');

    imageLink.addEventListener('click', (event) => {
        event.preventDefault();
        fileInput.click();
    });

    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imageElement.src = e.target.result;
                logo.src = e.target.result;

                const blob = new Blob([file], { type: file.type });
                const newFile = new File([blob], file.name, { type: file.type });

                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(newFile);
                hiddenInput.files = dataTransfer.files;
            };
            reader.readAsDataURL(file);
        }
        logo.style.width = '60px';
        logo.style.height = '60px';
        logo.style.borderRadius = '50px';
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const radioButtons = document.querySelectorAll('input[name="info-button"]');

    function updateLabelColors() {
        radioButtons.forEach(radio => {
            const label = document.querySelector(`label[for="${radio.id}"]`);
            if (radio.checked) {
                label.style.color = 'white';
            } else {
                label.style.color = 'black';
            }
        });
    }

    radioButtons.forEach(radio => {
        radio.addEventListener('change', updateLabelColors);
    });

    updateLabelColors();
});

document.addEventListener('DOMContentLoaded', () => {
    const persInfoRadio = document.getElementById('pers-info');
    const vacanciesInfoRadio = document.getElementById('vacancies-info');
    const fieldsToChange = document.querySelector('.fields__toChange');

    async function fetchData() {
        try {
            const response = await fetch('/api/personal_data/');
            if (!response.ok) {
                throw new Error('Сеть ответила с проблемой: ' + response.statusText);
            }
            personalData = await response.json();
            console.log(personalData);

            updateFieldsContent();

        } catch (error) {
            console.error('Ошибка:', error);
        }
    }

    fetchData();

    function updateFieldsContent() {
        if (!personalData) return;

        if (vacanciesInfoRadio.checked) {
            fieldsToChange.innerHTML = `
                <div class="field">
                    <p class="field header">Ваши резюме</p>
                </div>
            `;
        } else if (persInfoRadio.checked) {
            fieldsToChange.innerHTML = `
                <div class="field">
                    <p class="field header">Доп. информация</p>
                    <div class="field window">
                        <div class="field-columns">
                            <div class="field-column main">
                                <p class="field-text">Пол</p>
                                <p class="field-text">Возраст</p>
                            </div>
                            <div class="field-column">
                                <p class="field-text sex">${personalData.sex}</p>
                                <p class="field-text age">${personalData.age}</p>
                            </div>
                        </div>
                        <div class="field-buttons">
                            <button class="field-button sex" type="button">Изменить</button>
                            <button class="field-button age" type="button">Изменить</button>
                        </div>
                    </div>
                </div>
                <div class="field">
                    <p class="field header">Личные данные</p>
                    <div class="field window">
                        <div class="field-columns">
                            <div class="field-column main">
                                <p class="field-text">Email</p>
                                <p class="field-text">Телефон</p>
                                <p class="field-text">Социальные сети</p>
                            </div>
                            <div class="field-column">
                                <p class="field-text email">${personalData.email}</p>
                                <p class="field-text phone">${personalData.phone}</p>
                                <p class="field-text soc-network">${personalData.socNetwork}</p>
                            </div>
                        </div>
                        <div class="field-buttons">
                            <button class="field-button email" type="button">Изменить</button>
                            <button class="field-button phone" type="button">Изменить</button>
                            <button class="field-button soc-network" type="button">Изменить</button>
                        </div>
                    </div>
                </div>
            `;
            addEditListeners();
        }
    }

    function addEditListeners() {
        document.querySelectorAll('.field-button').forEach(button => {
            button.addEventListener('click', () => {
                const targetClass = button.classList[1];
                const textElement = document.querySelector(`.field-text.${targetClass}`);
                const hiddenInputs = document.querySelectorAll('.hidden-input-dopinfo');

                if (!textElement) return;

                if (button.textContent === 'Изменить') {
                    const currentText = textElement.textContent;
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.value = currentText;
                    input.classList.add('edit-input');
                    textElement.textContent = '';
                    textElement.appendChild(input);
                    button.textContent = 'Сохранить';
                } else {
                    const input = textElement.querySelector('.edit-input');
                    if (input) {
                        const newValue = input.value;
                        personalData[targetClass] = newValue;
                        if (targetClass === 'sex'){
                            hiddenInputs[0].value = newValue;
                        }
                        else if (targetClass === 'age'){
                            hiddenInputs[1].value = newValue;
                        }
                        else if (targetClass === 'email'){
                            hiddenInputs[2].value = newValue;
                        }
                        else if (targetClass === 'phone'){
                            hiddenInputs[3].value = newValue;
                        }
                        else if (targetClass === 'soc-network'){
                            hiddenInputs[4].value = newValue;
                        }

                        textElement.textContent = newValue;
                    }
                    button.textContent = 'Изменить';
                }
            });
        });
    }

    persInfoRadio.addEventListener('change', updateFieldsContent);
    vacanciesInfoRadio.addEventListener('change', updateFieldsContent);
});

