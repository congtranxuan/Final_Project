function perc2color(perc,max,min) {
    var base = (max - min);

    if (base == 0) { perc = 100; }
    else {
        perc = (perc - min) / base * 100; 
    }
    var r, g, b = 0;
    if (perc < 50) {
        r = 255;
        g = Math.round(5.1 * perc);
    }
    else {
        g = 255;
        r = Math.round(510 - 5.10 * perc);
    }
    var h = r * 0x10000 + g * 0x100 + b * 0x1;
    return '#' + ('000000' + h.toString(16)).slice(-6);
}

function legend() {
    var legends = L.control({
      //The location of legend is set at bottom right.
      position: "bottomright"
    });
    
      // Define the properties of legend
        legends.onAdd = function () {
        var labels = ["Life Expectancy Legend"]; 
        var div = L.DomUtil.create('div', 'legend');
        cat = ["No Data",'>50','>55','>60','>65','>70',">75",">80"];
        color = ["#10ff00", "#60ff00", "#afff00", "#ffff00","#ffaf00" ,"#ff6000", "#ff1000","#000000"];
    
        for (var i = 0; i < cat.length; i++) {
    
                div.innerHTML = 
                labels.push('<div class="square" style="background:' + color[i] + '"></div><span class="explanation">' + cat[color.length-i-1] +'</span>' );
            }
            div.innerHTML = labels.join('<br>');
            return div;
        };
    
        legends.addTo(myMap);
      }

// // Create a map object
// var myMap = L.map("leafletmap", { center: [42.258044, 22.709860],
//     minZoom: 1,
// 	maxZoom: 3
// });
var myMap = L.map("leafletmap", {
    center: [42.258044, 22.709860],
    zoom: 2
});



var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
    maxZoom: 13,
    id: "mapbox.light",
    accessToken: API_KEY
}).addTo(myMap);


d3.json("/map", function(responseLife) {
    //var responsegeo = data();
    console.log(responseLife);
            
    d3.json("static/db/countriesgeojson.json", function(responsegeo) {
         //var responsegeo = datajson();
         console.log(responsegeo);
         console.log(responseLife);
         var country = [];
         var bothsexes16 = [];
         var minAge = 100;
         var maxAge = 0;
         

         for (i=0;i< responseLife.length;i++) {
             country.push(responseLife[i].Country);
             bothsexes = parseInt(responseLife[i].Bothsexes16);
             if (bothsexes>maxAge){
                 maxAge = bothsexes;
             }
             if(bothsexes < minAge){
                 minAge = bothsexes;
             }
             bothsexes16.push(bothsexes);
            }
             console.log(bothsexes16);
             console.log(country);
            
            var colorcountry = {};
            var codecountry = {};
            for (i=0;i<country.length;i++){
                colorcountry[i] = bothsexes16[i];
                codecountry[country[i]] = i;
            }
            
            var countryname = [];
            responsegeo.features.forEach(d=>{
                countryname.push(d.properties.ADMIN);
            })
                     
             
                    
        L.geoJSON(responsegeo, { style: function(feature) {
                    return {
                     fillColor: perc2color(colorcountry[codecountry[feature.properties.ADMIN]],maxAge,minAge) || "#de1fb5",
                     fillOpacity: 1,
                     stroke: true,
                     color: "grey", // Lines in between countries.
                    weight: 2
                    };
                }
                }).bindPopup(function(layer) {
                return layer.feature.properties.ADMIN;
                }).addTo(myMap);
                        
       
        legend();   
           
});
});


