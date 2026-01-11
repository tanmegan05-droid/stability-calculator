// Get DOM elements
const draftInput = document.getElementById("draft");
const kgInput = document.getElementById("kg");
const calculateButton = document.getElementById("calculate");
const resultOutput = document.getElementById("result");
const ctx = document.getElementById("gz-curve").getContext("2d");

// Placeholder KN curve data
const knCurves = {
    "heel30": [0.5, 0.6, 0.7, 0.9], // Example KN curve for 30° heel
    "heel45": [0.4, 0.5, 0.6, 0.8], // Example KN curve for 45° heel
};
// Draft to displacement map
const displacementData = {
    "5.00": 2000,
    "5.05": 2020,
    // Additional draft values...
};

// Function to calculate GZ
function calculateGZ(draft, kg, angle) {
    const kn = knCurves["heel" + angle][0]; // Get KN for given angle and draft (hardcoded for demo)
    const gz = kn - kg * Math.sin((angle * Math.PI) / 180);
    return gz;
}

// Handle calculate button click
calculateButton.addEventListener("click", () => {
    const draft = draftInput.value;
    const kg = kgInput.value;
    const displacement = displacementData[draft];

    if (!displacement) {
        resultOutput.textContent = "Invalid draft input or data missing.";
        return;
    }

    const gzValues = [
        calculateGZ(draft, kg, 30),
        calculateGZ(draft, kg, 45),
    ];

    resultOutput.textContent = `Displacement: ${displacement}, GZ values: ${gzValues}`;

    new Chart(ctx, {
        type: "line",
        data: {
            labels: [30, 45],
            datasets: [
                {
                    label: "GZ Curve",
                    data: gzValues,
                },
            ],
        },
    });
});