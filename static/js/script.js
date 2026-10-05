const resumeInput = document.getElementById("resumeInput");
const dropZone = document.getElementById("dropZone");
const fileInfo = document.getElementById("fileInfo");
const analyzeBtn = document.getElementById("analyzeBtn");

let selectedFile = null;


function updateFile(file) {

    if (!file) {
        return;
    }

    selectedFile = file;

    fileInfo.textContent = "Selected: " + file.name;

    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze Resume";
}


resumeInput.addEventListener("change", function () {

    if (resumeInput.files.length > 0) {
        updateFile(resumeInput.files[0]);
    }

});


dropZone.addEventListener("dragover", function (event) {

    event.preventDefault();

    dropZone.classList.add("dragging");

});


dropZone.addEventListener("dragleave", function () {

    dropZone.classList.remove("dragging");

});


dropZone.addEventListener("drop", function (event) {

    event.preventDefault();

    dropZone.classList.remove("dragging");

    const files = event.dataTransfer.files;

    if (files.length > 0) {
        updateFile(files[0]);
    }

});


analyzeBtn.addEventListener("click", async function () {

    if (!selectedFile) {
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing...";

    fileInfo.textContent =
        "Please wait while PathPilot AI analyzes your resume...";

    const formData = new FormData();

    formData.append("resume", selectedFile);


    try {

        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });


        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || "Analysis failed.");
        }


        /*
         * Backend ippudu result.html ni direct ga return chestundi.
         * Kabatti JSON parse cheyyakunda HTML ni browser ki load chestunnam.
         */

        const html = await response.text();

        document.open();
        document.write(html);
        document.close();

    }

    catch (error) {

        fileInfo.textContent =
            "❌ " + error.message;

        analyzeBtn.disabled = false;
        analyzeBtn.textContent = "Analyze Resume";

    }

});