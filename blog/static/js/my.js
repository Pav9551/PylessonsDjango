// Define the sendGetRequest function
function sendGetRequest() {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/users/get-data/');
  xhr.onload = function() {
    if (xhr.status === 200) {
      // Success! Parse the response as JSON
      var response = JSON.parse(xhr.responseText);
      // Access the 'token' property and update the span
      document.getElementById('token').innerHTML = response.token;
    } else {
      // Oops! Something went wrong
      console.log('Request failed.  Returned status of ' + xhr.status);
    }
  };
  xhr.send();
}

// Export the sendGetRequest function
export { sendGetRequest };







