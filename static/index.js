function formSubmit() {
    const imageField = document.getElementById('image');
    const fromField = document.getElementById('from_lang');
    const toField = document.getElementById('to_lang');

    const formData = new FormData();

    formData.append('document', imageField.files[0]);
    formData.append('from_lang', fromField.value);
    formData.append('to_lang', toField.value);

    fetch('/translate', {
        method: 'POST',
        body: formData,
    }).then(response => response.text()).then(result => {
        document.getElementById('translated-text').innerHTML = result;
    });

}