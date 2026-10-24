
document.getElementById("alloy-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const zr = Number(document.getElementById("zr").value);
    const cu = Number(document.getElementById("cu").value);
    const ni = Number(document.getElementById("ni").value);
    const al = Number(document.getElementById("al").value);

    const total = zr + cu + ni + al;
    const message = document.getElementById("message");

    if ([zr, cu, ni, al].some(value => value < 0 || value > 100) ||
        Math.abs(total - 100) > 0.1) {
        message.textContent =
            "Please enter valid percentages that add up to 100%.";
        return;
    }

    message.textContent =
        "Input validated. Machine-learning model connection is not configured yet.";
});
