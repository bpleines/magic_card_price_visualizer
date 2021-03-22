mtg_set_codes = ['STX', 'KHM', 'ZNR', 'IKO', 'THB', 'ELD', 'WAR', 'RNA', 'GRN', 'DOM', 'RIX',
                 'XLN', 'HOU', 'AKH', 'AER', 'KLD', 'EMN', 'SOI', 'OGW', 'BFZ', 'DTK', 'FRF',
                 'KTK', 'JOU', 'BNG', 'THS', 'DGM', 'GTC', 'RTR', 'AVR', 'DKA', 'ISD', 'NPH',
                 'MBS', 'SOM', 'ROE', 'WWK', 'ZEN', 'ARB', 'CON', 'ALA', 'EVE', 'SHM', 'MOR',
                 'LRW', 'FUT', 'PLC', 'TSP', 'CSP', 'DIS', 'GPT', 'RAV', 'SOK', 'BOK', 'CHK',
                 '5DN', 'DST', 'MRD', 'SCG', 'LGN', 'ONS', 'JUD', 'TOR', 'ODY'];

function renderTimeseriesScatterplot(attribute_code, attribute_type='set') {
  document.getElementById("title").innerHTML = 'Magic the Gathering Rares: Price by Time';
  
  var attribute = (attribute_type === 'set') ? 'set' : 'color'
  var csvFilePath = "https://raw.githubusercontent.com/bpleines/data_vis/main/magic_card_csv_files_by_".concat(attribute).concat("/").concat(attribute_code).concat(".csv");
  //Read the data
  d3.csv(csvFilePath, function(data) {
    // Convert all str csv values to ints
    data.forEach(function(d) {
      d.cmc = +d.cmc;
      d.price = +d.price;
    });
    // Get the max of both cmc and price and pad each dimension by 1
    var max_cmc = 15;
    var max_price = 100; 
    // Add X axis
    var x = d3.scaleLinear()
      .domain([0, max_cmc])
      .range([0, width]);
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
      .domain([0, max_price])
      .range([height, 0]);
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
           .attr("r", 3.0)
           .style("opacity", 1)
           .style("fill", "#000000")
           .style("stroke", "black");

    d3.select("#my_dataviz")
      .data(data)
      .transition()
      .duration(1000) 
      .style("fill", function (d) { return d.color; })
      .style("opacity", 1);

    d3.select("#my_dataviz")
      .selectAll("circle")
      .data(data)
      .transition()
      .duration(1000)
      .attr("fill", "#000000");

    d3.select("#my_dataviz")
      .selectAll("g")
      .data(data)
      .transition()
      .duration(1000)
      .attr("fill", "#000000");
  })
}

function populateTimeseries() {
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
  for (i = 0; i < mtg_set_codes.length; i++) {
    renderTimeseriesScatterplot(mtg_set_codes[i]);
  }
}
