
let columnForm = document.querySelectorAll(".bird-form")
    let container = document.querySelector("#bird")
    let addButton = document.querySelector("#add-form")
    let totalForms = document.querySelector("#id_dataschemecolumn_set-TOTAL_FORMS")

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


// $("#btn-id").click(function(){
//   $(document).find("#btn-id").removeClass("actv");
//   $(this).addClass("actv");
// });

// function cloneMore(selector, type) {
//     var newElement = $(selector).clone(true);
//     var total = $('#id_' + type + '-TOTAL_FORMS').val();
//     newElement.find(':input').each(function() {
//         var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
//         var id = 'id_' + name;
//         $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
//     });
//     newElement.find('label').each(function() {
//         var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
//         $(this).attr('for', newFor);
//     });
//     total++;
//     $('#id_' + type + '-TOTAL_FORMS').val(total);
//     $(selector).after(newElement);
// }