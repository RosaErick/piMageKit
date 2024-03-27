from flask import Flask, request, render_template, send_file
from rembg import remove
from PIL import Image
from io import BytesIO

app = Flask(__name__)

def process_image(image_data, option, resize_dims=None, crop_dims=None):
    if option == 'remove_bg':
        return remove_background(image_data)
    elif option == 'remove_metadata':
        return remove_metadata(image_data)
    elif option == 'resize' and resize_dims:
        return resize_image(image_data, resize_dims)
    elif option == 'crop' and crop_dims:
        return crop_image(image_data, crop_dims)
    else:
        raise ValueError('Invalid processing option or missing parameters.')

def remove_background(image_data):
    output_image = remove(image_data)
    return output_image

def remove_metadata(image_data):
    image = Image.open(BytesIO(image_data))
    clean_data = BytesIO()
    image.save(clean_data, format='PNG', quality=100)
    clean_data.seek(0)
    return clean_data.getvalue()

def resize_image(image_data, resize_dims):
    image = Image.open(BytesIO(image_data))
    resized_image = image.resize(resize_dims)
    resized_data = BytesIO()
    resized_image.save(resized_data, format='PNG')
    resized_data.seek(0)
    return resized_data.getvalue()

def crop_image(image_data, crop_dims):
    image = Image.open(BytesIO(image_data))
    cropped_image = image.crop(crop_dims)
    cropped_data = BytesIO()
    cropped_image.save(cropped_data, format='PNG')
    cropped_data.seek(0)
    return cropped_data.getvalue()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', message='No selected file')

        image_data = file.read()
        option = request.form.get('option')
        
       
        resize_width = request.form.get('resize_width', type=int)
        resize_height = request.form.get('resize_height', type=int)
        crop_left = request.form.get('crop_left', type=int)
        crop_upper = request.form.get('crop_upper', type=int)
        crop_right = request.form.get('crop_right', type=int)
        crop_lower = request.form.get('crop_lower', type=int)

        try:
            processed_data = process_image(
                image_data, 
                option, 
                resize_dims=(resize_width, resize_height) if option == 'resize' else None,
                crop_dims=(crop_left, crop_upper, crop_right, crop_lower) if option == 'crop' else None
            )
            return send_file(
                BytesIO(processed_data),
                as_attachment=True,
                download_name=file.filename.replace('.jpg', '.png'),
                mimetype='image/png'
            )
        except ValueError as e:
            return render_template('index.html', message=str(e))

    return render_template('index.html', message=None)

if __name__ == '__main__':
    app.run(debug=True)
