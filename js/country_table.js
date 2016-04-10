	
								var jqXHR = $.getJSON('data/finaljson.json');
									jqXHR.complete(function(response) {
												
								countries = (response.responseJSON);								
								
									
								var country_list = [];
								
								for (var i = 0, len = countries.length; i < len; i++) {
								
								
									
											
									cty = {"Country" : countries[i].Name,
											"Attraction Rating" : countries[i].average,
											"Attractions" : countries[i].att_str,
											"Cluster ID" : countries[i].cluster_id										
										
										}
										
									
									country_list.push(cty);
									
									
									
									};		
												
								
									
									
											
							var svg = d3.select("body").append("svg")
											.attr("height", 1)
											.attr("width", 1);
										
							var table = d3.select("#country-table")
											.append("table")
											.attr("class", "table table-hover table-condensed"),
											thead = table.append("thead"),
											tbody = table.append("tbody");
											
							var columns = Object.keys(country_list[0]);	
								
							var sortAscending = true;
							
							
								
							var header = thead.append("tr")
											.selectAll("th")
											.data(columns)
											.enter()
											.append("th")
											.text(function(d){ return d;})
											.style("text-align", "center")
											.on('click', function (d) {									
											
		                	   header.attr('class', 'header');
		                	   
		                	   if (sortAscending) {
		                		 rows.sort(function(a, b) { return d3.ascending(a[d], b[d]); });
		                		 sortAscending = false;
		                		 this.className = 'aes';
		                	   }else {
		                		 rows.sort(function(a, b) { return d3.descending(a[d], b[d]); });
		                		 sortAscending = true;
		                		 this.className = 'des';
		                	   }
		                   });
							
							
												
						
							var rows = tbody.selectAll("tr")
								.data(country_list)
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
												
												
							