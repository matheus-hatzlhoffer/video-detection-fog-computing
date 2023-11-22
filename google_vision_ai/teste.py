import os
from google.cloud import vision
from google_vision_ai import VisionAI
from google_vision_ai import prepare_image_local, prepare_image_web, draw_boundary, draw_boundary_normalized
from functions import get_images_analisis


#instancia o link de conexão com a google
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './client_file_vision_ai.json'

image_list = [
    './images/5bf5ac6c2ba20.jpg',
    './images/25404103.jpg',
    './images/Buraco.jpg',
    './images/gellibrand-street-crossing.jpg',
    './images/gettyimages-1181241726-612x612.jpg',
    './images/governo-entrega-obras-de-pavimentacao-asfaltica-de-27-ruas-no-bairro-quarta-linha.jpg',
    './images/Pare 2.jpg',
    './images/Pare 3.jpg',
    './images/pare_horizontal2.jpg',
    './images/pare_horozintal.jpg',
    './images/pare.jpeg',
    './images/pare+rotatoria.jpg',
    './images/rua2_0.jpg',
    './images/Streetbit_Stream.jpg',
    './images/gellibrand-street-crossing.jpg'
]

get_images_analisis(image_list)



