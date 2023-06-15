/**
 * Performs an API request to the Musicgen hosted endpoint, and writes the resulting
 * output to file.
 */

const path = require("path");
const Max = require("max-api");
const fs = require("fs");
const https = require("https");

// Output file name
const outFile = "out.mp3";

/**
 * Converts a base64 string to an audio file and saves it to the specified outputPath.
 * @param {string} base64String - The base64 string representing the audio data.
 * @param {string} outputPath - The path where the output audio file will be saved.
 */
function base64ToAudio(base64String, outputPath) {
  // Convert base64 string to buffer
  const buffer = Buffer.from(base64String, "base64");

  // Write buffer to file
  fs.writeFile(outputPath, buffer, (error) => {
    if (error) {
      console.error("Error:", error);
    } else {
      console.log("Audio file successfully saved!");
    }
  });
}

/**
 * Performs an HTTP POST request to the specified URL with the provided data.
 * @param {string} url - The URL to which the POST request will be sent.
 * @param {Object} data - The data to be sent in the POST request body.
 * @param {Function} callback - The callback function to handle the response.
 */
function performHttpPost(url, data, callback) {
  // Convert data to JSON string
  const postData = JSON.stringify(data);

  // Set request options
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(postData),
    },
  };

  // Send the POST request
  const req = https.request(url, options, (res) => {
    let responseData = "";

    // Collect response data
    res.on("data", (chunk) => {
      responseData += chunk;
    });

    // Handle response end
    res.on("end", () => {
      callback(null, responseData);
    });
  });

  // Handle request errors
  req.on("error", (error) => {
    callback(error, null);
  });

  // Write data to request body and end the request
  req.write(postData);
  req.end();
}

Max.addHandler("request", (url, prompt, duration, temperature) => {
  // Prepare the data to be sent in the POST request
  url = url + "/inference";

  const data = {
    prompt: prompt,
    duration: duration,
    temperature: temperature,
  };

  // Inform Max that the request is starting
  Max.post("Starting request...");

  // Perform the POST request
  performHttpPost(url, data, (error, response) => {
    if (error) {
      // Handle error if the request fails
      Max.post("Error: " + error);
    } else {
      // Parse the response from the POST request
      const parsedResponse = JSON.parse(response);

      // Output the processing time of the request
      Max.post(
        "Success! Processing time: " +
          parsedResponse["result"]["processing_time_ms"]
      );

      // Convert the base64 string to an audio file
      base64ToAudio(parsedResponse["result"]["prediction"], outFile);

      // Output the processing time to Max/MSP
      Max.outlet(parsedResponse["result"]["processing_time_ms"]);
    }
  });
});
