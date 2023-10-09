const dropArea = document.querySelector('.drop-section');
const listSection = document.querySelector('.list-section');
const listContainer = document.querySelector('.list');
const fileSelector = document.querySelector('.file-selector');
const fileSelectorInput = document.querySelector('.file-selector-input');
const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

// Upload files with browse button
fileSelector.onclick = () => fileSelectorInput.click();
fileSelectorInput.onchange = () => {
    [...fileSelectorInput.files].forEach((file) => {
        if (typeValidation(file.type)) {
            uploadFile(file);
        }
    });
};

// When a file is over the drag area
dropArea.ondragover = (e) => {
    e.preventDefault();
    [...e.dataTransfer.items].forEach((item) => {
        if (typeValidation(item.type)) {
            dropArea.classList.add('drag-over-effect');
        }
    });
};

// When a file leaves the drag area
dropArea.ondragleave = () => {
    dropArea.classList.remove('drag-over-effect');
};

// When a file is dropped on the drag area
dropArea.ondrop = (e) => {
    e.preventDefault();
    dropArea.classList.remove('drag-over-effect');
    if (e.dataTransfer.items) {
        [...e.dataTransfer.items].forEach((item) => {
            if (item.kind === 'file') {
                const file = item.getAsFile();
                if (typeValidation(file.type)) {
                    uploadFile(file);
                }
            }
        });
    } else {
        [...e.dataTransfer.files].forEach((file) => {
            if (typeValidation(file.type)) {
                uploadFile(file);
            }
        });
    }
};

// Check the file type
function typeValidation(type) {
    return type === 'application/pdf';
}

// Upload a file using AJAX
function uploadFile(file) {
    listSection.style.display = 'block';
    const li = document.createElement('li');
    li.classList.add('in-prog');
    li.innerHTML = `
        <div class="col">
            <img src="/static/upload_file/img/pdf.png" alt="">
        </div>
        <div class="col">
            <div class="file-name">
                <div class="name">${file.name}</div>
                <span class="progress">0%</span>
            </div>
            <div class="file-progress">
                <span class="progress-bar"></span>
            </div>
            <div class="file-size">${(file.size / (1024 * 1024)).toFixed(2)} MB</div>
            <div class="file-status">Uploading...</div>
            <div class="custom-message"></div> <!-- Create an empty div for custom messages -->
        </div>
        <div class="col">
            <svg xmlns="http://www.w3.org/2000/svg" class="cross" height="20" width="20"><path d="m5.979 14.917-.854-.896 4-4.021-4-4.062.854-.896 4.042 4.062 4-4.062.854.896-4 4.062 4 4.021-.854.896-4-4.063Z"/></svg>
            <svg xmlns="http://www.w3.org/2000/svg" class="tick" height="20" width="20"><path d="m8.229 14.438-3.896-3.917 1.438-1.438 2.458 2.459 6-6L15.667 7Z"/></svg>
        </div>
    `;
    listContainer.prepend(li);

    const http = new XMLHttpRequest();
    const data = new FormData();
    data.append('file', file);
    const uploadUrl = '/upload/'; // Replace with your actual upload URL

    const statusElement = li.querySelector('.file-status');

    http.onload = () => {
        li.classList.remove('in-prog');
        const responseArray = JSON.parse(http.responseText);

        // Ensure responseArray is an array and contains at least one element
        if (Array.isArray(responseArray) && responseArray.length > 0) {
            // Access the first element (assuming there's only one)
            const responseObject = responseArray[0];

            // Update status based on the response
            statusElement.textContent = responseObject.message;

            // Color the status text based on the log field
            switch (responseObject.log) {
                case 'error':
                    statusElement.style.color = 'red';
                    break;
                case 'success':
                    statusElement.style.color = 'green';
                    break;
                case 'caution':
                    statusElement.style.color = 'violet';
                    break;
            }
        }

    };

    http.upload.onprogress = (e) => {
        const percentComplete = (e.loaded / e.total) * 100;
        li.querySelector('.progress').textContent = Math.round(percentComplete) + '%';
        li.querySelector('.progress-bar').style.width = percentComplete + '%';
    };

    http.open('POST', uploadUrl, true);

    // Set the CSRF token in the request headers
    http.setRequestHeader("X-CSRFToken", csrfToken);

    http.send(data);

    li.querySelector('.cross').onclick = () => http.abort();
    http.onabort = () => li.remove();
}

