document.getElementById("create-solarplant").onsubmit = function(event) {
    const name = document.getElementById("solarPlant_name").value;
    const location = document.getElementById("location").value;
    if (name.length < 5) {
        alert("Please rewrite the Solar Plant name to be at least 5 characters.");
        event.preventDefault(); // Prevent form submission
    } else {
        isValidLocation(location, function(isValid) {
            if (!isValid) {
                alert("Please enter a valid location.");
                event.preventDefault();
            } 
        });
    }
};

function isValidLocation(location, callback) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(location)}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) { // Check if any results returned
                callback(true);
            } else {
                callback(false);
            }
        })
        .catch(() => {
            callback(false); // Handle errors
        });
}