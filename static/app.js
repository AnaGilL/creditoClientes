const dialog = document.querySelector("#client-dialog");
const form = document.querySelector("#client-form");
const title = document.querySelector("#dialog-title");

function openCreateDialog() {
  form.reset();
  document.querySelector("#client-id").value = "";
  title.textContent = "Agregar cliente";
  dialog.showModal();
  document.querySelector("#client-name").focus();
}

document.querySelector("#add-client").addEventListener("click", openCreateDialog);
document.querySelector("[data-open-create]")?.addEventListener("click", openCreateDialog);

document.querySelectorAll(".edit-client").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelector("#client-id").value = button.dataset.id;
    document.querySelector("#client-name").value = button.dataset.nombre;
    document.querySelector("#client-company").value = button.dataset.empresa;
    document.querySelector("#client-email").value = button.dataset.correo;
    document.querySelector("#client-phone").value = button.dataset.telefono;
    document.querySelector("#client-notes").value = button.dataset.notas;
    title.textContent = "Editar cliente";
    dialog.showModal();
    document.querySelector("#client-name").focus();
  });
});

document.querySelector(".dialog-close").addEventListener("click", () => dialog.close());
document.querySelector("#cancel-dialog").addEventListener("click", () => dialog.close());
document.querySelectorAll(".delete-form").forEach((deleteForm) => {
  deleteForm.addEventListener("submit", (event) => {
    if (!window.confirm("¿Eliminar este cliente del directorio?")) event.preventDefault();
  });
});
dialog.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close();
});