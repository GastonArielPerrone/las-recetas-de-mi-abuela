var identification = prompt("Por favor, para la utilización del programa necesitamos tu identificación");
var id_real = ["36276343", "18735727", "92403849"];

function inProcess(identification, id_real) {
    if (id_real.includes(identification)) {
        var confirmation = confirm("Su identificación está permitida para hacer uso de este programa. ¿Desea continuar?");
        if (confirmation) {
            alert("Gracias. Continuemos.");
        } else {
            alert("Operación cancelada.");
            window.location.href = "/index.html";

        }
    } else {
        alert("¡Lo siento! Su identificación no está permitida para hacer uso de este programa.");
        window.location.href = "/index.html";
    }
}

// Llamada a la función
inProcess(identification, id_real);