			var map = AmCharts.makeChart("mapdiv", {
				type: "map",
				theme: "light",
				projection: "Eckert5",
				
				dataProvider: {
					map: "worldLow",						
					getAreasFromMap: true,
					
					//***** Modify this section to change the hover over pop up boxes *****//
					//***** Or you can also modify each country in the worldLow.js file *****//
					areas: 					[				  

					  {
						id: "AX",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "AI",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "AQ",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "BA",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "BV",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "IO",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "VG",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "CV",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "KY",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "CX",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "CC",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "CK",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "DM",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "FK",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "FO",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "GF",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "PF",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "TF",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "GI",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "GL",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "GP",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "GU",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "GG",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "HM",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "HK",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "IM",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "JE",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "KI",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "MO",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "MH",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "MQ",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "MU",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "YT",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "ME",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "MS",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "NR",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "AN",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "NC",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "NU",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "NF",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "MP",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "PW",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "PS",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "PN",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "PR",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "RE",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "SH",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "PM",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "VC",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "BL",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "MF",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "WS",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "SM",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "ST",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "SC",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "SI",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "SB",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "GS",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "SS",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "SJ",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "TK",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "TO",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "TC",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "TV",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "UM",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "VU",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "VI",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "WF",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "EH",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  {
						id: "US",
						selectable: false,
						title: "Not Available",
						color: "#c2c2a3",
					  },
					  

					  ],

					//***** Modify the above code to edit the pop up boxes *****//					
				},

				areasSettings: {
					autoZoom: true,
					selectedColor: "#CC0000"  //******* change this color for the zoomed in country *******//
				},

				smallMap: {}
			});