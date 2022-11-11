// set the dimensions and margins of the graph
var margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = 1030 - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#my_dataviz")
            .append("svg")
              .attr("width", width + margin.left + margin.right)
              .attr("height", height + margin.top + margin.bottom)
            .append("g")
              .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");

renderScatterplot('DMU')

function renderScatterplot(attribute_code, attribute_type='set') {
  // Clean out existing plot and plotted points
  var noData = [''];
  d3.select("#my_dataviz")
    .selectAll("circle")
    .data(noData)
    .exit()
    .remove();
  d3.select("#my_dataviz")
    .selectAll("g")
    .data(noData)
    .exit()
    .remove();
  document.getElementById("title").innerHTML = 'Magic the Gathering Rares ('.concat(attribute_code).concat(') : Price by Mana Cost and Color');

  var attribute = (attribute_type === 'set') ? 'set' : 'color'
  var csvFilePath = "https://raw.githubusercontent.com/bpleines/data_vis/main/magic_card_csv_files_by_".concat(attribute).concat("/").concat(attribute_code).concat(".csv");
  //Read the data
  d3.csv(csvFilePath, function(data) {
    // Convert all str csv values to ints
    data.forEach(function(d) {
      d.cmc = +d.cmc;
      d.price = +d.price;
    });
    // Get the max of both cmc and price and pad each dimension
    var max_cmc = d3.max(data, function(d) { return d.cmc; }) + 1;
    var max_price = d3.max(data, function(d) { return d.price; }) + 2;

    // Add X axis
    var x = d3.scaleLinear()
      .domain([0, max_cmc])
      .range([ 0, width ]);
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
      .domain([0, max_price])
      .range([ height, 0]);
    svg.append("g")
      .call(d3.axisLeft(y));

    // Labels
    var xAxisCall = d3.axisBottom(x)
    var xAxis = svg.append("g")
                 .attr("class", "x-axis")
                 .attr("transform", "translate(" + 0 + "," + height + ")")
                 .call(xAxisCall);

    var yAxisCall = d3.axisLeft(y);
    var yAxis = svg.append("g")
                 .attr("class", "y-axis")
                 .call(yAxisCall);

    // Add Labels
    d3.select("#my_dataviz")
      .selectAll("g")
      .data(data)
      .transition()
      .duration(1000)
      .attr("fill", "#000000");;

    xAxis.append("text")
         .attr("class", "axis-title")
         .attr("transform", "translate(" + width + ", 0)")
         .attr("x", -106)
         .attr("y", -16)
         .text("Converted Mana Cost");
    yAxis.append("text")
         .attr("class", "axis-title")
         .attr("transform", "rotate(-90)")
         .attr("y", 24)
         .text("Price (USD)");

    // Add dots
    var markers = svg.append('g')
                     .selectAll("dot")
                     .data(data);

    markers.enter()
           .append("circle")
	   .attr("cx", function (d) { return x(d.cmc); } )
	   .attr("cy", function (d) { return y(d.price); } )
           .attr("r", 6.0)
           .style("fill", function (d) { return d.color; })
           .style("stroke", "black")
           .on('mouseover', function (d, i) {
                d3.select(this).transition()
                    .duration('100')
                    .attr("r", 10);
                // Add the image to the page when plot point hovered over
                src = d.image;
                img = document.createElement("img");
                img.src = src;
                document.getElementById("card_picture").appendChild(img);
           })
           .on('mouseout', function (d, i) {
               d3.select(this).transition()
                   .duration('200')
                   .attr("r", 6);
               // remove image from page when hover off
               document.getElementById("card_picture").removeChild(img);
           });
  })
}
