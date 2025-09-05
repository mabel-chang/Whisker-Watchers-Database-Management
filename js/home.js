//BANNER TAB FUNCTIONS
function openTab(evt, tabName) {
  // URL of the HTML file you want to redirect to
  var newPageUrl = '../html/' + tabName + '.html';

  // Redirect to the new page
  window.location.href = newPageUrl;
}

function logout() {
    // URL of the sign-in page
    var signInPageUrl = '../html/sign_in.html';

    // Redirect to the sign-in page
    window.location.href = signInPageUrl;
}


google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawCharts);

    function drawCharts() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '../cgi-bin/home.py', true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var counts = JSON.parse(xhr.responseText);

                // Calculate the total count
                var totalCount = counts.reduce((acc, count) => acc + count, 0);

                var options = {
                    titleTextStyle: {
                        fontSize: 14,
                        textAlign: 'center'
                    },
                    titlePosition: 'center',
                    pieSliceText: 'value',
                    legend: 'none',
                    pieSliceTextStyle: {
                        fontSize: 25
                    }
                };

                var data1 = google.visualization.arrayToDataTable([
                    ['Category', 'Count'],
                    ['Total Mice', counts[0]]
                ]);
                var options1 = Object.assign({}, options);
                options1.title = 'ColSMA';

                var data2 = google.visualization.arrayToDataTable([
                    ['Category', 'Count'],
                    ['Total Mice', counts[1]]
                ]);
                var options2 = Object.assign({}, options);
                options2.title = 'Sm22-rtTA; TetO-Cre; mTmG; Mrtf';

                var data3 = google.visualization.arrayToDataTable([
                    ['Category', 'Count'],
                    ['Total Mice', counts[2]]
                ]);
                var options3 = Object.assign({}, options);
                options3.title = 'FAT-1';
                
                 var data5 = google.visualization.arrayToDataTable([
                    ['Category', 'Count'],
                    ['Total Mice', counts[3]]
                ]);
                var options5 = Object.assign({}, options);
                options5.title =  'Sm22-rtTA; TetO-Cre; mTmG';

                var data4 = google.visualization.arrayToDataTable([
                    ['Category', 'Count'],
                    ['Total Mice', totalCount] // Use the total count for the fourth chart
                ]);
                var options4 = Object.assign({}, options);
                options4.title = 'Total alive mice currently in lab';
                options4.colors = ['#e74c3c'];  

                var chart1 = new google.visualization.PieChart(document.getElementById('chart1'));
                chart1.draw(data1, options1);

                var chart2 = new google.visualization.PieChart(document.getElementById('chart2'));
                chart2.draw(data2, options2);

                var chart3 = new google.visualization.PieChart(document.getElementById('chart3'));
                chart3.draw(data3, options3);

                var chart4 = new google.visualization.PieChart(document.getElementById('chart4'));
                chart4.draw(data4, options4);
                
                var chart5 = new google.visualization.PieChart(document.getElementById('chart5'));
                chart5.draw(data5, options5);
            }
        };
        xhr.send();
    }