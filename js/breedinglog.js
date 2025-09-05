//BANNER TAB FUNCTIONS
function openTab(evt, tabName) {
  // URL of the HTML file you want to redirect to
  var newPageUrl = '../html/' + tabName + '.html';

  // Redirect to the new page
  window.location.href = newPageUrl;
}

// Function to fetch unfiltered table when the page loads
function fetchUnfilteredTable() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "../cgi-bin/breedinglog.py", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // Display unfiltered table
            var tableContainer = document.querySelector(".table-container");
            tableContainer.innerHTML = xhr.responseText;
        }
    };
    xhr.send();
}

// Function to submit filter form and display filtered table
function submitFilterForm() {
    var form = document.getElementById("filter-form");
    var formData = new FormData(form);

    // Make AJAX request to fetch filtered data
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "../cgi-bin/breedinglog.py?" + new URLSearchParams(formData).toString(), true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // Update table content with filtered data
            var tableContainer = document.querySelector(".table-container");
            var newTable = document.createElement("table");
            newTable.innerHTML = xhr.responseText;
            tableContainer.innerHTML = ""; // Clear existing content
            tableContainer.appendChild(newTable);
        }
    };
    xhr.send();
}

window.addEventListener('load', function() {
        submitFilterForm();
    });

// Function to reset filters and reload the page
function resetFilters() {
    // Reset form fields
    var form = document.getElementById("filter-form");
    form.reset();
    
    // Reload unfiltered table
    fetchUnfilteredTable();
}

// Function to download filtered table in selected format
function downloadFilteredTable() {
    var fileFormat = document.getElementById("file-format").value;
    var table = document.querySelector(".table-container table"); // Get the current table content

    // Generate download link based on selected format and selected table name
    var downloadLink;
    if (fileFormat === "csv") {
        downloadLink = generateCsv(table);
    } else if (fileFormat === "excel") {
        downloadLink = generateExcel(table);
    } else if (fileFormat === "txt") {
        downloadLink = generateTxt(table);
    } 
    
    // Trigger download
    downloadLink.click();
}

// Function to generate CSV file and return download link
function generateCsv(table) {
    var csvData = [];
    var rows = table.querySelectorAll("tr");
    rows.forEach(function (row) {
        var rowData = [];
        row.querySelectorAll("td, th").forEach(function (cell) {
            rowData.push(cell.innerText);
        });
        csvData.push(rowData.join(","));
    });
    var csvContent = "data:text/csv;charset=utf-8," + csvData.join("\n");
    var encodedUri = encodeURI(csvContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "breedinglog.csv");
    return link;
}

// Function to generate Excel file and return download link
function generateExcel(table) {
    var excelData = "<table>";
    var rows = table.querySelectorAll("tr");
    rows.forEach(function (row) {
        excelData += "<tr>";
        row.querySelectorAll("td, th").forEach(function (cell) {
            excelData += "<td>" + cell.innerText + "</td>";
        });
        excelData += "</tr>";
    });
    excelData += "</table>";
    var excelContent = "data:application/vnd.ms-excel;charset=utf-8," + encodeURIComponent(excelData);
    var link = document.createElement("a");
    link.setAttribute("href", excelContent);
    link.setAttribute("download", "breedinglog.xls");
    return link;
}

// Function to generate Text file and return download link
function generateTxt(table) {
    var txtData = [];
    var rows = table.querySelectorAll("tr");
    rows.forEach(function (row) {
        var rowData = [];
        row.querySelectorAll("td, th").forEach(function (cell) {
            rowData.push(cell.innerText);
        });
        txtData.push(rowData.join("\t"));
    });
    var txtContent = "data:text/plain;charset=utf-8," + txtData.join("\n");
    var link = document.createElement("a");
    link.setAttribute("href", txtContent);
    link.setAttribute("download", "breedinglog.txt");
    return link;
}

$(document).ready(function() {
    console.log("Document ready. Starting execution...");

    // Populate the strain_name dropdown on page load
    populateStrainDropdown();

    function populateStrainDropdown() {
        console.log("Populating all strain dropdowns...");
    
        // Create a new XMLHttpRequest object
        const xhr = new XMLHttpRequest();
    
        xhr.open('GET', '../cgi-bin/upload_testing_mabel4.py', true);
    
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

// Execute when the page loads
window.addEventListener('load', function() {
    fetchUnfilteredTable();
});
