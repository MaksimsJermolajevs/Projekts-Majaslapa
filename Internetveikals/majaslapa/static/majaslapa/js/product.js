// const accordion = document.getElementsByClassName("filter_title")
// const filter = document.getElementsByClassName("filter")

// for (i = 0; i < accordion.length; i++) {
// 	accordion[i].addEventListener("click", function () {
// 		this.classList.toggle("active")
// 	})
// }


const acc_btns = document.querySelectorAll(".acardion");
const acc_contents = document.querySelectorAll(".sidebar_content")

acc_btns.forEach(btn => {
    btn.addEventListener("click", () => {
        const panel = btn.nextElementSibling;
        panel.classList.toggle("active")

        btn.classList.toggle("active")
})
})
