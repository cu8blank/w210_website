function create_bubble_chart() {    
    
    var countries = (function () {
        var json = null;
        $.ajax({
            'async': false,
            'global': false,
            'url': 'data/finaljson.json',
            'dataType': "json",
            'success': function (data) {
                json = data;
            }
        });
        return json;
    })();
    for (var i=0; i < countries.length; i++) {
        if (countries[i].price > 100) {
            console.log(countries[i])
        }
    }
    ////////////////////////////////////////////////////////////
    //////////////////////// Set-up ////////////////////////////
    ////////////////////////////////////////////////////////////
    
    //Quick fix for resizing some things for mobile-ish viewers
    var mobileScreen = ($( window ).innerWidth() < 500 ? true : false);
    
    //Scatterplot
    var margin = {left: 30, top: 20, right: 20, bottom: 20},
        width = Math.min($("#chart").width(), 635) - margin.left - margin.right,
        height = width*2/3;
                
    var svg = d3.select("#chart").append("svg")
                .attr("width", (width + margin.left + margin.right))
                .attr("height", (height + margin.top + margin.bottom));
                
    var wrapper = svg.append("g").attr("class", "chordWrapper")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    // Define the div for the tooltip
    var div = d3.select("body").append("div")	
        .attr("class", "tooltip")				
        .style("opacity", 0); 
    
    //////////////////////////////////////////////////////
    ///////////// Initialize Axes & Scales ///////////////
    //////////////////////////////////////////////////////
    var opacityCircles = 0.7; 
    
    //Set the color for each region
    var cValue = function(d) { return d.cluster_id == null ? 0 : d.cluster_id; },
        color = d3.scale.category20();
    
                                 
    //Set the new x axis range
    var xScale = d3.scale.linear()
        .range([0, width])
        .domain(d3.extent(countries, function(d) {
            
            if (d.curr_week_pct_4 > 150) {  //there was an outlier in the data
                d.curr_week_pct_4 = d.curr_week_pct_4;
            } else if (d.curr_week_pct_4 == null) {
                d.curr_week_pct_4 == 0;
            } else {
                return d.curr_week_pct_4;
            }
        }))

        .nice();
    
    //Set new x-axis	
    var xAxis = d3.svg.axis()
        .orient("bottom")
        .ticks(6)
        .scale(xScale);	
    //Append the x-axis
    wrapper.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(" + 0 + "," + height + ")")
        .call(xAxis);
        
    //Set the new y axis range
    var yScale = d3.scale.linear()
        .range([height,0])
        .domain(d3.extent(countries, function(d) {return d.price == null ? 0 : +d.price;}))
        .nice();	
    var yAxis = d3.svg.axis()
        .orient("left")
        .ticks(6)
        .scale(yScale);	
    //Append the y-axis
    wrapper.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + 0 + "," + 0 + ")")
            .call(yAxis);
            
    //Scale for the bubble size
    var rScale = d3.scale.linear()
                .range([mobileScreen ? 1 : 2, mobileScreen ? 10 : 16])
                .domain(d3.extent(countries, function(d) {return d.attraction_rating == null ? 1 : Math.sqrt(d.attraction_rating * 100);}));
            
    ////////////////////////////////////////////////////////////	
    /////////////////// Scatterplot Circles ////////////////////
    ////////////////////////////////////////////////////////////	
    
    //Initiate the voronoi group element	
    var circleGroup = wrapper.append("g")
        .attr("class", "circleWrapper"); 
        
    //Place the country circles	
    wrapper.selectAll("countries")
        .data(countries.sort(function(a,b) { return Math.sqrt(b.attraction_rating * 100) > Math.sqrt(a.attraction_rating * 100); })) //Sort so the biggest circles are below
        .enter().append("circle")
            .attr("class", "countries")
            .style("opacity", opacityCircles)
            .style("fill", function(d) {return color(cValue(d));})
            .attr("cx", function(d) {return xScale(d.curr_week_pct_4);})
            .attr("cy", function(d) {return yScale(d.price);})
            .attr("r", function(d) {return rScale(Math.sqrt(d.attraction_rating * 100));})
            .on("mouseover", showTooltip)
            .on("mouseout", removeTooltip);
    
    //////////////////////////////////////////////////////
    ///////////////// Initialize Labels //////////////////
    //////////////////////////////////////////////////////
    
    //Set up X axis label
    wrapper.append("g")
        .append("text")
        .attr("class", "x title")
        .attr("text-anchor", "end")
        .style("font-size", (mobileScreen ? 8 : 12) + "px")
        .attr("transform", "translate(" + width + "," + (height - 10) + ")")
        .text("Safety Score");
    
    //Set up y axis label
    wrapper.append("g")
        .append("text")
        .attr("class", "y title")
        .attr("text-anchor", "end")
        .style("font-size", (mobileScreen ? 8 : 12) + "px")
        .attr("transform", "translate(18, 0) rotate(-90)")
        .text("Cost Score");

        
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////// Create the Legend////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    
    if (!mobileScreen) {
        //Legend			
        var	legendMargin = {left: 5, top: 10, right: 5, bottom: 10},
            legendWidth = 180,
            legendHeight = 380;
            
        var svgLegend = d3.select("#legend").append("svg")
                    .attr("width", (legendWidth + legendMargin.left + legendMargin.right))
                    .attr("height", (legendHeight + legendMargin.top + legendMargin.bottom));			
    
        var legendWrapper = svgLegend.append("g").attr("class", "legendWrapper")
                        .attr("transform", "translate(" + legendMargin.left + "," + legendMargin.top +")");
            
        var rectSize = 16, //dimensions of the colored square
            rowHeight = 22, //height of a row in the legend
            maxWidth = 125; //widht of each row
              
        //Create container per rect/text pair  
        var legend = legendWrapper.selectAll('.legendSquare')  	
                  .data(color.range())                              
                  .enter().append('g')   
                  .attr('class', 'legendSquare') 
                  .attr("transform", function(d,i) { return "translate(" + 0 + "," + (i * rowHeight) + ")"; });
         
        //Append small squares to Legend
        legend.append('rect')                                     
              .attr('width', rectSize) 
              .attr('height', rectSize) 			  		  
              .style('fill', function(d) {return d;});                                 
        //Append text to Legend
        legend.append('text')                                     
              .attr('transform', 'translate(' + 25 + ',' + (rectSize/2) + ')')
              .attr("class", "legendText")
              .style("font-size", "11px")
              .attr("dy", ".35em")		  
              .text(function(d,i) { return color.domain()[i]; });
    
    }//if !mobileScreen
    else {
        d3.select("#legend").style("display","none");
    }
          
    ///////////////////////////////////////////////////////////////////////////
    /////////////////// Hover functions of the circles ////////////////////////
    ///////////////////////////////////////////////////////////////////////////
 
    function removeTooltip() {		
            div.transition()		
                .duration(500)		
                .style("opacity", 0);
    };
    
    //Show the tooltip on the hovered over slice
    function showTooltip(d) {		
            div.transition()		
                .duration(200)		
                .style("opacity", .9);		
            div	.html("<strong> Country: </strong>" + d.Name + "<br/>" + "<strong> Safety Score: </strong>" + parseFloat(d.curr_week_pct_4).toFixed(2) + "<br/>" + "<strong> Cost Score: </strong>" + parseFloat(d.price).toFixed(2) + "<br/>"
                      + "<strong> Attraction Rating: </strong>" + parseFloat(d.attraction_rating).toFixed(2) + "<br/>" + "<strong> Cluster ID: </strong>" + d.cluster_id + "<br/>")	
                .style("left", (d3.event.pageX) + "px")		
                .style("top", (d3.event.pageY - 130) + "px");
 
    };
    
    //iFrame handler
    var pymChild = new pym.Child();
    pymChild.sendHeight()
    setTimeout(function() { pymChild.sendHeight(); },5000);
    
};

create_bubble_chart();