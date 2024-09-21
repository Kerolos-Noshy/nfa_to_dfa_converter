import base64
OUTPUT_FOLDER = 'static'

def get_svg_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f'<img src="data:image/svg+xml;base64,{encoded}">'
