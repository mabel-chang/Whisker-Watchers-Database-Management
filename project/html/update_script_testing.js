//BANNER TAB FUNCTIONS
function openTab(evt, tabName) {
  // URL of the HTML file you want to redirect to
  var newPageUrl = 'https://bioed.bu.edu/students_24/Team_1/' + tabName + '.html';

  // Redirect to the new page
  window.location.href = newPageUrl;
}

//PAGE CONTENT FUNCTIONS
// Function to open the selected tab and show its content
function openUpdateTab(tabId) {
    // Get all tab buttons and content containers
    var tabButtonExisitng = document.getElementById('update-container');
    var tabButtonNew = document.getElementById('create-container');
    var tabContentsExisting = document.getElementById('content-update-container');
    var tabContentsNew = document.getElementById('content-create-container');
    var tabButtonDelete = document.getElementById('delete-container');
    var tabContentsDelete = document.getElementById('content-delete-container');

    // Remove active class from all tab buttons
    tabButtonExisitng.classList.remove('active');
    tabButtonNew.classList.remove('active');
    tabButtonDelete.classList.remove('active');

    // Hide all content containers
    tabContentsExisting.classList.add('hidden');
    tabContentsNew.classList.add('hidden');
    tabContentsDelete.classList.add('hidden');

    var selectedTabButton = document.getElementById(tabId);
    var selectedTabContent = document.getElementById(`content-${tabId}`);
    
    // Add active class to the selected tab button
    selectedTabButton.classList.add('active');
    // Show the corresponding content container
    selectedTabContent.classList.remove('hidden');
}

//Download template and instructions
function openBothFiles(type){
    if (type == 'update'){
        window.open('https://bioed.bu.edu/students_24/mchang15/upload_template_instructions.pdf', '_blank');
        window.open('https://bioed.bu.edu/students_24/mchang15/upload_template.xlsx', '_blank');
    } else if (type == 'create'){
        window.open('https://bioed.bu.edu/students_24/mchang15/create_template_instructions.pdf', '_blank');
        window.open('https://bioed.bu.edu/students_24/mchang15/create_template.xlsx', '_blank');
    }
}

//EXCEL SHEET
let filteredData = null;

function handleFileUpload(type, excelID) {
    const fileInput = document.getElementById(excelID);
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an Excel file");
        return;
    }

    const reader = new FileReader();

    reader.onload = function(event) {
        const data = new Uint8Array(event.target.result);
        const workbook = XLSX.read(data, { type: 'array' });

        const sheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];

        const parsedData = XLSX.utils.sheet_to_json(sheet, { header: 1 });
        
        console.log('pasrsedData:', parsedData);

        filteredData = parsedData.filter(row => !row.every(cell => cell === null || cell === ''));
       
        // Log the filteredData to console
        console.log('Filtered Data:', filteredData);

        displayPreview(filteredData, type);
        
        if (type =="update"){
          document.getElementById("update-excel-buttons").style.display = "inline"; // Show the Send Data button
    
        } else if (type =="new"){
          document.getElementById("create-excel-buttons").style.display = "inline"; // Show the Send Data button
    
        }
    };

    reader.readAsArrayBuffer(file);
}

function displayPreview(data, type) {
    let previewContainer;
    if (type == "new") {
        previewContainer = $("#previewContainerNew");
        previewContainer.empty(); // Clear previous preview
    } else if (type =="update") {
        previewContainer = $("#previewContainerUpdate");
        previewContainer.empty(); // Clear previous preview
    }
    
    const table = $("<table>");
    const headers = data[0];

    // Create table header row
    const headerRow = $("<tr>");
    headers.forEach(header => {
        headerRow.append($("<th>").text(header));
    });
    table.append(headerRow);

    // Create table rows with data
    for (let i = 1; i < data.length; i++) {
        const rowData = data[i];
        const row = $("<tr>");
        rowData.forEach(cell => {
            row.append($("<td>").text(cell));
        });
        table.append(row);
    }

    previewContainer.append(table);
}

function sendData(url) {
    if (!filteredData) {
        alert("Please upload an Excel file first.");
        return;
    }

    // Create a new XMLHttpRequest object
    const xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                console.log('Server response:', xhr.responseText);
                // Update status message to indicate success
                alert("Transfer successful! Check the filter tab to make sure your updates were added correctly");
            } else {
                console.error('Error:', xhr.statusText);
                // Update status message to indicate error
                alert("Error occurred during transfer");
            }
        }
    };

    // Send form data as JSON string
    xhr.send(JSON.stringify({ filteredData: filteredData }));
}

