let fileNameLabel = document.getElementById("filename");
let fileInput = document.getElementById("file");

function updateFileNameLabel(e) {
	if (e.target.files.length > 0) {
		fileNameLabel.innerHTML = e.target.files[0].name;
	}
}

fileInput.addEventListener("input", updateFileNameLabel);
