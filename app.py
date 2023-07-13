from flask import Flask, jsonify, render_template, request
import numpy as np
import librosa
import librosa.display
from joblib import load

app = Flask(__name__)
app.secret_key = 'upgraded potato'

results_dict = {
    "predictedEmotion": [],
}

# Functions
def input_parser(input_file):
    try:
        X, sample_rate = librosa.load(input_file, res_type='kaiser_fast') 
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=128).T, axis=0) 
    except Exception as e:
        print("Error encountered while parsing file:", input_file)
        return None
    feature = mfccs.tolist()
    print("feature:", feature)
    return feature

def get_results_dict_from_svc_model(model, arr2d):
    pred_emotion = model.predict(arr2d)
    results_dict["predictedEmotion"] = pred_emotion[0]
    return results_dict

def get_results_dict_from_h5_model(model, arr2d):
    # Emotion h5 model
    probs = model.predict(arr2d)
    print("probs[0].tolist():", str(probs[0].tolist()))
    emotion_labels = ['neutral', 'calm', 'happy', 'sad', 'angry', 'fearful', 'disgust', 'surprise']
    pred_emotion = emotion_labels[int(np.argmax(probs))]
    results_dict["predictedEmotion"] = pred_emotion
    return results_dict

def model_test(input_file):
    user_file = {'filepath': [input_file]}
    # Import models
    model = load('F:\FINAL_PROJECTSMDYDX\models\CNN_model.sav')
   
    # Transforming data into a vector representation
    feature = input_parser(input_file)
    if feature is None:
        return jsonify({"error": "Error encountered while parsing the file."})
    arr = np.array(feature)
    arr2d = np.reshape(arr, (1, 128))
    
    # Evaluation of the models
    results_dict = get_results_dict_from_svc_model(model, arr2d)
    print(results_dict)
    return results_dict


# Add a new route for the introduction page
@app.route("/introduction")
def introduction():
    return render_template('introduction.html')

@app.route("/objectives")
def objectives():
    return render_template('objectives.html')

@app.route("/diagram")
def diagram():
    return render_template('diagram.html')
@app.route("/method")
def method():
    return render_template('method.html')
@app.route("/aim")
def aim():
    return render_template('aim.html')
# App routes
@app.route("/", methods=['GET', 'POST'])
def record_page():
    print("Responding to record page route request")
    if request.method == "POST":
        f = request.files['audio_data']
        results = model_test(f)
        print('File uploaded successfully')
        print(results)
        return jsonify(results)
    else:
        return render_template('index.html')

@app.route("/data")
def data():
    return jsonify(results_dict)

if __name__ == "__main__":
    app.run(debug=True)
    

