function plotbar(from_year,to_year,choice) {
    
  d3.json("/data",function(response) {
    
    console.log(choice.length);
    console.log(response);
    var year = parseInt(from_year);
    console.log(year);
    
    
   
    if (choice.length === 1){

      var yearX = [];
      var bothsexes = [];
      var male = [];
      var female = [];
     
      var hovertext1 = [];
      var hovertext2 =[];
      var hovertext3 = [];

      if (parseInt(from_year) >= parseInt(to_year)) {
      var year_length = 1;
      } 
      else {
      var year_length = parseInt(to_year) - parseInt(from_year) + 1;
      }
      console.log(year_length);
        for (i=0; i<year_length; i++){
        yearX.push(parseInt(year)+i);
        let yearslice = ((parseInt(year)+i).toString()).slice(2,4);
        console.log(yearslice);
        let Bothsexes_year = "Bothsexes".concat(yearslice);
        console.log(Bothsexes_year);
        let Male_year = "Male".concat(yearslice);
        let Female_year = "Female".concat(yearslice);
        let countrydata=[];
        let bothsexesdata=[];
        let maledata=[];
        let femaledata=[];
        
        response.forEach(data=>{
        let countrydata_ = data.Country;//arrayColumn(data,"Country");
        let bothsexesdata_ = data[Bothsexes_year];//arrayColumn(data,Bothsexes_year);
        let maledata_ = data[Male_year];
        let femaledata_ = data[Female_year];
        
        countrydata.push(countrydata_);
        bothsexesdata.push(bothsexesdata_);
        maledata.push(maledata_);
        femaledata.push(femaledata_);
        });
        console.log(countrydata);
        console.log(bothsexesdata);
        console.log(maledata);
        console.log(femaledata);

        

        for (j in countrydata){
           if (choice[0] === countrydata[j]){
            bothsexes.push(bothsexesdata[j]);
            male.push(maledata[j]);
            female.push(femaledata[j]);
            hovertext1.push(`${choice}<br>Bothsexes: ${bothsexesdata[j]}(years)`);
            hovertext2.push(`${choice}<br>Male: ${maledata[j]}(years)`);
            hovertext3.push(`${choice}<br>Female: ${femaledata[j]}(years)`)
            }
        }
        console.log(bothsexes);
        console.log(choice);
      }
      var trace1 = {
        x: yearX,
        y: bothsexes,
        name: 'Bothsexes',
        type: 'bar',
        marker: {
          color: '#00bfd8'},
        text: hovertext1
      };
      var trace2 = {
        x: yearX,
        y: male,
        name: 'Male',
        type: 'bar',
        marker: {
          color: 'rgb(204,204,204)'},
        text: hovertext2
      };
      var trace3 = {
        x: yearX,
        y: female,
        name: 'Female',
        type: 'bar',
        marker: {
          color: 'black'},
        text: hovertext3
       };
       databar = [trace1,trace2,trace3];
       console.log(databar)
       var layout = {
        xaxis: {title: 'Time'},
        yaxis: {title: `Life Expectancy(years)`},
        barmode: 'group',
        bargap: 0.15,
        bargroupgap: 0.1,
       // barmode: 'relative',
        title: `<b>Life Expectancy at Birth (years)</b>`

      };

    }
    else {
      var yearX = [];
      var nation1 = [];
      var nation2 = [];
           
     
      var hovertext1 = [];
      var hovertext2 = [];
      

      if (parseInt(from_year) >= parseInt(to_year)) {
      var year_length = 1;
      } 
      else {
      var year_length = parseInt(to_year) - parseInt(from_year) + 1;
      }

        for (i=0; i<year_length; i++){
        yearX.push(parseInt(year)+i);
        console.log(yearX);
        let yearslice = ((parseInt(year)+i).toString()).slice(2,4);
        let Bothsexes_year = "Bothsexes".concat(yearslice);
    
        let countrydata=[];
        let bothsexesdata=[];
                
        response.forEach(data=>{
        let countrydata_ = data.Country;//arrayColumn(data,"Country");
        let bothsexesdata_ = data[Bothsexes_year];//arrayColumn(data,Bothsexes_year);
               
        countrydata.push(countrydata_);
        bothsexesdata.push(bothsexesdata_);
        });
        for (j in countrydata){
           if (countrydata[j] === choice[0]){
            nation1.push(bothsexesdata[j]);
            hovertext1.push(`${choice[0]}<br>Bothsexes: ${bothsexesdata[j]}(years)`);
           }
           else if (countrydata[j] === choice[1]) {
             nation2.push(bothsexesdata[j]);
             hovertext2.push(`${choice[1]}<br>Bothsexes: ${bothsexesdata[j]}(years)`);
           }
          }
          console.log(hovertext1);
          console.log(hovertext2);
           
        }
        var trace1 = {
          x: yearX,
          y: nation1,
          name: `${choice[0]}`,
          type: 'bar',
          marker: {
            color: '#00bfd8'},
          text: hovertext1
          };
        var trace2 = {
          x: yearX,
          y: nation2,
          name: `${choice[1]}`,
          type: 'bar',
          marker: {
            color: 'rgb(204,204,204)'},
          text: hovertext2
        };
       
         databar = [trace1,trace2];
         console.log(databar);
         var layout = {
          xaxis: {title: 'Time'},
          yaxis: {title: 'Life Expectancy(years)'},
          barmode: 'group',
          bargap: 0.15,
          bargroupgap: 0.1,
          //barmode: 'relative',
          title: 'Life Expectancy at Birth (years)'
        };
      }
      Plotly.newPlot("chart1", databar, layout); 

      });
}


