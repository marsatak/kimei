console.log('doleanceEdit.js')
const ndiBox = document.querySelector('#ndi')
console.log(ndiBox)
document.addEventListener('DOMContentLoaded', function () {
    const upperCaseInputs = document.querySelectorAll('input[type="text"], textarea');
    upperCaseInputs.forEach(input => {
        input.addEventListener('input', function () {
            this.value = this.value.toUpperCase();
        });
    });
});