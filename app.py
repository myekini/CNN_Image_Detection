import io
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np

app = Flask(__name__)

# Replace with actual paths
MODEL_PATH = 'checkpoints/model_keras_leaf.h5'
CHECKPOINT_PATH = 'checkpoints/model_weights-leaf.weights.h5'
TARGET_NAMES = ['Class 0 (African_Almond)', 'Class 1 (Avocado)', 'Class 2 (Cashew)', 'Class 3 (Guava)','Class 4 (Mango)']

# Load the model architecture and weights
model = load_model(MODEL_PATH)
model.load_weights(CHECKPOINT_PATH)


def preprocess_image(image):
    # Convert to RGB (if needed)
    image = image.convert('RGB')

    # Resize the image
    image = image.resize((224, 224))

    # Convert to a NumPy array
    image = img_to_array(image)

    # Normalize the image
    image = image / 255.0

    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    # Convert to grayscale
    image = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])  # Convert RGB to grayscale

    # Reshape the image for the model's input format
    image = np.expand_dims(image, axis=-1)

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