function deleteData() {
    const mouseIDsInput = document.getElementById("mouseIDs").value.trim();
    const mouseIDs = mouseIDsInput.split(",").map(id => id.trim());
    
    console.log('Data to delete:', mouseIDs);
    
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://bioed.bu.edu/cgi-bin/students_24/Team_1/upload_testing_mabel3.py', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                console.log('Server response:', xhr.responseText);
                // Update status message to indicate success
                alert("Transfer successful! Check the filter tab to make sure your updates were added correctly");
            } else {
                console.error('Error:', xhr.statusText);
                // Update status message to indicate error
                alert("Error occurred during transfer");
            }
        }
    };

    xhr.send(JSON.stringify({ mouseIDs: mouseIDs }));
}

function collectFormData(formId, url) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);

    // Convert FormData to a JSON object
    const formDataObject = {};
    formData.forEach((value, key) => {
        formDataObject[key] = value;
    });

    // Send the form data to the server using XMLHttpRequest
    const xhr = new XMLHttpRequest();

    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                console.log('Server Response:', xhr.responseText);
                alert('Form data sent successfully!');
            } else {
                console.error('Error:', xhr.statusText);
                alert('Error sending form data.');
            }
        }
    };

    // Send the JSON-formatted form data to the server
    console.log("TESTING:", JSON.stringify(formDataObject))
    xhr.send(JSON.stringify({ filteredData:formDataObject}));
}

$(document).ready(function() {
    // Event listener for strain name and mouse ID input fields
    $('#strain_name_create, #mouseID_create').on('input', function() {
        // Get the values of the strain name and mouse ID input fields
        var strainName = $('#strain_name_create').val();
        var mouseID = $('#mouseID_create').val();

        // Check if both fields are filled
        if (strainName && mouseID) {
            // Show the submit button
            $('#create-form-submit').parent().removeClass('hidden');
        } else {
            // Hide the submit button
            $('#create-form-submit').parent().addClass('hidden');
        }
    });
    
    // Event listener for strain name and mouse ID input fields
    $('#strain_name_update, #mouseID_update').on('input', function() {
        // Get the values of the strain name and mouse ID input fields
        var strainName = $('#strain_name_update').val();
        var mouseID = $('#mouseID_update').val();

        // Check if both fields are filled
        if (strainName && mouseID) {
            // Show the submit button
            $('#update-form-submit').parent().removeClass('hidden');
        } else {
            // Hide the submit button
            $('#update-form-submit').parent().addClass('hidden');
        }
    });

    console.log("Document ready. Starting execution...");

    // Populate the strain_name dropdown on page load
    populateStrainDropdown();

    function populateStrainDropdown() {
        console.log("Populating all strain dropdowns...");
    
        // Create a new XMLHttpRequest object
        const xhr = new XMLHttpRequest();
    
        xhr.open('GET', 'https://bioed.bu.edu/cgi-bin/students_24/mchang15/mchang15_testing4.py', true);
    
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    try {
                        console.log("XHR response received:", xhr.responseText);
    
                        // Parse the JSON response from the server
                        const jsonData = JSON.parse(xhr.responseText);
    
                        // Check if jsonData has the strain_names property
                        if (jsonData.hasOwnProperty('strain_names')) {
                            const strainNamesArray = jsonData.strain_names;
    
                            // Select all strain_name dropdown elements
                            const strainDropdowns = $('select[name="strain_name"]');
    
                            // Clear existing options in all dropdowns
                            strainDropdowns.empty();
    
                            // Add options for each strain name from the array to all dropdowns
                            strainNamesArray.forEach(function(name) {
                                strainDropdowns.append($('<option>', {
                                    value: name,
                                    text: name
                                }));
                            });
    
                            console.log("Dropdowns populated successfully.");
                        } else {
                            console.error("JSON data does not contain 'strain_names' property.");
                        }
                    } catch (error) {
                        console.error('Error parsing JSON:', error);
                    }
                } else {
                    console.error('Error fetching data. Status:', xhr.status);
                }
            }
        };
    
        // Send the GET request
        xhr.send();
    }


    console.log("Execution completed.");
});

function openBothFiles(){
  window.open('https://bioed.bu.edu/students_24/mchang15/upload_template_instructions.pdf', '_blank');
  window.open('https://bioed.bu.edu/students_24/mchang15/upload_template.xlsx', '_blank');
}




