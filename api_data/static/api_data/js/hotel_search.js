 async function loadCities() {
    try {
        const response = await fetch('/hotel_search/get_cities/');

        if (!response.ok) {
            throw new Error('Failed to load cities');
        }

        allCities = await response.json();
        console.log(`Loaded ${allCities.length} cities`);

        return allCities;

    } catch (error) {
        console.error('Error loading cities:', error);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('autoComplete').value = '';

    var allCities = loadCities();

    var config = {
        placeHolder: "Search for a city to view hotels...",
        data: {
            src: allCities
        },
        resultItem: {
            highlight: true,
        },
        events: {
            input: {
                selection: (event) => {
                    const selection = event.detail.selection.value;
                    autoCompleteJS.input.value = selection;
                }
            }
        }
    }
    const autoCompleteJS = new autoComplete(config);
});

window.onload = function() {
};