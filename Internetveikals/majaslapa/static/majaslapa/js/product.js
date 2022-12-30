//Filtrešanas ailes animācijas
const acc_btns = document.querySelectorAll(".acardion");
const acc_contents = document.querySelectorAll(".sidebar_content")

acc_btns.forEach(btn => {
    btn.addEventListener("click", () => {
        const panel = btn.nextElementSibling;
        panel.classList.toggle("active")
        btn.classList.toggle("active")
})
})

// Cenas
const rangeInput = document.querySelectorAll(".range-input input"),
priceInput = document.querySelectorAll(".sidebar_content input"),
range = document.querySelector(".slider .progress");
let priceGap = 1;


priceInput.forEach(input =>{
    input.addEventListener("input", e =>{
        let minPrice = parseInt(priceInput[1].value),
        maxPrice = parseInt(priceInput[0].value);

        if((maxPrice - minPrice >= priceGap) && maxPrice <= rangeInput[1].max){
            if(e.target.className === "input-min"){
                rangeInput[0].value = minPrice;
                range.style.left = ((minPrice / rangeInput[0].max) * 1) + "%";
            }else{
                rangeInput[1].value = maxPrice;
                range.style.right = 1 - (maxPrice / rangeInput[1].max) * 1 + "%";
            }
        }
    });
});

rangeInput.forEach(input =>{
    input.addEventListener("input", e =>{
        let minVal = parseInt(rangeInput[0].value),
        maxVal = parseInt(rangeInput[1].value);
        if((maxVal - minVal) < priceGap){
            if(e.target.className === "range-min"){
                rangeInput[0].value = maxVal - priceGap
            }else{
                rangeInput[1].value = minVal + priceGap;
            }
        }else{
            priceInput[0].value = minVal;
            priceInput[1].value = maxVal;
            range.style.left = ((minVal / rangeInput[0].max) * 100) + "%";
            range.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
        }
    });
});


const selectElement = document.querySelector('.sidebar_content');
const submit = document.querySelector('#submit');

selectElement.addEventListener('change', (event) => {
    (submit).submit()
});


//checkbox
var last;
document.addEventListener('input',(e)=>{
var closest=e.target.closest("*[data-name='check']");
console.log(closest)
if(e.target.closest("*[data-name]")){
if(last)
last.checked=false;
}

e.target.checked=true;
last=e.target;
})

//poga
