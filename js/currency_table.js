
										var jqXHR = $.getJSON('data/finalc.json');
											jqXHR.complete(function(response) {
												
											countries = (response.responseJSON);
										
										var data = [];										
										var inc_curr = []
										for (var i = 0, len = countries.length; i < len; i++) {
										
										if ((countries[i].currency != null) && !(inc_curr.indexOf(countries[i].currency) >=0)) {
											var curr_rate =  parseFloat(countries[i].rate_curr);
										
										
											curr={'Currency' : countries[i].currency,  'Current Rate' : curr_rate.toFixed(1)};
											currpred=[parseFloat(countries[i].rate_7),  parseFloat(countries[i].rate_30) ,  parseFloat(countries[i].rate_90)];																	
										
										
							
											//one week pred
											if ( (((curr_rate - currpred[0]) / curr_rate  ) <= 0.025 ) && (((curr_rate - currpred[0]) / curr_rate  ) >= - 0.025 )) {
												curr['One Week Change'] ='Minimal Change'	
											}else if ( (((curr_rate - currpred[0]) / curr_rate  ) < 0.05 ) && (((curr_rate - currpred[0]) / curr_rate  ) > 0.025 )) {
												curr['One Week Change'] ='Decrease'	
											}else if ( (((curr_rate - currpred[0]) / curr_rate  ) < -0.025 ) && (((curr_rate - currpred[0]) / curr_rate  ) > -0.05 )) {
												curr['One Week Change'] ='Increase'	
											}else if ( (((curr_rate - currpred[0]) / curr_rate  ) >= 0.05 )) {
												curr['One Week Change'] ='Large Decrease'
											}else if ( (((curr_rate - currpred[0]) / curr_rate  ) <= -0.05 ) ) {
												curr['One Week Change'] ='Large Increase'	
											}; 
											
											//one month pred
											if ( (((curr_rate - currpred[1]) / curr_rate  ) <= 0.025 ) && (((curr_rate - currpred[1]) / curr_rate  ) >= - 0.025 )) {
												curr['One Month Change'] ='Minimal Change'	
											}else if ( (((curr_rate - currpred[1]) / curr_rate  ) < 0.05 ) && (((curr_rate - currpred[1]) / curr_rate  ) > 0.025 )) {
												curr['One Month Change'] ='Decrease'		
											}else if ( (((curr_rate - currpred[1]) / curr_rate  ) < -0.025 ) && (((curr_rate - currpred[1]) / curr_rate  ) > -0.05 )) {
												curr['One Month Change'] ='Increase'	
											}else if ( (((curr_rate - currpred[1]) / curr_rate  ) >= 0.05 )) {
												curr['One Month Change'] ='Large Decrease'
											}else if ( (((curr_rate - currpred[1]) / curr_rate  ) <= -0.05 ) ) {
												curr['One Month Change'] ='Large Increase'	
											}; 
											
											//three month pred
											if ( (((curr_rate - currpred[2]) / curr_rate  ) <= 0.025 ) && (((curr_rate - currpred[2]) / curr_rate  ) >= - 0.025 )) {
												curr['Three Month Change'] ='Minimal Change'	
											}else if ( (((curr_rate - currpred[2]) / curr_rate  ) < 0.05 ) && (((curr_rate - currpred[2]) / curr_rate  ) > 0.25 )) {
												curr['Three Month Change'] ='Decrease'
											}else if ( (((curr_rate - currpred[2]) / curr_rate  ) < -0.025 ) && (((curr_rate - currpred[2]) / curr_rate  ) > -0.05 )) {
												curr['Three Month Change'] ='Increase'	
											}else if ( (((curr_rate - currpred[2]) / curr_rate  ) >= 0.05 )) {
												curr['Three Month Change'] ='Large Decrease'	
											}else if ( (((curr_rate - currpred[2]) / curr_rate  ) <= -0.05 ) ) {
												curr['Three Month Change'] ='Large Increase'	
											}; 
							
							data.push(curr);
							inc_curr.push(countries[i].currency)
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
											
											var changedict = {'Large Decrease': 2, 'Decrease' : 1, 'Minimal Change' : 0, 'Increase' : -1, 'Large Increase' : -2}
											
											var header = thead.append("tr")
												.selectAll("th")
												.data(columns)
												.enter()
												.append("th")
												.text(function(d){ return d;})
												.on('click', function (d) {								
											
													header.attr('class', 'header');
		                	   
													if (sortAscending && ['One Week Change','One Month Change','Three Month Change'].indexOf(d) >= 0) {
														rows.sort(function(a, b) { 
														return d3.ascending(changedict[a[d]], changedict[b[d]]); });
														sortAscending = false;
														this.className = 'aes';
													} else if (sortAscending) {
														rows.sort(function(a, b) { return d3.ascending(a[d], b[d]); });
														sortAscending = false;
														this.className = 'aes';
													} else if (sortAscending == false && ['One Week Change','One Month Change','Three Month Change'].indexOf(d) >= 0) {
														rows.sort(function(a, b) { return d3.descending(changedict[a[d]], changedict[b[d]]); });
														sortAscending = true;
														this.className = 'des';
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
									