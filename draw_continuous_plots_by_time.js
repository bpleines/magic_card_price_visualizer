let mtg_set_codes;
mtg_set_codes = ['BRO', 'DMU', 'SNC', 'NEO', 'VOW', 'MID', 'AFR',
                'STX', 'KHM', 'ZNR', 'IKO', 'THB', 'ELD', 'WAR', 'RNA', 'GRN', 'DOM', 'RIX',
                'XLN', 'HOU', 'AKH', 'AER', 'KLD', 'EMN', 'SOI', 'OGW', 'BFZ', 'DTK', 'FRF',
                'KTK', 'JOU', 'BNG', 'THS', 'DGM', 'GTC', 'RTR', 'AVR', 'DKA', 'ISD', 'NPH',
                'MBS', 'SOM', 'ROE', 'WWK', 'ZEN', 'ARB', 'CON', 'ALA', 'EVE', 'SHM', 'MOR',
                'LRW', 'FUT', 'PLC', 'TSP', 'CSP', 'DIS', 'GPT', 'RAV', 'SOK', 'BOK', 'CHK',
                '5DN', 'DST', 'MRD', 'SCG', 'LGN', 'ONS', 'JUD', 'TOR', 'ODY', 'APC', 'PLS',
                'INV', 'PCY', 'NEM', 'MMQ', 'UDS', 'ULG', 'USG', 'EXO', 'STH', 'TMP', 'WTH',
                'VIS', 'MIR', 'ALL', 'HML', 'ICE', 'FEM', 'DRK', 'LEG', 'ATQ', 'ARN']

function renderTimeseriesScatterplot(attribute_code, attribute_type='set', max_price=2600) {
  document.getElementById("title").innerHTML = 'Magic the Gathering Rares: Price by Time';
  var attribute = (attribute_type === 'set') ? 'set' : 'color';
  var csvFilePath = "https://raw.githubusercontent.com/bpleines/magic_card_price_visualizer/main/magic_card_csv_files_by_".concat(attribute).concat("/").concat(attribute_code).concat(".csv");
  // Read the data
  d3.csv(csvFilePath, function(d) {
      // Convert all str csv values to ints
      d.release_year = +d.release_year;
      d.price = +d.price;
      return d;
    }).then(function(data) {
      var min_release_year = 1992;
      var max_release_year = 2022;
      // Add X axis
      var x = d3.scaleLinear()
        .domain([min_release_year, max_release_year])
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
           .attr("y", -45)
           .text("Release Year");
      yAxis.append("text")
           .attr("class", "axis-title")
           .attr("transform", "rotate(-90)")
           .attr("y", 24)
           .text("Price (USD)");

      // Add dots
      var markers = svg.append('g')
                       .selectAll("dot")
                       .data(data);

      let img;
      let src;
      markers.enter()
             .append("circle")
	     .attr("cx", function (d) { return x(d.release_year); } )
	     .attr("cy", function (d) { return y(d.price); } )
             .attr("r", 3.0)
             .style("opacity", .75)
             .style("fill", function (d) { return d.color; })
             .style("stroke", "black")
             .on('mouseover', function (event, d) {
                  d3.select(this).transition()
                      .duration('100')
                      .attr("r", 15.0);
                  // Add the image to the page when plot point is hovered over
                  src = d.image;
                  img = document.createElement("img");
                  img.src = src;
                  document.getElementById("card_picture").appendChild(img);
             })
             .on('mouseout', function (event, d) {
                 d3.select(this).transition()
                     .duration('200')
                     .attr("r", 3.0);
                 // remove image from page when hover off
                 document.getElementById("card_picture").removeChild(img);
             });
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
  // plot in reverse order
  let i;
  for (i = mtg_set_codes.length - 1; i >= 0; i--) {
    renderTimeseriesScatterplot(mtg_set_codes[i]);
  }
}
