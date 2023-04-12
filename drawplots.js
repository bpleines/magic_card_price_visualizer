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

renderScatterplot('ONE')

function renderScatterplot(attribute_code, attribute_type='set') {
  // Clean out existing plot and plotted points
  var noData = [''];
  d3.select("#my_dataviz")
    .selectAll("g")
    .data(noData)
    .exit()
    .remove();
  document.getElementById("title").innerHTML = 'Magic the Gathering Rares ('.concat(attribute_code).concat(') : Price by Mana Cost and Color');

  var attribute = (attribute_type === 'set') ? 'set' : 'color'
  var csvFilePath = "https://raw.githubusercontent.com/bpleines/magic_card_price_visualizer/main/magic_card_csv_files_by_".concat(attribute).concat("/").concat(attribute_code).concat(".csv");
  //Read the data
  d3.csv(csvFilePath, function(d) {
      // Convert all str csv values to ints
      d.cmc = +d.cmc;
      d.price = +d.price;
      return d;
    }).then(function(data) {
      // Get the max of both cmc and price and pad each dimension
      var max_cmc = d3.max(data, function(d) { return d.cmc + 1; });
      var max_price = d3.max(data, function(d) { return d.price * 1.10; });

      // Add X axis
      var xscale = d3.scaleLinear()
	.domain([0, max_cmc])
	.range([0, width]);
      svg.append("g")
	.attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(xscale));

      // Add Y axis
      var yscale = d3.scaleLinear()
	.domain([0, max_price])
	.range([height, 0]);
      svg.append("g")
	.call(d3.axisLeft(yscale));

      // Labels
      var xAxisCall = d3.axisBottom(xscale)
      var xAxis = svg.append("g")
		   .attr("id", "x-axis")
		   .attr("class", "x-axis")
		   .attr("transform", "translate(" + 0 + "," + height + ")")
		   .call(xAxisCall);

      var yAxisCall = d3.axisLeft(yscale);
      var yAxis = svg.append("g")
		   .attr("id", "y-axis")
		   .attr("class", "y-axis")
		   .call(yAxisCall);

      // Add Labels
      d3.select("#my_dataviz")
	.selectAll("g")
	.data(data)
	.transition()
	.duration(500)
	.attr("fill", "#000000");;

      xAxis.append("text")
	   .attr("class", "axis-title")
	   .attr("transform", "translate(" + width + ", 0)")
	   .attr("x", -106)
	   .attr("y", -16)
	   .text("Mana Value");
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
	     .attr("cx", function (d) { return xscale(d.cmc); } )
	     .attr("cy", function (d) { return yscale(d.price); } )
	     .attr("r", 6.0)
	     .style("fill", function (d) { return d.color; })
	     .style("stroke", "black")
	     .on('mouseover', function (event, d) {
		  d3.select(this).transition()
		      .duration('100')
		      .attr("r", 15);
		  // Add the image to the page when plot point is hovered over
		  console.log("d.image: ".concat(d.image));
                  console.log("d.color: ".concat(d.color));
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
