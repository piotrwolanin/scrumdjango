document.getElementById('add-form').addEventListener('click', addForm);
addEventListeners();

const numbersOnly = /[0-9]{1,3}/;

function addEventListeners() {
  const rmFormBtns = document.querySelectorAll('.remove-form');
  rmFormBtns.forEach(button => {
    button.addEventListener('click', removeForm);
  });
}

function addForm(event) {
  event.preventDefault();

  const allForms = document.querySelectorAll('.form-horizontal');

  if (allForms.length < 5) {

    const lastForm = allForms[allForms.length - 1];
    const newForm = lastForm.cloneNode(true);

    const newFormInputs = newForm.querySelectorAll(
      `select[id^=id_form-${allForms.length -
        1}], input[id^=id_form-${allForms.length -
          1}], ul[id^=id_form-${allForms.length - 1}]`
    );

    const newFormLabels = newForm.querySelectorAll(
      `label[for^=id_form-${allForms.length - 1}]`
    );

    const inputArray = Array.from(newFormInputs);
    inputArray.forEach(input => {
      input.id = input.id.replace(
        `id_form-${allForms.length - 1}`,
        `id_form-${allForms.length}`
      );

      if (input.name !== undefined) {
        input.name = input.name.replace(
          `form-${allForms.length - 1}`,
          `form-${allForms.length}`
        );
      }
    });

    const labelArray = Array.from(newFormLabels);
    labelArray.forEach(label => {
      label.htmlFor = label.htmlFor.replace(
        `id_form-${allForms.length - 1}`,
        `id_form-${allForms.length}`
      );
    });

    const formset = document.getElementById('create-tasks');
    formset.appendChild(newForm);
    addEventListeners();

    const totalForms = document.getElementById('id_form-TOTAL_FORMS');
    totalForms.value = Number(totalForms.value) + 1;
  }
}

function removeForm(event) {
  event.preventDefault();

  const allForms = document.querySelectorAll('.form-horizontal');

  if (allForms.length > 1) {

    const selectedForm = event.currentTarget.parentNode;

    const selectedFormId = selectedForm.querySelector('select').id;
    const selectedFormIndex = Number(numbersOnly.exec(selectedFormId)[0]);

    let nextForm = selectedForm.nextElementSibling;
    let nextFormIndex = selectedFormIndex;

    selectedForm.remove();

    while (nextForm !== null) {

      const nextFormInputs = nextForm.querySelectorAll(
        `select[id^=id_form-], input[id^=id_form-], ul[id^=id_form-]`
      );

      const nextFormLabels = nextForm.querySelectorAll(
        `label[for^=id_form-]`
      );

      const inputArray = Array.from(nextFormInputs);

      inputArray.forEach(input => {
        input.id = input.id.replace(
          `id_form-${nextFormIndex + 1}`,
          `id_form-${nextFormIndex}`
        );

        if (input.name !== undefined) {
          input.name = input.name.replace(
            `form-${nextFormIndex + 1}`,
            `form-${nextFormIndex}`
          );
        }
      });

      const labelArray = Array.from(nextFormLabels);
      labelArray.forEach(label => {
        label.htmlFor = label.htmlFor.replace(
          `id_form-${nextFormIndex + 1}`,
          `id_form-${nextFormIndex}`
        );
      });

      nextForm = nextForm.nextElementSibling;
      nextFormIndex += 1;
    };

    const totalForms = document.getElementById('id_form-TOTAL_FORMS');
    totalForms.value = Number(totalForms.value) - 1;
  }
}