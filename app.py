import io
import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*":{"origins":"*"}})

# Replace with actual paths
MODEL_PATH = '/home/ubuntu/CNN/checkpoints/image_classifier.keras'
TARGET_NAMES = ['African_Almond', 'Avocado', 'Cashew', 'Guava', 'Mango']

# Load the model architecture and weights
model = load_model(MODEL_PATH)

def preprocess_image(image):
    # Convert to RGB
    image = image.convert('RGB')

    # Resize the image
    image = image.resize((256, 256))  # Adjust to match the model input size

    # Convert to a NumPy array
    image = img_to_array(image)

    # Normalize the image
    image = image / 255.0

    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    return image

@app.route('/')
def index():
    return "Hello application"

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get the uploaded image
        image_file = request.files['image']
        
        # Validate the image
        if image_file and allowed_file(image_file.filename):
            try:
                # Load and preprocess the image
                image = load_img(io.BytesIO(image_file.read()))
                preprocessed_image = preprocess_image(image)

                # Make prediction
                prediction = model.predict(preprocessed_image)
                predicted_class = np.argmax(prediction)

                # Get the predicted class name
                predicted_class_name = TARGET_NAMES[predicted_class]
                return jsonify({'prediction': predicted_class_name})

            except Exception as e:
                return jsonify({'error': str(e)})
        else:
            return jsonify({'error': 'Allowed image types: jpg, jpeg, png'})

def allowed_file(filename):
    allowed_extensions = {'jpeg', 'jpg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

if __name__ == '__main__':
    app.run(debug=True)
