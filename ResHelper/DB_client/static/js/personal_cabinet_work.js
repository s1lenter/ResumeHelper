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

    let personalData;
    let vacsData;

    async function fetchData() {
        const response = await fetch('/api/personal_data/');
        personalData = await response.json();
        console.log(personalData)
        updateFieldsContent();
    }

    async function fetchVacsData() {
        const response = await fetch('/api/vacancy_data/');
        vacsData = await response.json();
        console.log(vacsData)
        updateFieldsContent();
    }

    fetchData();
    fetchVacsData();

    function updateFieldsContent() {
        if (!personalData) return;

        if (vacanciesInfoRadio.checked) {
          let vacanciesHTML = `
          <div class="field">
              <p class="field header">Ваши вакансии</p>
          </div>
          `;
          const count = 4;
          const keys = Object.keys(vacsData);
          for (const id of keys) {
            let i = 0
              vacanciesHTML += `
                  <div class="js-main">
                      <div class="info">
                        <p class="name">${vacsData[id].name}</p>
                        <p class="salary">${vacsData[id].salary_info}</p>
                        <p class="company">${vacsData[id].company_name}</p>
                        <p class="city">${vacsData[id].location}</p>
                      </div>
                      <div class="js-main-buttons">
                        <a href="/delete_vac/${id}" class="delete-button">x</a>
                        <a href="/work_vacs_detail/${id}" class="delete-button">Посмотреть вакансию</button>
                      </div>
                  </div>
              `;
            }

          fieldsToChange.innerHTML = vacanciesHTML;
        } else if (persInfoRadio.checked) {
            fieldsToChange.innerHTML = `
                <div class="field">
                    <div class="field window">
                        <div class="field-columns">
                            <div class="field-column main">
                                <p class="field-text">Должность</p>
                            </div>
                            <div class="field-column">
                                <p class="field-text post">${personalData.emp_post}</p>
                            </div>
                        </div>
                        <div class="field-buttons">
                            <button class="field-button post" type="button">Изменить</button>
                        </div>
                    </div>
                </div>
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
                    if (targetClass === 'sex') {
                        const currentText = textElement.textContent;
                        const select = document.createElement('select');
                        select.classList.add('edit-select');

                        const maleOption = document.createElement('option');
                        maleOption.value = 'Мужской';
                        maleOption.textContent = 'Мужской';
                        select.appendChild(maleOption);

                        const femaleOption = document.createElement('option');
                        femaleOption.value = 'Женский';
                        femaleOption.textContent = 'Женский';
                        select.appendChild(femaleOption);

                        select.value = currentText;

                        textElement.textContent = '';
                        textElement.appendChild(select);
                    } else {
                        const currentText = textElement.textContent;
                        const input = document.createElement('input');
                        input.type = 'text';
                        input.value = currentText;
                        input.classList.add('edit-input');
                        textElement.textContent = '';
                        textElement.appendChild(input);
                    }
                    button.textContent = 'Сохранить';
                } else {
                    if (targetClass === 'sex') {
                      const select = textElement.querySelector('.edit-select');
                      if (select) {
                          const newValue = select.value;
                          personalData[targetClass] = newValue;
                          hiddenInputs[0].value = newValue;
                          textElement.textContent = newValue;
                      }
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
                            else if (targetClass === 'post'){
                                hiddenInputs[5].value = newValue;
                            }

                            textElement.textContent = newValue;
                        }
                    }
                    button.textContent = 'Изменить';
                }
            });
        });
    }

    persInfoRadio.addEventListener('change', updateFieldsContent);
    vacanciesInfoRadio.addEventListener('change', updateFieldsContent);
});

