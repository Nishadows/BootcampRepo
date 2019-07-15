// @TODO: YOUR CODE HERE!
var svgWidth = 950;
var svgHeight = 600;

var margin ={
    top: 20,
    right: 20,
    bottom: 60,
    left: 50
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom - 20;

var svg = d3.select("#scatter")
.append("svg")
.attr("width",svgWidth)
.attr("height", svgHeight);

var chartGroup = svg.append("g")
.attr("transform", `translate(${margin.top},${margin.left})`);

d3.csv("assets/data/data.csv").then(function(statedata){

    var xValue = function(d) { return +d.poverty;};

    var xScale = d3.scaleLinear()
    .domain([d3.min(statedata, d => +d.poverty)-1,d3.max(statedata, d => +d.poverty)+1])
    .range([0,width]);

    var xMap = function(d){
        return xScale(xValue(d));
    };

    var yValue = function(d) {return +d.healthcare;};

    var yScale = d3.scaleLinear()
    .domain([d3.min(statedata, d => +d.healthcare)-1, d3.max(statedata, d => +d.healthcare)+1])
    .range([height, 0]);

    var yMap = function(d){
        return yScale(yValue(d));    
    };

    chartGroup.selectAll("g").data(statedata)
    .enter()   
    .append("circle")
    .attr("r", 10)
    .attr("cx",xMap)
    .attr("cy",yMap)
    .style("fill","#67a8d6");

    chartGroup.selectAll("g").data(statedata)
    .enter()    
    .append("text")
    .text(d => d.abbr)
    .attr("x", xMap)
    .attr("y", yMap)
    .attr("text-anchor", "middle")
    .attr("dominant-baseline","middle")
    .attr("font-weight", "bold")
    .attr("font-size", "10px")
    .style("fill", "#ffffff"); 

    var bottomAxis = d3.axisBottom(xScale);
    var leftAxis = d3.axisLeft(yScale);

    chartGroup.append("g").attr("transform", `translate(${margin.left}, ${height})`)
    .call(bottomAxis)

    chartGroup.append("g").attr("transform", `translate(${margin.left}, 0)`)
    .call(leftAxis)
    
    chartGroup.append("text")
    .attr("transform", `translate(${width / 2}, ${height + margin.top + 20})`)
    .attr("text-anchor", "middle")
    .attr("font-size", "16px")
    .attr("font-weight", "bold")
    .attr("fill", "black")
    .text("In Poverty (%)");

    chartGroup.append("text")
    .attr("transform", [`translate(0, ${height/2})`,"rotate(-90)"])
    .attr("text-anchor", "middle")
    .attr("font-size", "16px")
    .attr("font-weight", "bold")
    .attr("fill", "black")
    .text("Lack of Healthcare (%)");

});


