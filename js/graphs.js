//BANNER TAB FUNCTIONS
function openTab(evt, tabName) {
  // URL of the HTML file you want to redirect to
  var newPageUrl = '../html/' + tabName + '.html';

  // Redirect to the new page
  window.location.href = newPageUrl;
}

function drawChart(data) {
    google.charts.load('current', { packages: ['corechart'] });
    google.charts.setOnLoadCallback(drawChart);

    var chartData = [['Group', 'Frequency']];
    var groups = {};

    var selectedGroup1 = document.getElementById('group1').value;
    var selectedGroup2 = document.getElementById('group2').value;

    if (selectedGroup1 === selectedGroup2 && selectedGroup1 !== "" && selectedGroup2 !== "") {
       alert("Please select different grouping variables.");
       return;
    }

    // Iterate through the data to group items by their labels
    data.forEach(function(item) {
        var label = '';

        // Construct label based on available grouping variables
        if (selectedGroup1 && item.hasOwnProperty(selectedGroup1)) {
            label += item[selectedGroup1];
        }

        if (selectedGroup2 && item.hasOwnProperty(selectedGroup2)) {
            label += ' ' + item[selectedGroup2];
        }

        // If the group doesn't exist yet, create it
        if (!groups[label]) {
            groups[label] = 0;
        }
        
        // Increment the count for the group
        groups[label] += item['count'];
    });

    // Convert the groups object into chart data
    for (var group in groups) {
        chartData.push([group, groups[group]]);
    }
    
    console.log('Chart Data:', chartData); // Log the chart data

    var dataTable = google.visualization.arrayToDataTable(chartData);
    
    console.log('Data Table:', dataTable); // Log the chart data
    
    var chartType = document.getElementById('chartType').value;

    var options = {
        title: (selectedGroup1 || selectedGroup2) ? ('Mouse count by ' + selectedGroup1 + (selectedGroup2 ? ' and ' + selectedGroup2 : '')) : 'Total mice count',
        vAxis: {title: 'Mouse count'},
        hAxis: {title: selectedGroup1},
        isStacked: true,
        legend: { position: 'right' }, // Show legend on the right side
        colors: ['#3366CC', '#DC3912', '#FF9900', '#109618', '#990099', '#0099C6', '#DD4477', '#66AA00'], // Customize colors
    };

    var chart;
    if (chartType === 'bar') {
        chart = new google.visualization.ColumnChart(document.getElementById('chart'));
    } else {
        chart = new google.visualization.PieChart(document.getElementById('chart'));
    }

    google.visualization.events.addListener(chart, 'ready', function () {
        // Change the download link href attribute to the chart's image URI
        var chartImageURI = chart.getImageURI();
        document.getElementById("download_link").setAttribute("href", chartImageURI);
        // Set the download attribute to the chart title
        var chartTitle = options.title.replace(/[^a-z0-9]/gi, '_').toLowerCase(); // Clean title for filename
        document.getElementById("download_link").setAttribute("download", chartTitle + ".png");
    });

    chart.draw(dataTable, options);

    // Show download options container
    document.getElementById('downloadContainer').style.display = 'block';
}


function GenerateChart() {
    var form = document.getElementById("mouseFrequencyForm");
    var formData = new FormData(form);

    fetch(form.action + "?" + new URLSearchParams(formData), {
        method: 'GET', // Use GET method
    })
    .then(response => response.json())
    .then(data => {
        drawChart(data); // Pass data to drawChart function
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("generateChartBtn").addEventListener("click", function() {
        GenerateChart();
    });

    document.getElementById("resetFiltersBtn").addEventListener("click", function() {
        // Reset all form elements
        document.getElementById("mouseFrequencyForm").reset();
        // Reset chart if it's already drawn
        document.getElementById('chart').innerHTML = '';
    });
});

document.getElementById("downloadChartBtn").addEventListener("click", function() {
    // Trigger the download
    document.getElementById("download_link").click();
});


// Add the download link with an initial href attribute
document.getElementById("download_link").setAttribute("href", "/");

$(document).ready(function() {
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
