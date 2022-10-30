const showPasswordToggle = document.querySelector('.showPasswordToggle');
const passwordField = document.querySelector('#passwordField')


const handleToggleInput=(e)=>{
if (showPasswordToggle.name === 'eye-off-outline'){
    showPasswordToggle.name = 'eye-outline';
    passwordField.setAttribute('type', 'text')
}else{
    showPasswordToggle.name = 'eye-off-outline';
    passwordField.setAttribute('type', 'password')
}
}

showPasswordToggle.addEventListener('click',handleToggleInput);