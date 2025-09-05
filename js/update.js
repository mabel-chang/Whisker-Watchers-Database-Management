//BANNER TAB FUNCTIONS
function openTab(evt, tabName) {
  // URL of the HTML file you want to redirect to
  var newPageUrl = '../html/' + tabName + '.html';

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
document.addEventListener("DOMContentLoaded", function() {
    const selectDropdownU = document.getElementById("strain_name1");
    const selectDropdownC = document.getElementById("strain_name2");
    const inputText = document.getElementById("strain_name_input2");
    const submitContainerC = document.getElementById("submitContainer2");
    const submitContainerU = document.getElementById("submitContainer1");
    const fileInputC = document.getElementById('fileInput2');
    const fileInputU = document.getElementById('fileInput1');
    
    // Add event listeners to both input elements
    fileInputC.addEventListener("change", toggleSubmitButton);
    fileInputU.addEventListener("change", toggleSubmitButton);
    
    
    // Check if both preview is loaded and either strain_name or strain_name_input is filled
    function toggleSubmitButton() {
        const nameFilledC = selectDropdownC.value || inputText.value;
        const nameFilledU = selectDropdownU.value;

        if (nameFilledC) {
            submitContainerC.classList.remove('hidden'); // Show the submit button container
        } else {
            submitContainerC.classList.add('hidden'); // Hide the submit button container
        }
        if (nameFilledU) {
            submitContainerU.classList.remove('hidden'); // Show the submit button container
        } else {
            submitContainerU.classList.add('hidden'); // Hide the submit button container
        }
    }

    // Call toggleSubmitButton initially to check the initial state
    toggleSubmitButton();
    
    // Add event listeners to both input elements
    selectDropdownC.addEventListener("input", function() {
        if (selectDropdownC.value != '') {
            inputText.disabled = true;
            inputText.value = ""; // Clear the input text if dropdown is selected
        } else {
            inputText.disabled = false;
        }
    });

    inputText.addEventListener("input", function() {
        if (inputText.value) {
            selectDropdownC.disabled = true;
            selectDropdownC.selectedIndex = 0; // Reset dropdown to default if input text is filled
        } else {
            selectDropdownC.disabled = false;
        }
    });
    
    const selectDropdownDel = document.getElementById("strain_name_del");
    const mouseIDsInput = document.getElementById("mouseIDs");
    const deleteContainer = document.getElementById("deleteContainer");

    // Add event listeners to both input elements
    selectDropdownDel.addEventListener("input", toggleDeleteButton);
    mouseIDsInput.addEventListener("input", toggleDeleteButton);

    // Check if both strain_name and mouseIDs are filled
    function toggleDeleteButton() {
        const strainName = selectDropdownDel.value;
        const mouseIDs = mouseIDsInput.value.trim();

        if (strainName && mouseIDs) {
            deleteContainer.classList.remove('hidden'); // Show the delete button container
        } else {
            deleteContainer.classList.add('hidden'); // Hide the delete button container
        }
    }

    // Call toggleDeleteButton initially to check the initial state
    toggleDeleteButton();
});

function openBothFiles(type){
    if (type == 'update'){
        window.open('../assets/upload_template_instructions.pdf', '_blank');
        window.open('../assets/upload_template.xlsx', '_blank');
    } else if (type == 'create'){
        window.open('../assets/create_template_instructions.pdf', '_blank');
        window.open('../assets/create_template.xlsx', '_blank');
    }
}

//EXCEL SHEET
function previewExcel(fileElm, type) {
    const fileInput = document.getElementById(fileElm);
    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function (e) {
        const data = e.target.result;
        const lines = data.split(/\r\n|\n/);
        let tableHtml = '<table class="preview-table">';
        
        lines.forEach(line => {
            tableHtml += '<tr>';
            const cells = line.split(',');
            cells.forEach(cell => {
                tableHtml += `<td>${cell}</td>`;
            });
            tableHtml += '</tr>';
        });

        tableHtml += '</table>';
        
        const previewDiv = document.getElementById(type);
        previewDiv.innerHTML = tableHtml;
    };

    reader.readAsText(file);
}

function submitForm(url, type) {
    console.log(type);
    let form = '';
    let strainDropdownValue = '';
    let inputTextValue = '';
    let previewDiv = '';
    let submitContainer = '';
    let strainDropdown = '';
    let inputText = '';
    if (type == 'update'){
        form = document.getElementById('uploadForm1');
        strainDropdownValue = document.getElementById('strain_name1').value;
        previewDiv = document.getElementById('preview1');
        submitContainer = document.getElementById('submitContainer1');
    } else if (type == 'create'){
        form = document.getElementById('uploadForm2');
        strainDropdown = document.getElementById('strain_name2');
        strainDropdownValue = document.getElementById('strain_name2').value;
        previewDiv = document.getElementById('preview2');
        inputText = document.getElementById('strain_name_input2');
        inputTextValue = document.getElementById('strain_name_input2').value;
        submitContainer = document.getElementById('submitContainer2');
    }
    
    const formData = new FormData(form);

    // Check if either the dropdown or input text is filled
    if (strainDropdownValue) {
        formData.append('strainName', strainDropdownValue);
    } else if (inputTextValue) {
        formData.append('strainName', inputTextValue);
    } else {
        console.error('Both strain name fields are empty!');
        return; // Exit the function if both fields are empty
    }
    
    console.log("Strain Name:", formData.get('strainName'));

    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        console.log(data); // Show response from the server
    })
    .catch(error => console.error('Error:', error));
    
    form.reset();
    previewDiv.innerHTML = '';
    submitContainer.classList.add('hidden');
    strainDropdown.disabled = false;
    inputText.disabled = false;
}

function deleteData() {
    const mouseIDsInput = document.getElementById("mouseIDs").value.trim();
    const mouseIDs = mouseIDsInput.split(",").map(id => id.trim());
    const strainName = document.getElementById("strain_name_del").value;

    console.log('Data to delete:', mouseIDs);
    console.log('Strain Name:', strainName);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '../cgi-bin/upload_delete.py', true);
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

    xhr.send(JSON.stringify({ strainName: strainName, mouseIDs: mouseIDs }));
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
    xhr.send(JSON.stringify(formDataObject));
}

$(document).ready(function() {
   console.log("Document ready. Starting execution...");

   // Populate the strain_name dropdown on page load
   populateStrainDropdown();

   function populateStrainDropdown() {
       console.log("Populating all strain dropdowns...");
   
       // Create a new XMLHttpRequest object
       const xhr = new XMLHttpRequest();
   
       xhr.open('GET', '../cgi-bin/strain_autopopulate.py', true);
   
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
                           
                           strainDropdowns.append($('<option>'));
   
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

