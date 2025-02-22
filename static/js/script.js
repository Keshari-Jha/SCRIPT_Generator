function addRow() {
    let table = document.getElementById("locations");
    let row = table.insertRow(-1);
    let fields = ["loc", "ip_a", "ip_b", "ip_c", "ip_d", "lport_udp_b", "lport_udp_c"];

    fields.forEach((field, index) => {
        let cell = row.insertCell(index);
        let input = document.createElement("input");
        input.type = "text";
        input.name = field;
        input.setAttribute("onfocus", "this.select()"); // Enable selection for copy-paste
        cell.appendChild(input);
    });
}
document.getElementById("enumBtn").addEventListener("click", function() {
    submitScript("enum");
});

document.getElementById("sccpBtn").addEventListener("click", function() {
    submitScript("sccp");
});

document.getElementById("ipsmBtn").addEventListener("click", function() {
    submitScript("ipsm");
});
document.getElementById("flashBtn").addEventListener("click", function() {
    submitScript("flash");
});
function submitScript(scriptType) {
    let action = document.querySelector('input[name="action"]:checked').value; // config or delete
    let rows = document.querySelectorAll("#locations tr");
    let locations = [];

    rows.forEach((row, index) => {
        if (index > 0) { // Skip header row
            let inputs = row.getElementsByTagName("input");
            let values = Array.from(inputs).map(input => input.value);
            if (values.some(value => value !== "")) { // Ensure row is not empty
                locations.push(values);
            }
        }
    });

    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ locations, action, scriptType })
    })
    .then(response => response.json())
    .then(data => window.location.href = "/download/" + data.filename);
};
