from rest_framework.decorators import api_view
from rest_framework.response import Response
import base64
from PIL import Image
import os
import requests
import time

@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'GET':
        return Response({"message": "get"})
    elif request.method == 'POST':
        base64_string = request.data['base64']
        imgdata = base64.b64decode(base64_string)
        file_name = os.path.join(os.path.dirname(__file__), 'image.png')
        with open(file_name, 'wb') as f:
            f.write(imgdata)
        
        crop_areas = [
        (115,855,395,1135),(425,855,705,1135),(735,855,1015,1135),
        (115,1165,395,1445),(425,1165,705,1445),(735,1165,1015,1445),
        (115,1475,395,1755),(425,1475,705,1755),(735,1475,1015,1755)
        ]
    
        img = Image.open(file_name)
        arr_b64 = []
        def crop_image(img, crop_area, new_filename):
            cropped_image = img.crop(crop_area)
            cropped_image.save(new_filename)   
        # Loops through the "crop_areas" list and crops the image based on the coordinates in the list
        for i, crop_area in enumerate(crop_areas):
            filename = os.path.splitext(file_name)[0]
            ext = os.path.splitext(file_name)[1]
            new_filename = filename + '_ngon' + str(i+1) + ext
            crop_image(img, crop_area, new_filename)
            with open(new_filename, "rb") as img_file:
                b64_string = base64.b64encode(img_file.read())
                b64_image = b64_string.decode('utf-8')
                arr_b64.append(b64_image)

        images= {
            '0': arr_b64[0],
            '1': arr_b64[1],
            '2': arr_b64[2],
            '3': arr_b64[3]
        }

        target = 'Please click each image containing sunflowers in a field'

        images2= {
            '4': arr_b64[4],
            '5': arr_b64[5],
            '6': arr_b64[6],
            '7': arr_b64[7],
            '8': arr_b64[8]
        }
        def FetchAPI(image,target):
            return requests.post('https://free.nocaptchaai.com/solve', json={
                'images': image,
                'target': target,
                'method':'hcaptcha_base64'
            },
            headers={
                'Content-type': 'application/json',
                'uid': '123',
                'apikey': 'legen92-113316d6-9765-fff9-839e-91911fe19387'
            })
        result = []
        while True:
            res = FetchAPI(image=images,target=target)
            if res.json()["status"] == 'new':
                print("status-1 : new")
                time.sleep(2)
            elif res.json()["status"] == 'skip':
                print("status-1 : skip")
                return Response({'message':'skip'})
            else:
                print("status-1 : solve")
                for e in res.json()["solution"]:
                    result.append(e)
                break

        while True:
            res = FetchAPI(image=images2,target=target)
            if res.json()["status"] == 'new':
                print("status-2 : new")
                time.sleep(2)
            elif res.json()["status"] == 'skip':
                print("status-2 : skip")
                return Response({'message':'skip'})
            else:
                print("status-2 : solve")
                for e in res.json()["solution"]:
                    result.append(e)
                break
        
        return Response({"message": "success","result":result})
