
										var jqXHR = $.getJSON('data/finalc.json');
											jqXHR.complete(function(response) {
												
											countries = (response.responseJSON);
										
										var data = [];										
										
										for (var i = 0, len = countries.length; i < len; i++) {
											
											
											if (countries[i].currency != null) {											
												curr={'Currency' : countries[i].currency, 
													'Current Rate' : parseFloat(countries[i].rate_curr.toFixed(1)),
													'One Week' : parseFloat(countries[i].rate_7.toFixed(1)),
													'One Month Prediction' : parseFloat(countries[i].rate_30.toFixed(1)),
													'Three Month Prediction' : parseFloat(countries[i].rate_90.toFixed(1))};
													
											data.push(curr);
													
										};
										};
										
										
																					
										var svg = d3.select("body").append("svg")
											.attr("height", 1)
											.attr("width", 1);
										
										var table = d3.select("#currency-table")
											.append("table")
											.attr("class", "table table-hover table-condensed"),
											thead = table.append("thead"),
											tbody = table.append("tbody");
							
										
											
											// Get every column value	
							
											var columns = Object.keys(data[0]);											
											
											
											var sortAscending = true;											
											
											
											var header = thead.append("tr")
												.selectAll("th")
												.data(columns)
												.enter()
												.append("th")
													.text(function(d){ return d;})
													.on('click', function (d) {									
											
													header.attr('class', 'header');
		                	   
													if (sortAscending) {
														rows.sort(function(a, b) { 
														return d3.ascending(a[d], b[d]); });
														sortAscending = false;
														this.className = 'aes';
		                	 
													} else {
														rows.sort(function(a, b) { return d3.descending(a[d], b[d]); });
														sortAscending = true;
														this.className = 'des';
													}
													})
													.style("text-align", "center")
													.style("font-weight", "bold");
										
											var rows = tbody.selectAll("tr")
												.data(data)
												.enter()
												.append("tr");
												
												
										
											var cells = rows.selectAll("td")
												.data(function(row){
													return columns.map(function(d, i){
														return {i: d, value: row[d]};
													});
												})
												.enter()
												.append("td")
												.html(function(d){ return d.value;});
												
												
							
		});								
									