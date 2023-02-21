from rest_framework.decorators import api_view
from rest_framework.response import Response
import base64
import os
import ocrspace
api = ocrspace.API()

@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'GET':
        return Response({"message": "success get"})
    elif request.method == 'POST':
        # base64_string = request.data["data"]
        # imgdata = base64.b64decode(base64_string)
        # file_name = os.path.join(os.path.dirname(__file__), 'image.png')

        # with open(file_name, 'wb') as f:
        #     f.write(imgdata)

        # text = api.ocr_file(file_name).replace("\r\n", " ").strip()
        return Response({"message": "success"})
