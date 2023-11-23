from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .forms import ImageForm
from .model import process_image_with_yolo
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ImageUploadSerializer  


# Create your views here.
@require_http_methods(["GET", "POST"])
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            
            # Processamento da imagem com YOLO
            image_base64 = process_image_with_yolo(image)

            return render(request, 'upload_success.html', {'image_base64': image_base64})

    else:
        form = ImageForm()
    return render(request, 'upload_image.html', {'form': form})


class ImageUploadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            
            # Processamento da imagem com YOLO
            image_base64 = process_image_with_yolo(image)

            # Retorna a imagem processada como resposta da API
            return Response({'image_base64': image_base64})
        return Response(serializer.errors, status=400)
