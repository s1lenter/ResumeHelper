document.addEventListener('DOMContentLoaded', () => {
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
                input.classList.add('edit-input')
                textElement.textContent = '';
                textElement.appendChild(input);
                button.textContent = 'Сохранить';
            } else {
                const input = textElement.querySelector('.edit-input');
                if (input) {
                    textElement.textContent = input.value;
                }
                button.textContent = 'Изменить';
            }
        });
    });
});

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
