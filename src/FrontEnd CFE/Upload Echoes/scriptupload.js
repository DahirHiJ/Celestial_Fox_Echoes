const form = document.querySelector("form");
const fileInput = form.querySelector(".file-input");
const progressArea = document.querySelector(".progress-area");
const uploadedArea = document.querySelector(".uploaded-area");

form.addEventListener("submit", (e) => {
    e.preventDefault();
    fileInput.click();
});

fileInput.onchange = ({ target }) => {
    let file = target.files[0];
    if (file) {
        let fileName = file.name; 
        uploadFile(file);
    }
}

function uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);

    fetch("URL_DE_TU_BACKEND", {
        method: "POST",
        body: formData,
    })
    .then((response) => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Error al cargar el archivo.");
        }
    })
    .then((data) => {
        // Aquí puedes manejar la respuesta del backend si es necesario
        console.log("Archivo cargado exitosamente:", data);
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}
