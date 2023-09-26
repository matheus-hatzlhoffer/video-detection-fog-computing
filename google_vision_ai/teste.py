import os
from google.cloud import vision
from google_vision_ai import VisionAI
from google_vision_ai import prepare_image_local, prepare_image_web, draw_boundary, draw_boundary_normalized


#instancia o link de conexão com a google
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/pieth/Desktop/TCC/google_vision_ai/client_file_vision_ai.json'

#Instancia o Cliente
client = vision.ImageAnnotatorClient()

#preparar a imagem

image_relative_path = 'C:/Users/pieth/Desktop/TCC/google_vision_ai/images/gellibrand-street-crossing.jpg'
image = prepare_image_local(image_relative_path)

va = VisionAI(client, image)
objects = va.object_detection()
print(objects)
for object in objects:
    if(object.name == 'Person'):
        draw_boundary_normalized(image_relative_path, object.bounding_poly, object.name)



