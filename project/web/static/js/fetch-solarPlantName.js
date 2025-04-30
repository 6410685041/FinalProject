document.addEventListener("DOMContentLoaded", function(){
    fetch('http://127.0.0.1:5003/SolarPlant/all')
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok: ' + response.statusText);
      }
      return response.json();
  })
  .then(string_data => {
      try {
          const data = JSON.parse(string_data);
          const selectElement = document.getElementById('solarPlant');

          if (Array.isArray(data)) {
              data.forEach(item => {
                  const option = document.createElement('option');
                  option.value = item.solarPlant_id;
                  option.textContent = item.solarPlant_name;
                  selectElement.appendChild(option);
              });
          } else {
              console.error('Expected an array but received:', data);
          }
      } catch (error) {
          console.error('Error parsing JSON:', error);
      }
    })
    .catch(error => console.error('Error fetching data:', error.message));
  });