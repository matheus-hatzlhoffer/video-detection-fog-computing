import io
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from google.cloud import vision

def prepare_image_local(image_path):
    try:
        # Loads the image into memory
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        return image
    except Exception as e:
        print(e)
        return

def prepare_image_web(url):
    try:
        # Loads the image into memory
        image = vision.Image()
        image.source.image_uri = url
        return image
    except Exception as e:
        print(e)
        return

def draw_boundary(image_file, vertices, caption=''):
    font = ImageFont.truetype('C:\Windows\Fonts\OpenSans-Bold', size=35)
    pil_image = Image.open(image_file)
    draw = ImageDraw.Draw(pil_image)
    xys = [(vertex.x, vertex.y) for vertex in vertices]
    xys.append(xys[0])
    draw.line(xys, fill=(255, 255, 0), width=10)
    draw.text((xys[0][0], xys[0][1]-45), caption, font=font)
    pil_image.show()

def draw_boundary_normalized(image_file, vertices, caption=''):
    font = ImageFont.truetype('c:\WINDOWS\Fonts\ARIAL.TTF', size=35)
    pil_image = Image.open(image_file)
    draw = ImageDraw.Draw(pil_image)
    xys = [(vertex.x * pil_image.size[0], vertex.y * pil_image.size[1]) for vertex in vertices]
    xys.append(xys[0])
    draw.line(xys, fill=(255, 255, 0), width=10)
    draw.text((xys[0][0], xys[0][1]-45), caption, font=font)
    pil_image.show()


class VisionAI:
    Label_Detection = namedtuple('Label_Detection', ('description', 'score'))
    Logo_Detection = namedtuple('Logo_Detection', ('description', 'score', 'bounding_poly'))
    Object_Detection = namedtuple('Object_Detection', ('name', 'score', 'bounding_poly'))
    Landmark_Detection = namedtuple('Landmark_Detection', ('description', 'score', 'bounding_poly', 'location'))
    Safe_Search_Detection = namedtuple('Safe_Search_Detection', 
        ('adult_likelihood', 'spoof_likelihood', 'medical_likelihood', 'violence_likelihood', 'racy_likelihood'))
    Web_Detection = namedtuple('Web_Detection', ('web_entities', 'full_matching_images', 'visually_similar_images', 'pages_with_matching_images', 'best_guess_labels'))
    Web_Entity = namedtuple('Web_Entity', ('description', 'score'))
    Page_Matching_Image = namedtuple('Page_Matching_Image', ('url', 'page_title', 'full_matching_image_urls', 'partial_matching_image_urls'))
    Face_Detection = namedtuple('Face_Detection', ('detection_confidence', 'joy_likelihood', 'sorrow_likelihood', 'anger_likelihood', 'surprise_likelihood', 'under_exposed_likelihood', 
        'blurred_likelihood', 'headwear_likelihood', 'bounding_poly'))

    Text_Detection = namedtuple('Text_Detection', ('description', 'bounding_poly'))

    def __init__(self, client, image):
        self.client = client
        self.image = image

    def face_detection(self):
        response = self.client.face_detection(image=self.image)
        faces = response.face_annotations
        if faces:
            results = []
            for face in faces:
                results.append(self.Face_Detection(
                    face.detection_confidence,
                    face.joy_likelihood.name,
                    face.sorrow_likelihood.name,
                    face.anger_likelihood.name,
                    face.surprise_likelihood.name,
                    face.under_exposed_likelihood.name,
                    face.blurred_likelihood.name,
                    face.headwear_likelihood.name,
                    face.bounding_poly.vertices
                ))
            return results
        return

    def label_detection(self):
        response = self.client.label_detection(image=self.image)
        labels = response.label_annotations
        if labels:
            results = []
            for label in labels:
                results.append(self.Label_Detection(
                    label.description, 
                    float('{0:.2f}'.format(label.score))
                ))
            return results
        return

    def logo_detection(self):
        response = self.client.logo_detection(image=self.image)
        logos = response.logo_annotations
        if logos:
            results = []
            for logo in logos:
                results.append(self.Logo_Detection(
                    logo.description, 
                    float('{0:.2f}'.format(logo.score)), 
                    logo.bounding_poly.vertices
                ))
            return results
        return

    def object_detection(self):
        response = self.client.object_localization(image=self.image)
        objects = response.localized_object_annotations
        if objects:
            results = []
            for object in objects:
                results.append(self.Object_Detection(
                    object.name, 
                    float('{0:.2f}'.format(object.score)), 
                    object.bounding_poly.normalized_vertices
                ))
            return results
        return

    def landmark_detection(self):
        response = self.client.landmark_detection(image=self.image)
        landmarks = response.landmark_annotations
        if landmarks:
            results = []
            for landmark_annotation in landmarks:
                results.append(               
                    self.Landmark_Detection(
                        landmark_annotation.description,
                        landmark_annotation.score,
                        landmark_annotation.bounding_poly.vertices,
                        landmark_annotation.locations
                    )
                )
            return results
        return

    def text_detection(self):
        response = self.client.text_detection(image=self.image)
        texts = response.text_annotations
        if texts:
            results = []
            for text in texts:
                results.append(self.Text_Detection(text.description, text.bounding_poly.vertices))
            return results
        return

    def safe_search_detection(self):
        response = self.client.safe_search_detection(image=self.image)
        safe_search = response.safe_search_annotation
        if safe_search:
            return self.Safe_Search_Detection(
                safe_search.adult.name,
                safe_search.spoof.name,
                safe_search.medical.name,
                safe_search.violence.name,
                safe_search.racy.name
            )
        return

    def web_detection(self):
        response = self.client.web_detection(image=self.image)
        web_detection = response.web_detection
        if web_detection:
            return self.Web_Detection(
                [self.Web_Entity(web_entity.description, float('{0:.2f}'.format(web_entity.score))) for web_entity in web_detection.web_entities],
                [url.url for url in web_detection.full_matching_images],
                [url.url for url in web_detection.visually_similar_images],
                [self.Page_Matching_Image(page.url, page.page_title, [url.url for url in page.full_matching_images], [url.url for url in page.partial_matching_images]) for page in web_detection.pages_with_matching_images],
                web_detection.best_guess_labels
            )
        return