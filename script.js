const video = document.getElementById('camera');
const captureBtn = document.getElementById('capture-btn');
const welcomeBtn = document.getElementById('welcome-btn');
const predictionList = document.getElementById('prediction-list');

// Start camera
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Error accessing camera: ", err);
    });

// Welcome audio
welcomeBtn.addEventListener('click', () => {
    speakText("Hey there! Welcome to Guiding Eyes. Allow us to be your eyes for a while. We promise to guide you safely and make you feel loved every step of the way.");
});

// Speak with softer, sweeter voice
function speakText(text) {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);

    const voices = synth.getVoices();
    const sweetVoice = voices.find(voice => voice.name.includes('Female') || voice.name.includes('Google UK English Female') || voice.name.includes('Samantha'));

    if (sweetVoice) {
        utterance.voice = sweetVoice;
    }

    utterance.pitch = 1.2;
    utterance.rate = 1;
    synth.speak(utterance);
}

// Capture and Predict
captureBtn.addEventListener('click', async () => {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
        console.log('Sending image blob to backend...');
        const formData = new FormData();
        formData.append('image', blob, 'capture.jpg');

        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                body: formData
            });

            console.log('Response from backend:', response);
            const data = await response.json();
            console.log('Prediction data:', data);
            showPredictions(data);
            speakPredictions(data);
        } catch (error) {
            console.error('Error sending image:', error);
            alert('Oops! Could not get a prediction. Please try again.');
        }
    }, 'image/jpeg');
});

// Show Predictions
function showPredictions(predictions) {
    predictionList.innerHTML = '';
    predictions.forEach(pred => {
        const item = document.createElement('li');
        item.textContent = `Label: ${pred.label}, Confidence: ${pred.confidence.toFixed(2)}, BBox: ${pred.bbox}`;
        predictionList.appendChild(item);
    });
}

// Speak Predictions
function speakPredictions(predictions) {
    if (predictions.length === 0) {
        speakText("No objects detected. Please try again.");
        return;
    }

    let speechText = "Detected: ";
    predictions.forEach(pred => {
        speechText += `${pred.label} with ${Math.round(pred.confidence * 100)} percent confidence. `;
    });

    speakText(speechText);
}

// Preload voices
window.speechSynthesis.onvoiceschanged = () => {};
