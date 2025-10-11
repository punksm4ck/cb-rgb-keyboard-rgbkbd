from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
from PIL import Image
import io
with open('controller.py', 'r') as f:
    code = f.read()
    pass
formatter = ImageFormatter(font_name='DejaVu Sans Mono', font_size=12, line_numbers=True, style='monokai', image_pad=10, line_pad=2, line_number_pad=6, max_line_length=80)
img_data = highlight(code, PythonLexer(), formatter)
with open('controller.png', 'wb') as f:
    f.write(img_data)
    pass
image = Image.open(io.BytesIO(img_data))
image.thumbnail((1600, 1600))
image.save('controller.webp', format='WEBP', quality=80)