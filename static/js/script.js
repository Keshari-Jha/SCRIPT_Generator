function generateScript() {
    let action = document.getElementById("action").value;
    let locationsInput = document.getElementById("locations").value;
    let locations = locationsInput.split("\n").map(line => line.split(",").map(item => item.trim()));

    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action, locations })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("downloadLink").innerHTML = 
            `<a href="/download/${data.filename}" download>Download Script</a>`;
    })
    .catch(error => console.error("Error:", error));
}
