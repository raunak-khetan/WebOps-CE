document.addEventListener('DOMContentLoaded', () => {
	let drop = document.querySelector('.deshboard');
	let desh = document.querySelector('.ul');
	let showBtn = document.querySelector('#drop-btn');
	let display = 1;

	drop.addEventListener('click', (event) => {
		if (display === 1) {
			showBtn.classList.add('rotate');
			desh.style.display = 'block';
			display = 0;
		} else {
			showBtn.classList.remove('rotate');
			desh.style.display = 'none';
			display = 1;
		}
	});

	let currentCity = 'kurukshetra'; // Set the default city as 'Kurukshetra'

	// Fetch the cities data
	fetch('/api/cities/')
		.then((response) => response.json())
		.then((cities) => {
			// Initially render the city list excluding the default current city
			renderCityList(cities, currentCity);

			// Fetch events for Kurukshetra by default on page load
			fetchEventsForCity(currentCity);

			// Set up click event listener for city links after rendering
			document
				.getElementById('ul-1')
				.addEventListener('click', function (event) {
					const link = event.target.closest('.city-link');
					if (link) {
						event.preventDefault();
						const selectedCityName = link.getAttribute('data-city');

						// Update the current city to the clicked city
						currentCity = selectedCityName;

						// Update the city image in the header dynamically
						updateCityImage(selectedCityName);

						// Fetch events for the selected city
						fetchEventsForCity(selectedCityName);

						// Re-render the city list with the newly selected city removed
						renderCityList(cities, currentCity);

						// Redirect to the chosen city page after a short delay
						setTimeout(() => {
							window.location.href = link.href;
						}, 300);
					}
				});
		})
		.catch((error) => {
			console.error('Error fetching city data:', error);
		});

	// Function to render city list except for the current city
	function renderCityList(cities, excludeCity) {
		const cityList = document.getElementById('ul-1');
		cityList.innerHTML = ''; // Clear current city list

		// Filter out the city to exclude and render the rest
		const filteredCities = cities.filter(
			(city) => city.name.toLowerCase() !== excludeCity.toLowerCase()
		);

		filteredCities.forEach((city) => {
			const li = document.createElement('li');
			li.className = slugify(city.name);

			// Creating link element
			const a = document.createElement('a');
			a.href = 'javascript:void(0)';
			a.dataset.city = city.name;
			a.className = 'city-link';

			// Creating image element
			const img = document.createElement('img');
			img.src = `/static/core/asset/${slugify(city.name)}.png`;
			img.alt = city.name;

			// Appending image to link
			a.appendChild(img);

			// Appending link to list item
			li.appendChild(a);

			// Appending list item to the city list
			cityList.appendChild(li);
		});
	}

	// Function to slugify city names
	function slugify(text) {
		return text
			.toString()
			.toLowerCase()
			.replace(/\s+/g, '-') // Replace spaces with -
			.replace(/[^\w-]+/g, '') // Remove all non-word chars
			.replace(/--+/g, '-') // Replace multiple - with single -
			.trim(); // Trim any leading or trailing spaces
	}

	// Function to update the city image in the header dynamically
	function updateCityImage(cityName) {
		const cityImage = document.getElementById('city-img');
		const cityLink = document.querySelector('.city-img-header1 a');

		if (cityImage && cityLink) {
			cityImage.src = `/static/core/asset/${slugify(cityName)}.png`;
			cityImage.alt = cityName;
			cityLink.dataset.city = cityName;
		}
	}

	// second-dropdown
	let drop1 = document.querySelector('#drop1');
	let dash1 = document.querySelector('#ul-1');
	let showBtn1 = document.querySelector('#drop-btn-1');
	let cityimg = document.getElementById('city-img');
	let display1 = 1;

	drop1.addEventListener('click', () => {
		if (display1 === 1) {
			showBtn1.classList.add('rotate');
			dash1.style.display = 'block';
			cityimg.src = `/static/core/asset/${slugify(currentCity)}.png`;
			display1 = 0;
		} else {
			showBtn1.classList.remove('rotate');
			dash1.style.display = 'none';
			display1 = 1;
		}
	});

	const festGrid = document.getElementById('fest-grid');

	function fetchEventsForCity(cityName) {
		fetch(`/get-events/${encodeURIComponent(cityName)}/`)
			.then((response) => {
				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}
				return response.json();
			})
			.then((data) => {
				console.log(data);
				festGrid.innerHTML = '';

				data.events.forEach((event) => {
					festGrid.innerHTML += `
              <div class="event-title">${event.name}</div>
              <div class="event-date">${data.time}</div>
            `;
				});

				// Reset dropdown and image to reflect the selected city
				showBtn1.classList.remove('rotate');
				dash1.style.display = 'none';
				display1 = 1;
				cityimg.src = `/static/core/asset/${slugify(cityName)}.png`;
			})
			.catch((error) => console.error('Error fetching events:', error));
	}
});

// Sidebar functions
function showSidebar() {
	const sidebar = document.querySelector('.hamburger');
	sidebar.style.display = 'flex';
}

function hideSidebar() {
	const sidebar = document.querySelector('.hamburger');
	sidebar.style.display = 'none';
}
