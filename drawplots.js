// set the dimensions and margins of the graph
var margin = {top: 10, right: 30, bottom: 60, left: 80},
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

renderScatterplot('ONE')

function renderScatterplot(attribute_code, attribute_type='set') {
  // Clean out existing plot and plotted points
  var noData = [''];
  d3.select("#my_dataviz")
    .selectAll("g")
    .data(noData)
    .exit()
    .remove();
  document.getElementById("title").innerHTML = 'Magic the Gathering Rares ('.concat(attribute_code).concat(') : Price by Mana Value and Color');

  var attribute = (attribute_type === 'set') ? 'set' : 'color'
  var csvFilePath = "https://raw.githubusercontent.com/bpleines/magic_card_price_visualizer/main/magic_card_csv_files_by_".concat(attribute).concat("/").concat(attribute_code).concat(".csv");
  // Read the data
  d3.csv(csvFilePath, function(d) {
      // Convert all str csv values to ints
      d.cmc = +d.cmc;
      d.price = +d.price;
      return d;
    }).then(function(data) {
      // Get the max of both cmc and price and pad each dimension
      var max_cmc = d3.max(data, function(d) { return d.cmc + 1; });
      var max_price = d3.max(data, function(d) { return d.price * 1.10; });

      // Create x axis scale
      var x = d3.scaleLinear()
	.domain([0, max_cmc])
	.range([0, width]);

      // Create y axis scale
      var y = d3.scaleLinear()
	.domain([0, max_price])
	.range([height, 0]);

      // Create x and y axes
      var xAxisCall = d3.axisBottom(x);
      var xAxis = svg.append("g")
		   .attr("id", "x-axis")
		   .attr("class", "x-axis")
		   .attr("transform", "translate(" + 0 + "," + height + ")")
		   .call(xAxisCall)
                   .selectAll("text")
                     .style("font-size", 20);

      var yAxisCall = d3.axisLeft(y);
      var yAxis = svg.append("g")
		   .attr("id", "y-axis")
		   .attr("class", "y-axis")
		   .call(yAxisCall)
                   .selectAll("text")
                     .style("font-size", 20);

      d3.select("#my_dataviz")
	.selectAll("g")
	.data(data)
	.transition()
	.duration(500)
	.attr("fill", "#000000");

      // Add labels
      svg.append("text")
         .attr("text-anchor", "end")
         .attr("x", Math.floor(width / 1.8))
         .attr("y", height + margin.top + 30)
         .text("Mana Value");
      svg.append("text")
         .attr("text-anchor", "end")
         .attr("transform", "rotate(-90)")
         .attr("y", -margin.left + 30)
         .attr("x", Math.floor(-height / 2.4))
         .text("Price (USD)")

      // Add dots
      var markers = svg.append('g')
		       .selectAll("dot")
		       .data(data);

      let img;
      let src
      markers.enter()
	     .append("circle")
	     .attr("cx", function (d) { return x(d.cmc); } )
	     .attr("cy", function (d) { return y(d.price); } )
	     .attr("r", 6.0)
	     .style("fill", function (d) { return d.color; })
	     .style("stroke", "black")
	     .on('mouseover', function (event, d) {
		  d3.select(this).transition()
		      .duration('100')
		      .attr("r", 15);
		  // Add the image to the page when plot point is hovered over
                  src = d.image;
		  img = document.createElement("img");
		  img.src = src;
		  document.getElementById("card_picture").appendChild(img);
	     })
	     .on('mouseout', function (event, d) {
		 d3.select(this).transition()
		     .duration('200')
                   .attr("r", 6);
                 // remove image from page when hover off
                 document.getElementById("card_picture").removeChild(img);
             });
  })
}
