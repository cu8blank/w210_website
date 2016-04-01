
										
									
								var jqXHR = $.getJSON('data/finalc.json');
									jqXHR.complete(function(response) {
												
								countries = (response.responseJSON);
									
								var safe_list = [];
								
								
								
								
								
								for (var i = 0, len = countries.length; i < len; i++) {
																				
										safety={'Country' : countries[i].Name, 'Current Value' : parseFloat(countries[i].curr_week_pct_4.toFixed(1))};
										safetypred=[countries[i].pred_1_week,  countries[i].pred_1_month ,  countries[i].pred_3_months];
										
										
										
										//one week pred		
										if ((countries[i].curr_week_pct_4/10).toFixed(0)-safetypred[0] == 0){
													safety['One Week Change']='Minimal Change'
										}else if ((countries[i].curr_week_pct_4/10).toFixed(0)-safetypred[0] == 1){
													safety['One Week Change']='Decrease'
										}else if ((countries[i].curr_week_pct_4/10).toFixed(0)-safetypred[0] == -1){
													safety['One Week Change']='Increase'
										}else if ((countries[i].curr_week_pct_4/10).toFixed(0)-safetypred[0] > 1){
													safety['One Week Change']='Large Decrease'	
										}else {
													safety['One Week Change']='Large Increase';		
										};
										
										//one month pred 
										if ((countries[i].curr_week_pct_4/10).toFixed(0)-safetypred[1] == 0){
													safety['One Month Change']='Minimal Change'	
										}else if ((countries[i].curr_week_pct_4/10).toFixed(0)-safetypred[1] == 1){
													safety['One Month Change']='Decrease'	
										}else if ((countries[i].curr_week_pct_4/10).toFixed(0)-safetypred[1] == -1){
													safety['One Month Change']='Increase'
										}else if ((countries[i].curr_week_pct_4/10).toFixed(0)-safetypred[1] > 1){
													safety['One Month Change']='Large Decrease'	
										}else {
													safety['One Month Change']='Large Increase';		
										};
										
										//three month pred 
										if ((countries[i].curr_week_pct_4/10).toFixed(0)-safetypred[2] == 0){
													safety['Three Month Change']='Minimal Change'			
										}else if ((countries[i].curr_week_pct_4/10).toFixed(0)-safetypred[2] == 1){
													safety['Three Month Change']='Decrease'	
										}else if ((countries[i].curr_week_pct_4/10).toFixed(0)-safetypred[2] == -1){
													safety['Three Month Change']='Increase'	
										}else if ((countries[i].curr_week_pct_4/10).toFixed(0)-safetypred[2] > 1){
													safety['Three Month Change']='Large Decrease'		
										}else {
													safety['Three Month Change']='Large Increase';		
										};

									
									
									safe_list.push(safety);
									
									
									
									};		
												
							
													
											
							var svg = d3.select("body").append("svg")
											.attr("height", 1)
											.attr("width", 1);
										
							var table = d3.select("#safety-table")
											.append("table")
											.attr("class", "table table-hover table-condensed"),
											thead = table.append("thead"),
											tbody = table.append("tbody");
											
							var columns = ['Country','Current Value','One Week Change','One Month Change','Three Month Change'];
								
							var sortAscending = true;
							
							
							var changedict = {'Large Decrease': 2, 'Decrease' : 1, 'Minimal Change' : 0, 'Increase' : -1, 'Large Increase' : -2}
								
							var header = thead.append("tr")
											.selectAll("th")
											.data(columns)
											.enter()
											.append("th")
											.text(function(d){ return d;})
											.style("text-align", "center")
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
		                   });
							
							
												
						
							var rows = tbody.selectAll("tr")
								.data(safe_list)
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
												
												
							