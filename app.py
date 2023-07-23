from flask import Flask, render_template, request,send_file,jsonify
from PIL import Image
import numpy as np
import tensorflow as tf
import cv2
import secrets
model_path = './model.tflite'
import os
import shutil
from flask_cors import CORS
import requests
import subprocess
import json

app = Flask(__name__)
# cors = CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
CORS(app, origins=["http://localhost:4200"])

# https://deep-learning-rbl-project.netlify.app/

# https://deep-learning-rbl-project.netlify.app/

# define the path to the static folder
DETECTION_THRESHOLD = 0.4
#c
classes = [ 'red','white','ripe','green']

# Define a list of colors for visualization
COLORS=np.array([[255, 0, 0],[255, 255, 255],[255, 255, 0],[0, 65, 0]])

def preprocess_image(image_arr, input_size):
    """Preprocess the input image array to feed to the TFLite model"""
    img = tf.convert_to_tensor(image_arr, dtype=tf.uint8)
    original_image = img
    resized_img = tf.image.resize(img, input_size)
    resized_img = resized_img[tf.newaxis, :]
    resized_img = tf.cast(resized_img, dtype=tf.uint8)
    return resized_img, original_image

results = []
def detect_objects(interpreter, image, threshold):
  """Returns a list of detection results, each a dictionary of object info."""

  signature_fn = interpreter.get_signature_runner()

  # Feed the input image to the model
  output = signature_fn(images=image)

  # Get all outputs from the model
  count = int(np.squeeze(output['output_0']))
  scores = np.squeeze(output['output_1'])
  classes = np.squeeze(output['output_2'])
  boxes = np.squeeze(output['output_3'])

  
  for i in range(count):
    if scores[i] >= threshold:
      result = {
        "bounding_box": boxes[i],
        "class_id": classes[i],
        "score": scores[i]
      }
      results.append(result)
  return results

def run_odt_and_draw_results(image_path, interpreter, threshold=0.5):
  """Run object detection on the input image and draw the detection results"""
  # Load the input shape required by the model
  _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

  # Load the input image and preprocess it
  preprocessed_image, original_image = preprocess_image(
      image_path,
      (input_height, input_width)
    )

  # Run object detection on the input image
  
  results = detect_objects(interpreter, preprocessed_image, threshold=threshold)

  # Plot the detection results on the input image
  original_image_np = original_image.numpy().astype(np.uint8)
  for obj in results:
    # Convert the object bounding box from relative coordinates to absolute
    # coordinates based on the original image resolution
    ymin, xmin, ymax, xmax = obj['bounding_box']
    xmin = int(xmin * original_image_np.shape[1])
    xmax = int(xmax * original_image_np.shape[1])
    ymin = int(ymin * original_image_np.shape[0])
    ymax = int(ymax * original_image_np.shape[0])
    

    # Find the class index of the current object
    class_id = int(obj['class_id'])

    # Draw the bounding box and label on the image
    color = [int(c) for c in COLORS[class_id]]
    cv2.rectangle(original_image_np, (xmin, ymin), (xmax, ymax), color, 2)
    # Make adjustments to make the label visible for all objects
    y = ymin - 15 if ymin - 15 > 15 else ymin + 15
    label = "{}: {:.0f}%".format(classes[class_id], obj['score'] * 100)
    cv2.putText(original_image_np, label, (xmin, y),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

  # Return the final image
  original_uint8 = original_image_np.astype(np.uint8)
  return original_uint8
model_path = './model.tflite'
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()



@app.before_request
def clear_static_folder():
    """Clear the static folder before each request"""
    if request.endpoint == 'static':
        return
    shutil.rmtree(app.static_folder)
    os.mkdir(app.static_folder)
    url = 'http://127.0.0.1:4200/'
    

def numpy_encoder(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the uploaded image file
        image = request.files['file']
        random_string = secrets.token_hex(8)
        
        im = Image.open(image)
        # im.save(f'static/input{random_string}.png')
        im.thumbnail((512, 512), Image.ANTIALIAS)
        im_arr = np.array(im)

        detection_result_image = run_odt_and_draw_results(
            im_arr,
            interpreter,
            threshold=DETECTION_THRESHOLD
        )
        # img = Image.fromarray(detection_result_image)
        # img.save(f'static/predicted{random_string}.png')
        
        # Render the result template with the input and predicted images
        # return render_template('result.html', input_image=f'input{random_string}.png', predicted_image=f'predicted{random_string}.png')
    
    # Render the home template for GET request
    # return render_template('home.html')
    # return send_file(f'static/predicted{random_string}.png', mimetype='image/png')
    with open("imag.txt", "w") as file:
      file.write(str(detection_result_image.tolist()))
    subprocess.check_output(['python', 'test.py'], text=True)
    current_path = os.getcwd()
    # return detection_result_image.tolist()
    # results.append(current_path+'\TestOutput1.png')
    ans = []
    for x in results:
      ans.append(x['class_id'])
    print(ans)
    return str(ans)
  

    
if __name__ == '__main__':
    app.run(port=80,debug=True)
