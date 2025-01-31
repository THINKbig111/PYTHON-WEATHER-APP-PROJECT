document.addEventListener('DOMContentLoaded', () => {
    let daytimediv = document.getElementById('daytimeDiv');
    let btn = document.getElementById('btn');
    let days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    let months = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"];

    setInterval(() => {
        let newDate = new Date();
        let mins = newDate.getMinutes();
        let hours = newDate.getHours();
        let ampm = hours >= 12 ? 'PM' : 'AM';
        let hour12 = hours > 12 ? hours % 12 : hours;
        hour12 = hour12 === 0 ? 12 : hour12;
        let day = newDate.getDay();
        let date = newDate.getDate();
        let month = newDate.getMonth();

        daytimediv.innerHTML = mins < 10
            ? `<p>${hour12}:0${mins} ${ampm} </p><p>${days[day]}, ${date} ${months[month]} </p>`
            : `<p>${hour12}:${mins} ${ampm}</p><p>${days[day]}, ${date} ${months[month]} </p>`;
    }, 1000);

    btn.addEventListener('click', async () => {
        let cityNameVal = document.getElementById('city').value;
        document.querySelector('.container').textContent = '';
        document.querySelector(".weatherBottom").innerHTML = "";

        try {
            let response = await fetch(`/get_weather/?city=${cityNameVal}`);
            let data = await response.json();
            if (response.ok) {
                displayWeather(data.weather);
                forecast(data.forecast);
            } else {
                console.error('Error fetching weather data', data);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    function displayWeather(data) {
        let weatherDetail = document.createElement('div');
        weatherDetail.id = 'weatherDetail';

        let upper = document.createElement('div');
        upper.classList.add('upper');

        let timeZone = document.createElement('div');
        timeZone.classList.add('timeZone');
        setInterval(() => {
            let newDate = new Date();
            let mins = newDate.getMinutes();
            let hours = newDate.getHours();
            let ampm = hours >= 12 ? 'PM' : 'AM';
            let hour12 = hours > 12 ? hours % 12 : hours;
            hour12 = hour12 === 0 ? 12 : hour12;
            let day = newDate.getDay();
            let date = newDate.getDate();
            let month = newDate.getMonth();

            timeZone.innerHTML = mins < 10
                ? `<p>${hour12}:0${mins} ${ampm} </p><p>${days[day]}, ${date} ${months[month]} </p>`
                : `<p>${hour12}:${mins} ${ampm}</p><p>${days[day]}, ${date} ${months[month]} </p>`;
        }, 1000);

        let weatherIcon = document.createElement('div');
        weatherIcon.classList.add('weatherIcon');

        let info = document.createElement('div');
        info.id = 'info';

        let icon = document.createElement('img');
        icon.classList.add('iconimg');
        icon.src = ` https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png`;

        let iconDes = document.createElement('p');
        iconDes.textContent = data.weather[0].main;
        iconDes.id = 'description';

        let cityName = document.createElement('h1');
        cityName.textContent = data.name;

        let temp = document.createElement('p');
        let temper = (data.main.temp - 273.15).toFixed(2);
        temp.textContent = `Temperature ${temper} °C`;

        let wind = document.createElement('p');
        wind.textContent = `Wind ${data.wind.speed} m/sec;`;

        let pressure = document.createElement('p');
        pressure.textContent = `Pressure ${data.main.pressure} hpa`;

        let humidity = document.createElement('p');
        humidity.textContent = `Humidity ${data.main.humidity}%`;

        let sunrise = document.createElement('p');
        let rise = data.sys.sunrise;
        let date = new Date(rise * 1000);
        let hr = date.getHours();
        let hr12 = hr > 12 ? hr % 12 : hr;
        let AmPm = hr >= 12 ? 'PM' : 'AM';
        let min = date.getMinutes();
        sunrise.textContent = min < 10
            ? `Sunrise ${hr12}:0${min} ${AmPm}`
            : `Sunrise ${hr12}:${min} ${AmPm}`;

        let sunset = document.createElement('p');
        let set = data.sys.sunset;
        let date1 = new Date(set * 1000);
        let hr1 = date1.getHours();
        let hr112 = hr1 > 12 ? hr1 % 12 : hr1;
        let AmPm1 = hr1 >= 12 ? 'PM' : 'AM';
        let min1 = date1.getMinutes();
        sunset.textContent = min1 < 10
            ? `Sunset ${hr112}:0${min1} ${AmPm1}`
            : `Sunset ${hr112}:${min1} ${AmPm1}`;

        let weatherMap = document.createElement('div');
        weatherMap.id = 'weatherMap';

        let lat = data.coord.lat;
        let lon = data.coord.lon;
        let frame = document.createElement("iframe");
        frame.src = `https://maps.google.com/maps?q=${lat},${lon}&t=&z=13&ie=UTF8&iwloc=&output=embed`;
        frame.width = '620px';
        frame.height = '325px';

        weatherIcon.append(icon, iconDes);
        info.append(cityName, temp, pressure, humidity, wind, sunrise, sunset);
        upper.append(timeZone, weatherIcon);
        weatherDetail.append(upper, info);
        weatherMap.append(frame);
        document.querySelector('.container').append(weatherDetail, weatherMap);
    }

    function forecast(data) {
        document.querySelector(".weatherBottom").style.display = 'flex';
        for (let i = 5; i < 40; i += 8) {
            let card = document.createElement("div");
            card.setAttribute("class", "forecastCards");

            let icon = document.createElement("img");
            icon.src = `http://openweathermap.org/img/wn/${data.list[i].weather[0].icon}@2x.png`;

            let desc = document.createElement("p");
            desc.textContent = data.list[i].weather[0].description;

            let date = document.createElement("h2");
            date.textContent = data.list[i].dt_txt.split(" ")[0];

            let minMax = document.createElement("div");
            minMax.setAttribute("id", "minMaxTemp");

            let minTemp = document.createElement("p");
            minTemp.textContent = "Min Temp " + data.list[i].main.temp_min + " °C";

            let maxTemp = document.createElement("p");
            maxTemp.textContent = "Max Temp " + data.list[i].main.temp_max + " °C";

            minMax.append(minTemp, maxTemp);
            card.append(date, icon, desc, minMax);
            document.querySelector(".weatherBottom").append(card);
        }
    }
});