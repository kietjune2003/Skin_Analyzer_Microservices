from flask import render_template, request, jsonify
from .objectdetection_service import detect_objects
from .classification_service import classify_image
from .utils import crop_regions, draw_boxes
from PIL import Image
import io
import os

def register_routes(app):

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/analyze', methods=['GET', 'POST'])
    def analyze():
        if request.method == 'GET':
            return render_template('index.html')

        file = request.files.get('image')
        if not file:
            return render_template('index.html', error='No image uploaded.')

        image = Image.open(io.BytesIO(file.read())).convert('RGB')

        detections = detect_objects(image)

        if not detections:
            return render_template('result.html', message='No relevant regions detected.')

        cropped_images = crop_regions(image, detections)

        results = []
        for crop, det in zip(cropped_images, detections):
            disease_pred = classify_image(crop)
            results.append({
                'detected_class': det['class'],
                'confidence': det['confidence'],
                'bbox': det['bbox'],
                'disease_prediction': disease_pred
            })

        os.makedirs('app/static', exist_ok=True)
        output_path = 'app/static/result.jpg'
        image_with_boxes = draw_boxes(image.copy(), detections)
        image_with_boxes.save(output_path)

        return render_template(
            'result.html',
            results=results,
            result_image='/static/result.jpg'
        )

    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'})