function plotscatter(year,choice) {
    
    d3.json("/data",function(response) {
      
        let data = response;
        //const arrayColumn = (arr, n) => arr.map(x => x[n]);
        let year_capita = year.concat("capita");

        let yearslice = year.slice(2,4);
        let Bothsexes_year = "Bothsexes".concat(yearslice);
        let Male_year = "Male".concat(yearslice);
        let Female_year = "Female".concat(yearslice);

        let continent =[];
        let countrydata=[];
        let bothsexesdata=[];
        let maledata=[];
        let femaledata=[];
        let percentdata=[];
        let capitadata=[];

        data.forEach(data=>{
          let continent_ = data.Continent;//arrayColumn(data,"Continent");
          let countrydata_ = data.Country;//arrayColumn(data,"Country");
          let bothsexesdata_ = data[Bothsexes_year];//arrayColumn(data,Bothsexes_year);
          let maledata_ = data[Male_year];
          let femaledata_ = data[Female_year];
          let percentdata_ = data[year];//arrayColumn(data,year);
          let capitadata_ = data[year_capita];//arrayColumn(data,year_capita)

          continent.push(continent_);
          countrydata.push(countrydata_);
          bothsexesdata.push(bothsexesdata_);
          maledata.push(maledata_);
          femaledata.push(femaledata_);
          percentdata.push(percentdata_);
          capitadata.push(capitadata_);
        });

        let country =[];
        let bothsexes = [];
        let male = [];
        let female = [];
        let percent = [];
        let capita = [];
        
        for(i in continent) {
          if (choice === "all") {
              country = countrydata;
              bothsexes = bothsexesdata;
              male = maledata;
              female = femaledata;
              percent = percentdata;
              capita = capitadata;
              }
          else if (choice === continent[i]) {
              country.push(countrydata[i]);
              bothsexes.push(bothsexesdata[i]);
              male.push(maledata[i]);
              female.push(femaledata[i]);
              capita.push(capitadata[i]);
              percent.push(percentdata[i]);
              }
            var hovertext1 = [];
            var hovertext2 =[];
            for (var i in country) {
            hovertext1.push(`${country[i]}<br>${year}: ${percent[i]}%`);
            hovertext2.push(`${country[i]}<br>${year}: ${capita[i]}$`);
            };
          };
          
          
        var trace1 = {
          x: bothsexes,
          y: percent,
          hovertext: hovertext1,
          mode: "markers",
          type: "scatter",
          name: "%(GDP)",
          marker: {
            color: "#00bfd8",
            symbol: "hexagram"
          }
        };
        var trace2 = {
          x: bothsexes,
          y: capita,
          hovertext:hovertext2,
          yaxis: 'y2',
          mode: "markers",
          type: "scatter",
          name: "perCapita (Int$)",
          marker: {
            color: "black",
            symbol: "circle"
          }
        };

        var dataplot = [trace1,trace2];

        var layout = {
          title: `<b>Relationship of Life Expectancy and Healthcare Expenditure</b><br>Region: ${choice==="all"?"Worldwide":choice} in ${year}`,
          xaxis: { title: "Life Expectation (Years) ", titlefont: {colorwidth: 2, color: "black"}
                },
          yaxis: { 
            title: "Healthcare Expenditure (HE) %(GDP)",
            titlefont: {color: '#00bfd8'},
            tickfont: {color: '#00bfd8'},
          },
          yaxis2: {
            title: "HE perCapita (int$))",
            titlefont: {color: 'black'},
            tickfont: {color: 'black'},
            //anchor: 'free',
            anchor: 'x',
            overlaying: 'y',
            side: 'right'
          }
          };
        Plotly.newPlot("chart2", dataplot, layout);    
        
             
      });
    }


    function init() {
      // Grab a reference to the dropdown select element
              // Use the first sample from the list to build the initial plots
        var selector = d3.select("#selData");

        // Use the list of sample names to populate the select options
        d3.json("/country", function(sampleNames) {
          console.log(sampleNames);
          sampleNames.forEach((sample) => {
            selector
              .append("option")
              .text(sample)
              .property("value", sample);
          });
        });


        year ="2015";
        choice ="all";
        plotscatter(year,choice);

        year_from = "2000";
        year_to = "2016";
        country = ["United States of America"];
        plotbar(year_from,year_to,country)

      };
    
    function update_continent(continent){
      console.log(continent);
      var sect = document.getElementById("year");
      var year = sect.options[sect.selectedIndex].value;
      plotscatter(year,continent);
    }

    function update_year(year) {
      console.log(year);
      var sect = document.getElementById("continent");
      var continent = sect.options[sect.selectedIndex].value;
      plotscatter(year,continent);
    }

    function from_year(year_from){
      var sect = document.getElementById("year_to");
      var year_to = sect.options[sect.selectedIndex].value;
      var country = getChoices();
      plotbar(year_from,year_to,country);
    }

    function to_year(year_to){
      var sect = document.getElementById("year_from");
      var year_from = sect.options[sect.selectedIndex].value;
      var country = getChoices();
      plotbar(year_from,year_to,country);

    }

    function getChoices(){
      //retrieve data
      var selLanguage = document.getElementById("selData");
      //set up output string
      var country = [];
      //step through options
      for (i = 0; i < selLanguage.length; i++){
       //examine current option
       currentOption = selLanguage[i];
       //print it if it has been selected
       if (currentOption.selected == true){
       country.push(currentOption.value)
       } // end if
      } // end for loop
      var sect1 = document.getElementById("year_from");
      var year_from = sect1.options[sect1.selectedIndex].value;
      var sect2 = document.getElementById("year_to");
      var year_to = sect2.options[sect2.selectedIndex].value;
      plotbar(year_from,year_to,country);
      console.log(country);
      return country;
      }
    // Initialize the plot
    init();
   



