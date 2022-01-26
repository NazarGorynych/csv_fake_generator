
let columnForm = document.querySelectorAll(".bird-form")
    let container = document.querySelector("#bird")
    let addButton = document.querySelector("#add-form")
    let totalForms = document.querySelector("#id_form-TOTAL_FORMS")

    let formNum = columnForm.length-1
    addButton.addEventListener('click', addForm)

    function addForm(e){
        e.preventDefault()

        let newForm = columnForm[0].cloneNode(true)
        let formRegex = RegExp(`form-(\\d){1}-`,'g')

        formNum++
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
        container.insertBefore(newForm, addButton)

        totalForms.setAttribute('value', `${formNum+1}`)
    }


$("#btn-id").click(function(){
  $(document).find("#btn-id").removeClass("actv");
  $(this).addClass("actv");
});
