document.addEventListener("DOMContentLoaded", function () {
    $('.ui.dropdown').dropdown();
    const searchInput = document.querySelector("input");
    const searchButton = document.getElementById("searchInput");
    const meaningText = document.getElementById("meaningText");
    const jungianBtn = document.getElementById("jungianBtn");
    const modernBtn = document.getElementById("modernBtn");
    let currentType = "jungian"; // Tipo seleccionado por defecto

    // Función para obtener el significado desde el backend
    function buscarSignificado(palabra, tipo) {
        fetch("/buscar_palabra", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ palabra, tipo }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.significado) {
                meaningText.innerText = data.significado;
            } else {
                meaningText.innerText = "No se encontró el significado, si lo desea inicie sesion para ser parte de nuestro equipo y agregar nuevos sueños";
            }
        })
        .catch(error => {
            meaningText.innerText = "Error al obtener el significado.";
            console.error("Error:", error);
        });
    }

    // Evento al hacer clic en el botón de búsqueda
    searchButton.addEventListener("click", function () {
        const palabra = searchInput.value.trim().toLowerCase();
        if (palabra) {
            buscarSignificado(palabra, currentType);
        } else {
            meaningText.innerText = "Por favor, ingrese una palabra clave.";
        }
    });

    // Evento para cambiar a "Jungian" y buscar de nuevo automáticamente
    jungianBtn.addEventListener("click", function () {
        if (currentType !== "jungian") {
            currentType = "jungian";
            jungianBtn.classList.add("active");
            modernBtn.classList.remove("active");
            buscarSignificado(searchInput.value.trim().toLowerCase(), currentType);
        }
    });

    // Evento para cambiar a "Modern" y buscar de nuevo automáticamente
    modernBtn.addEventListener("click", function () {
        if (currentType !== "modern") {
            currentType = "modern";
            modernBtn.classList.add("active");
            jungianBtn.classList.remove("active");
            buscarSignificado(searchInput.value.trim().toLowerCase(), currentType);
        }
    });
});


//MODALS

document.querySelectorAll('.editar-publicacion').forEach(button => {
    button.addEventListener('click', function () {
        const id = this.getAttribute('data-id');
        const content = this.getAttribute('data-content');

        // Llenar el formulario con los datos de la publicación
        document.getElementById('contenido-editar').value = content;

        // Configurar la acción del formulario
        document.getElementById('form-editar').action = `/editar_publicacion/${id}`;

        // Mostrar el modal
        $('#modal-editar').modal('show');
    });
});

// Cerrar el modal al hacer clic en "Cancelar"
document.querySelector('.ui.modal .cancel').addEventListener('click', function () {
    $('#modal-editar').modal('hide');
});

// Enviar el formulario y cerrar el modal al guardar
document.getElementById('form-editar').addEventListener('submit', function (e) {
    e.preventDefault();
    fetch(this.action, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(new FormData(this)),
    })
    .then(response => {
        if (response.ok) {
            window.location.reload(); // Recargar la página para ver los cambios
        } else {
            alert('Error al actualizar la publicación');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
    // Abrir el modal de confirmación al hacer clic en "Eliminar"
document.querySelectorAll('.eliminar-publicacion').forEach(button => {
    button.addEventListener('click', function () {
        const id = this.getAttribute('data-id');

        // Configurar el enlace de eliminación
        document.getElementById('confirmar-eliminar').href = `/eliminar_publicacion/${id}`;

        // Mostrar el modal
        $('#modal-confirmar-eliminar').modal('show');
    });
});

    // Abrir el modal para agregar significados
document.getElementById('abrir-modal-agregar').addEventListener('click', function () {
    $('#modal-agregar').modal('show');
});

// Cerrar modales al hacer clic en "Cancelar" o "Cerrar"
document.querySelectorAll('.ui.modal .cancel').forEach(button => {
    button.addEventListener('click', function () {
        $(this).closest('.ui.modal').modal('hide');
    });
});

