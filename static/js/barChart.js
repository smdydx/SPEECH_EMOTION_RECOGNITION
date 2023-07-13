function buildMetaData() {
    console.log("Called buildMetaData");
    d3.json("/data", function(resultData) {
        if (resultData.predictedEmotion) {
            var predictedEmotion = resultData.predictedEmotion;
            displayPredictedEmotion(predictedEmotion);
        } else {
            setTimeout(buildMetaData, 300);
        }
    });
}

function displayPredictedEmotion(predictedEmotion) {
    // Get the element with ID "result"
    var resultElement = document.getElementById('result');
  
    // Set the text content of the element
    resultElement.textContent = "Predicted Emotion: " + predictedEmotion;
  
    // Set the background color, text color, padding, and text alignment
    resultElement.style.backgroundColor = "green";
    resultElement.style.color = "white";
    resultElement.style.textAlign = "center";
    resultElement.style.padding = "50px";
  
    // Set the display, alignment, height, and width to center the element
    resultElement.style.display = "flex";
    resultElement.style.justifyContent = "center";
    resultElement.style.alignItems = "center";
    resultElement.style.height = "100px";
    resultElement.style.width = "200px";
}

