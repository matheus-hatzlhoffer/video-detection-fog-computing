import io
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from google.cloud import vision
from google_vision_ai import prepare_image_local, VisionAI

def draw_multiple_boundary_normalized(image_file, list):
    font = ImageFont.truetype('c:\WINDOWS\Fonts\ARIAL.TTF', size=35)
    pil_image = Image.open(image_file)
    draw = ImageDraw.Draw(pil_image)

    for item in list:
        xys = [(vertex.x * pil_image.size[0], vertex.y * pil_image.size[1]) for vertex in item[0]]
        xys.append(xys[0])
        draw.line(xys, fill=item[2], width=10)
        draw.text((xys[0][0], xys[0][1]-45), item[1], font=font)
    pil_image.show()

def get_images_analisis(image_list):
    client = vision.ImageAnnotatorClient()
    for image_relative_path in image_list:
        image = prepare_image_local(image_relative_path)

        va = VisionAI(client, image)
        objects = va.object_detection()
        if objects is not None:
            list = []
            for object in objects:
                if(object.name == 'Person'):
                    list.append([object.bounding_poly, object.name, (255, 255,0)])
                elif(object.name == 'Car'):
                    list.append([object.bounding_poly, object.name, (0,0,255)])
                else:
                    list.append([object.bounding_poly, object.name, (0,255,0)])

            draw_multiple_boundary_normalized(image_relative_path, list)
        else:
            pil_image = Image.open(image_relative_path)
            pil_image.show()