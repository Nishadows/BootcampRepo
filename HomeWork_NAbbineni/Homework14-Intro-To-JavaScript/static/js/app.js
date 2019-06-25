// from data.js
var inputValue = "";

// YOUR CODE HERE!
function filterResults(inputDate){
    var tableData = data;
    var tbody = d3.select("#ufo-table").select("tbody");
    var rows = tbody.selectAll("tr").remove();

    tableData.forEach(function(d) {
        if (d.datetime == inputDate || !inputDate){
            console.log(d);
            var row = tbody.append("tr");

            Object.entries(d).forEach(function([key, value]) {
              console.log(key, value);
              var cell = row.append("td");
              cell.text(value);
            });
        };    
    });
};

// Select the submit button
var submit = d3.select("#filter-btn");

submit.on("click", function() {

  // Prevent the page from refreshing
  d3.event.preventDefault();

  // Select the input element and get the raw HTML node
  var inputElement = d3.select("#datetime");

  // Get the value property of the input element
  var inputValue = inputElement.property("value");

  console.log(inputValue);

  filterResults(inputValue); 

});


filterResults(inputValue);