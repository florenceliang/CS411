
        function get_weather_by_city() {
            const city = document.getElementById('search_bar').value
            get_weather('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=46298d85e7d4b0e1deefe4d6fcb4f839')
        }

        // function to get weather by using current location
        function get_weather_by_coordinates(){
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;
                        const endpoint = "https://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + lon + "&appid=46298d85e7d4b0e1deefe4d6fcb4f839";
                        get_weather(endpoint);
                    }
                );
            } else {
                console.log("Geolocation is not supported by this browser.");
            }
        }

        // display weather of determined location
        function get_weather(endpoint) {
            console.log("endpoint " + endpoint)
            const request = new XMLHttpRequest();
            request.open("GET", endpoint, true);
            request.onload = function () {
                if (request.status == 404) {
                    alert("An unknown error has occured. Please make sure the city is spelled correctly. ex: newyork -> new york");
                } else {
                    const weather = JSON.parse(this.response);
                    //var condition = (parseFloat(weather['weather'][0]['main']))
                    var temp = (parseFloat(weather['main']['temp']) - 273.15) * 9/5 + 32
                    var feels_like = (parseFloat(weather['main']['feels_like']) - 273.15) * 9/5 + 32
                    document.getElementById('city_temp').innerHTML = 'The temperature for your city is ' + temp.toFixed(2).toString() + ' degrees Fahrenheit'
                    document.getElementById('feels_like').innerHTML = 'Feels like: ' + feels_like.toFixed(2).toString() + ' degrees Farenheit'
                    document.getElementById('wind_speed').innerHTML = 'Winds of ' + weather['wind']['speed'] + 'MPH'

                    var outcome = "unknown"
                    if (weather['weather'][0]['main'] === "Clouds") {
                        var outcome = "cloudy"
                    }
                    else if (weather['weather'][0]['main'] === "Clear"){
                        var outcome = "sunny"
                    }
                    else if (weather['weather'][0]['main'] === "Tornado"){
                        var outcome = "foggy"
                    }
                    else if (weather['weather'][0]['main'] === "Squall"){
                        var outcome = "foggy"
                    }
                    else if (weather['weather'][0]['main'] === "Ash"){
                        var outcome = "foggy"
                    }
                    else if (weather['weather'][0]['main'] === "Dust"){
                        var outcome = "foggy"
                    }
                    else if (weather['weather'][0]['main'] === "Sand"){
                        var outcome = "foggy"
                    }
                    else if (weather['weather'][0]['main'] === "Fog"){
                        var outcome = "foggy"
                    }
                    else if (weather['weather'][0]['main'] === "Dust"){
                        var outcome = "foggy"
                    }
                    else if (weather['weather'][0]['main'] === "Haze"){
                        var outcome = "foggy"
                    }
                    else if (weather['weather'][0]['main'] === "Smoke"){
                        var outcome = "foggy"
                    }
                    else if (weather['weather'][0]['main'] === "Mist"){
                        var outcome = "foggy"
                    }
                    else if (weather['weather'][0]['main'] === "Snow"){
                        var outcome = "snowing"
                    }
                    else if (weather['weather'][0]['main'] === "Rain"){
                        var outcome = "raining"
                    }
                    else if (weather['weather'][0]['main'] === "Drizzle"){
                        var outcome = "raining"
                    }
                    else if (weather['weather'][0]['main'] === "Thunderstorm"){
                        var outcome = "raining"
                    }
                    document.getElementById('condition').innerHTML = "Condition is " + outcome

                    var data = {
                       outcome
                    }
                    $.post( "/postmethod", {
                    canvas_data: JSON.stringify(data)
                    },
                    }
            };
            request.send();
        }