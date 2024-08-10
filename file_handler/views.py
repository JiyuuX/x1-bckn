from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UserProjects
from .serializers import UserProjectsSerializer
from .models import UserProjects, UserProjectsData, UserProjectShapes, AllLabels
from users.models import UserAccount  
from django.db import transaction #atomic
from django.shortcuts import get_object_or_404
from rest_framework import status
import requests
import csv
import os
import json
import random


@api_view(['POST'])
def search_label(request):
    label = request.data.get('label', '').lower()
    if label:
        labels = AllLabels.objects.filter(label__iexact=label)  # Case-insensitive arama
        if labels.exists():
            response_data = []
            for label in labels:
                response_data.append({
                    'label': label.label,
                    'x': random.uniform(0, 1),  # 0-1 arası rastgele bir değer
                    'y': random.uniform(0, 1),  # 0-1 arası rastgele bir değer
                    'size': 1, #random.uniform(0, 1),  # 0-1 arası rastgele bir değer
                    'color': '#FF0000'  # Sabit kırmızı renk kodu
                })
            return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)
        else:
            # Eğer etiket bulunamazsa Instagram'a istek gönder
            try:
                username = label  # Kullanıcı adını buraya koyun
                # Kullanıcı adı ile kullanıcı ID'sini alma isteği
                user_id_url = f"https://www.instagram.com/{username}/?__a=1"
                user_response = requests.get(user_id_url)
                user_data = user_response.json()
                user_id = user_data['graphql']['user']['id']
                
                # Kullanıcı ID'sini kullanarak veri çekme
                headers = {
                    'Cookie': 'ig_did=0513863C-41F1-47BF-B2BA-8432258316B6; ig_nrcb=1; datr=lcDVZelvpOEtdAhw-97fqiNS; ds_user_id=2540082; fbm_124024574287414=base_domain=.instagram.com; ps_n=1; ps_l=1; csrftoken=Q3J9HpPRUFqvuZ9tqY4SiftfxfzlnYoW; mid=ZkO0PgAEAAGxvPpL3uLZrDFIqtRD; dpr=1; shbid="8954\0542540082\0541749654799:01f702fa68ecec6502f25a8af31128063ffec84086cca84e3bfcbd80aee95d741f8eb7bc"; shbts="1718118799\0542540082\0541749654799:01f79da9bc72ad9b2fc52f6ea5012a9a83990a2d7c7bdb98c4d710b33ff30453836694f6"; sessionid=2540082%3A7ZJkKnFSEvhVSK%3A9%3AAYctw1yit46rlxJYr3hOr_J1HmKVeGA6GTtui8239vw; fbsr_124024574287414=zCng5MjPugAEiCraWa8xATlRv3Uzpq4JqwGQaW2P5rY.eyJ1c2VyX2lkIjoiNTUzNTA5OTg4IiwiY29kZSI6IkFRRFFJZ0kwYkZqYnQxZkdyZ1JlcHBzSTA1S2F6UXd5NlkwaUVDbzBIY2dJb3BrS09uYjNZN0czX1JLT09rRVJsck9uYzhLZm9CTkJmS2cyZDJqWDZBR2tGNnVlYXRHUS1mZVZNcnRRWHVWWFhmaDZNc0l5ZkxBVFB6SXBqZjV0TzBYMFBGQ180SGUzRFBGYU9peTFBVTJLNjBsWUtHSVFHYWlyOExtbElzS0kzNWNBVnZuZDg3Q2Y5ODVKcXpSRGFBSkROVFdzNThDd0wtbWJPaVdoR1dIemhlaXFfaTRBeXhDM1FZaEV1VE9Yc0JtMmlhSzNOcUxGdGRWMXhOTGxQOW54WkIzRDFydXNhdW9fU3h1VU9VTVlhREtTWFNaMXMxOW5ESVpFcnBmcFJNZVBUcjlha1YyeEF4RjJYSzdWVTJ3Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCT3c1V1V5cWF0VVJ4SlpCaUJnS1B5cm5IVUFSeFpBenRXQmFjVUQyZVFOTWxtOWl3YTBwTFpBN291QzNLbnJiV3lzeFNVSGdjOGptMjRJbFZSU09sVXNKQ3RzT3dJM2Y2Y1dIQmZzZ0Fpdzg1bjVkYWs2bDFDNjBhTjhSTTBBYTZyWGtRVlZ2T1BZWGMyU3I0QlpBeHN4SzdpZHU4elJiVldlWkJDdFFMWHQ3Zmt1WXE1UW5kUiIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNzE4MTE4ODAyfQ; wd=909x968; rur="RVA\0542540082\0541749654840:01f70a65a7981c4db976af0ba440358954f667b72a4f5fc9311ceb1fdd395ce4776d0493"',
                }
                url = f"https://www.instagram.com/graphql/query/?query_hash=c9100bf9110dd6361671f113dd02e7d6&variables={{%22user_id%22:{user_id},%22include_reel%22:%22true%22}}"
                response = requests.get(url, headers=headers)
                print("Instagram API Response:", response.json())  # Instagram'dan gelen cevabı yazdır
                # Gelecek cevaba göre işleme yapabilirsiniz (örneğin veriyi AllLabels'a ekleme)
                return JsonResponse({'message': 'Data fetched from Instagram API'}, status=status.HTTP_200_OK)
            except Exception as e:
                print("Error fetching data from Instagram:", str(e))
                return JsonResponse({'message': 'Error fetching data from Instagram'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({'message': 'Label is required'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def save_shapes_view(request, project_title):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            shapes = data.get('shapes', [])
            user_email = data.get('userEmail', '')
            
            #-------------------------------------------------------
            #DEBUG PURPOSE
            #print(data)
            #print("-"*20)
            #print(shapes)
            #print("-"*20)
            #print(user_email)
            #print("-"*20)
            #-------------------------------------------------------

            # Find user by email then id
            user = UserAccount.objects.get(email=user_email)
            user_id = user.id

            # Find project by title and owner (user) then id
            project = UserProjects.objects.get(title=project_title, owner=user)
            project_id = project.id

            #DEBUG PURPOSE
            #print(user_id)
            #print("-"*20)
            #print(project_id)

            # Delete existing shapes for this project and user
            UserProjectShapes.objects.filter(project_id=project_id, user_id=user_id).delete()

            # Save new shapes to the database
            for shape in shapes:
                try:
                    UserProjectShapes.objects.create(
                        project_id=project_id,
                        user_id=user_id,
                        shape_data=shape
                    )
                except Exception as e:
                    print(f"Error saving shape: {shape}")
                    print(f"Exception: {e}")
                    return JsonResponse({'error': f'Error saving shape: {shape}. Exception: {e}'}, status=400)

            return JsonResponse({'message': 'Shapes saved successfully'}, status=200)

        except UserAccount.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        except UserProjects.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


from rest_framework.decorators import api_view

@api_view(['GET'])
def load_shapes(request, project_title):
    if request.method == 'GET':
        try:
            user_email = request.GET.get('userEmail', '')
            user = get_object_or_404(UserAccount, email=user_email)

            project = get_object_or_404(UserProjects, title=project_title, owner=user)
            shapes = UserProjectShapes.objects.filter(project=project, user=user)

            if shapes.exists():
                shapes_data = [shape.shape_data for shape in shapes]
                return JsonResponse(shapes_data, safe=False)
            else:
                return JsonResponse([], safe=False)
        
        except UserAccount.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        except UserProjects.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    else:
        return JsonResponse({'error': 'Only GET method is allowed'}, status=405)






def get_csrf_token_view(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})




@method_decorator(csrf_exempt, name='dispatch')
class FileUploadView(View):
    def post(self, request):
        #print("Request POST data:", request.POST)
        #print("Request FILES data:", request.FILES)
        
        # Check if 'file' and 'projectTitle' are present in request
        if 'file' not in request.FILES or 'projectTitle' not in request.POST:
            return JsonResponse({'error': 'File or project title missing'}, status=400)
        
        uploaded_file = request.FILES['file']
        project_title = request.POST.get('projectTitle', '')
        user_email = request.POST.get('userEmail', '')
        user = UserAccount.objects.get(email=user_email)

        # Ensure the project title is not empty
        if not project_title.strip():
            return JsonResponse({'error': 'Project title cannot be empty'}, status=400)
        
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Read CSV and process data
        if uploaded_file.name.endswith('.csv'):
            with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                headers = csv_reader.fieldnames

                required_columns = ['Id', 'Label', 'Modularity_Class', 'Pageranks', 'Filter', 'X', 'Y', 'Size', 'Color', 'Level1']
                if all(col in headers for col in required_columns):
                    # Save project title to UserProjects table
                    project_obj, created = UserProjects.objects.get_or_create(title=project_title, owner=user)

                    # Prepare data for bulk_create
                    user_project_data_list = []
                    for row in csv_reader:
                        user_project_data = UserProjectsData(
                            project_id=project_obj,
                            Data_Id=row['Id'],
                            Label=row['Label'],
                            Modularity_Class=row['Modularity_Class'],
                            Pageranks=row['Pageranks'],
                            Custom_Filter=row['Filter'],
                            X=row['X'],
                            Y=row['Y'],
                            Size=row['Size'],
                            Color=row['Color'],
                            Level1=row['Level1']  
                        )
                        user_project_data_list.append(user_project_data)

                    # Bulk create UserProjectsData entries
                    with transaction.atomic():
                        UserProjectsData.objects.bulk_create(user_project_data_list)

                    return JsonResponse({'message': 'Dosya başarıyla yüklendi ve işlendi'}, status=200)
                else:
                    return JsonResponse({'error': 'CSV dosyası belirtilen sütunları içermiyor'}, status=400)

        return JsonResponse({'message': 'Dosya başarıyla yüklendi'}, status=200)





@api_view(['GET'])
def user_projects(request):
    user = request.user

    if user.is_authenticated:  # is user auth check ???
        user_email = user
        projects = UserProjects.objects.filter(owner=user_email)
        project_titles = [project.title for project in projects]
        #print("calisti")
        return Response({'projects': project_titles})
    else:
        return Response({'error': 'User is not authenticated.'}, status=401)





#@api_view(['GET'])
@csrf_exempt
def user_project_data(request, project_title):
    try:
        # Proje başlığına göre ilgili proje nesnesini al
        project = get_object_or_404(UserProjects, title=project_title)
        # Proje nesnesinin id'sine göre ve Filter değeri "true" olan verileri filtrele
        project_data = UserProjectsData.objects.filter(
            project_id=project.id, Custom_Filter="true"
        ).values(
            'Label', 'X', 'Y', 'Size', 'Color', 'Level1'
        )
        return JsonResponse(list(project_data), status=200, safe=False)
    except UserProjects.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
    except UserProjectsData.DoesNotExist:
        return JsonResponse({'error': 'Project data not found'}, status=404)




@csrf_exempt
def user_project_delete(request, project_title):
    #print('DEBUG : user_project_delete(), OK ')
    project = get_object_or_404(UserProjects, title=project_title)
    project.delete()
    return JsonResponse({'message': 'Project and associated data deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
   
   


