document.addEventListener('DOMContentLoaded', () => {
    const editButton = document.querySelector('.edit-info-data-button');
    const fnameElement = document.querySelector('.info-fname');
    const lnameElement = document.querySelector('.info-lname');

    editButton.addEventListener('click', () => {
        if (editButton.textContent === 'Редактировать') {
            enableEditing(fnameElement);
            enableEditing(lnameElement);
            editButton.textContent = 'Сохранить';
        } else {
            saveEditing(fnameElement);
            saveEditing(lnameElement);
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

    function saveEditing(element) {
        const input = element.querySelector('.edit-input');
        if (input) {
            element.textContent = input.value;
        }
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const logo = document.querySelector('.personal-cabinet-work-logo').querySelector('img');
    const imageLink = document.querySelector('.info-image');
    const imageElement = imageLink.querySelector('img');
    const fileInput = document.querySelector('.upload-image-input');

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

    const savedData = {
        password: '123456SK',
        email: 'namefamily@gmail.com',
        phone: '+7 903 565 44 76',
        job: '...',
        comment: '...',
        specialOne: '...',
        specialTwo: '...'
    };

    function updateFieldsContent() {
        if (vacanciesInfoRadio.checked) {
            fieldsToChange.innerHTML = `
                <div class="field">
                    <p class="field header">Мои вакансии</p>
                </div>
            `;
        } else if (persInfoRadio.checked) {
            fieldsToChange.innerHTML = `
                <div class="field">
                    <p class="field header">Доп. информация</p>
                    <div class="field window">
                        <div class="field-columns">
                            <div class="field-column main">
                                <p class="field-text">Должность</p>
                                <p class="field-text">Комментарий</p>
                            </div>
                            <div class="field-column">
                                <p class="field-text job">${savedData.job}</p>
                                <p class="field-text comment">${savedData.comment}</p>
                            </div>
                        </div>
                        <div class="field-buttons">
                            <button class="field-button job" type="button">Изменить</button>
                            <button class="field-button comment" type="button">Изменить</button>
                        </div>
                    </div>
                </div>
                <div class="field">
                    <p class="field header">Личные данные</p>
                    <div class="field window">
                        <div class="field-columns">
                            <div class="field-column main">
                                <p class="field-text">Пароль</p>
                                <p class="field-text">Email</p>
                                <p class="field-text">Телефон</p>
                            </div>
                            <div class="field-column">
                                <p class="field-text password">${savedData.password}</p>
                                <p class="field-text email">${savedData.email}</p>
                                <p class="field-text phone">${savedData.phone}</p>
                            </div>
                        </div>
                        <div class="field-buttons">
                            <button class="field-button password" type="button">Изменить</button>
                            <button class="field-button email" type="button">Изменить</button>
                            <button class="field-button phone" type="button">Изменить</button>
                        </div>
                    </div>
                </div>
                <div class="field">
                    <p class="field header">Спецпризнаки</p>
                    <div class="field window">
                        <div class="field-columns">
                            <div class="field-column main">
                                <p class="field-text">Спецпризнак 1</p>
                                <p class="field-text">Спецпризнак 2</p>
                            </div>
                            <div class="field-column">
                                <p class="field-text special-one">${savedData.specialOne}</p>
                                <p class="field-text special-two">${savedData.specialTwo}</p>
                            </div>
                        </div>
                        <div class="field-buttons">
                            <button class="field-button special-one" type="button">Изменить</button>
                            <button class="field-button special-two" type="button">Изменить</button>
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
                        savedData[targetClass] = newValue;
                        textElement.textContent = newValue;
                    }
                    button.textContent = 'Изменить';
                }
            });
        });
    }

    persInfoRadio.addEventListener('change', updateFieldsContent);
    vacanciesInfoRadio.addEventListener('change', updateFieldsContent);

    updateFieldsContent();
});

