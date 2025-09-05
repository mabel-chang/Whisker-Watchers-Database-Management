//BANNER TAB FUNCTIONS
function openTab(evt, tabName) {
  // URL of the HTML file you want to redirect to
  var newPageUrl = '../html/' + tabName + '.html';

  // Redirect to the new page
  window.location.href = newPageUrl;
}

// Function to submit filter form and display filtered table
function submitFilterForm() {
    var form = document.getElementById("filter-form");
    var formData = new FormData(form);

    // Make AJAX request to fetch filtered data
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "../cgi-bin/filter.py?" + new URLSearchParams(formData).toString(), true);
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

// Function to reset filters and reload the page
function resetFilters() {
    // Reset form fields
    var form = document.getElementById("filter-form");
    form.reset();
   

    // Reset table container
    var tableContainer = document.querySelector(".table-container");
    tableContainer.innerHTML = "";
    
    // Reset download options
    resetDownloadOptions();
    resetDownloadProtocol();
}

function resetDownloadOptions() {
    // Reset file format selection
    document.getElementById("file-format").selectedIndex = 0;

    // Hide download options container
    document.querySelector(".download-options-container").style.display = "none";
}

function resetDownloadProtocol() {
    // Hide download protocol container
    document.querySelector(".download-protocol-container").style.display = "none";
}

// Function to show filter options when "View Table" button is clicked
function showFilterOptions() {
    var filterOptions = document.getElementById("filter");
    filterOptions.style.display = "block";
}

// Function to view table based on selected table in dropdown
function viewTable() {
    var selectedTable = document.getElementById("tables").value;
    if (selectedTable) {
        var form = new FormData();
        form.append("selected_table", selectedTable);

        var xhr = new XMLHttpRequest();
        xhr.open("GET", "../cgi-bin/filter.py?" + new URLSearchParams(form).toString(), true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                // Create a new table element and append it to the table container
                var tableContainer = document.querySelector(".table-container");
                var newTable = document.createElement("table");
                newTable.innerHTML = xhr.responseText;
                tableContainer.innerHTML = ""; // Clear existing content
                tableContainer.appendChild(newTable);

                var downloadOptionsContainer = document.querySelector(".download-options-container");
                downloadOptionsContainer.style.display = "block"; // Added: Display download options
            }
        };
        xhr.send();
    } else {
        // Handle error when no table is selected
        alert("Please select a table before viewing.");
    }
    
    updateDownloadButton(selectedTable);
}

// Function to download filtered table in selected format
function downloadFilteredTable() {
    var fileFormat = document.getElementById("file-format").value;
    var selectedTableIndex = document.getElementById("tables").selectedIndex; // Get the index of the selected table
    var selectedTableName = document.getElementById("tables").options[selectedTableIndex].text; // Get the text (name) of the selected table
    var table = document.querySelector(".table-container table"); // Get the current table content

    // Generate download link based on selected format and selected table name
    var downloadLink;
    if (fileFormat === "csv") {
        downloadLink = generateCsv(table, selectedTableName);
    } else if (fileFormat === "excel") {
        downloadLink = generateExcel(table, selectedTableName);
    } else if (fileFormat === "txt") {
        downloadLink = generateTxt(table, selectedTableName);
    } 
    
    // Trigger download
    downloadLink.click();
}

// Function to generate CSV file and return download link
function generateCsv(table, selectedTableName) {
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
    link.setAttribute("download", selectedTableName + ".csv");
    return link;
}

// Function to generate Excel file and return download link
function generateExcel(table, selectedTableName) {
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
    link.setAttribute("download", selectedTableName + ".xls");
    return link;
}

// Function to generate Text file and return download link
function generateTxt(table, selectedTableName) {
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
    link.setAttribute("download", selectedTableName + ".txt");
    return link;
}

function updateDownloadButton(selectedTable) {
    var downloadButton = document.getElementById("download-button");
    var protocolName = document.getElementById("protocol-name");
    var protocolContainer = document.querySelector(".download-protocol-container");
    
    if (selectedTable === "FAT-1") {
        downloadButton.setAttribute("style", "display: block;");
        downloadButton.setAttribute("onclick", "downloadProtocol('GT-Fat-1.docx')");
        protocolName.innerText = "GT-Fat-1.docx";
        protocolContainer.style.display = "block"; // Display the protocol download container
    } else if (selectedTable === "Sm22-rtTA; TetO-Cre; mTmG") {
        downloadButton.setAttribute("style", "display: block;");
        downloadButton.setAttribute("onclick", "downloadProtocol('GT-protocol-rtTA-Cre-mTmG.docx')");
        protocolName.innerText = "GT-protocol-rtTA-Cre-mTmG.docx";
        protocolContainer.style.display = "block"; // Display the protocol download container
    } else if (selectedTable === "Sm22-rtTA; TetO-Cre; mTmG; Mrtf") {
        downloadButton.setAttribute("style", "display: block;");
        downloadButton.setAttribute("onclick", "downloadProtocol('Genotyping-MRTFA-LayneLab[22].docx')");
        protocolName.innerText = "Genotyping-MRTFA-LayneLab[22].docx";
        protocolContainer.style.display = "block"; // Display the protocol download container
    } else {
        downloadButton.setAttribute("style", "display: none;");
        protocolName.innerText = "";
        protocolContainer.style.display = "none"; // Hide the protocol download container if none of the specific tables are selected
    }
}


function downloadProtocol(protocolFileName) {
    var protocolUrl = "../" + protocolFileName;
    var downloadLink = document.createElement("a");
    downloadLink.href = protocolUrl;
    downloadLink.download = protocolFileName;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}


