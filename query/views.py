# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

from .models import Script
from .serializers import ScriptSerializer


# @csrf_exempt
# @login_required
@api_view(['post'])
# @permission_classes([IsAuthenticated])
def createScript(request):
    user = request.user
    script_name = request.data.get("script_name")
    query_text = request.data.get("query_text")

    script = Script.objects.create(script_name=script_name, query_text=query_text, reg_user=user.username)

    return JsonResponse({'script_id': script.id, 'script_name': script.script_name}, status=201)


@api_view(['get'])
def getScript(request, pk):
    try:
        # script = Script.objects.get(pk=pk, public_yn=True)  # pk와 public_yn=True로 Script 조회
        script = Script.objects.get(pk=pk)
    except Script.DoesNotExist:
        return JsonResponse({'message': 'Script does not exist.'}, status=404)

    serializer = ScriptSerializer(script)
    return JsonResponse(serializer.data)


@api_view(['get'])
def getScriptByName(request, script_name):
    try:
        # script = Script.objects.get(script_name=script_name, public_yn=True)  # script_name과 public_yn=True로 Script 조회
        script = Script.objects.get(script_name=script_name)
    except Script.DoesNotExist:
        return JsonResponse({'message': 'Script does not exist.'}, status=404)

    serializer = ScriptSerializer(script)
    return JsonResponse(serializer.data)


# Script 수정 API
@api_view(['post'])
def updateScript(request, script_name):
    try:
        # script = Script.objects.get(script_name=script_name, public_yn=True)  # pk와 public_yn=True로 Script 조회
        script = Script.objects.get(script_name=script_name)
    except Script.DoesNotExist:
        return JsonResponse({'message': 'Script does not exist.'}, status=404)

    if script.reg_user != request.user.username:  # Script 생성자와 요청한 사용자가 다른 경우
        return JsonResponse({'message': 'You are not authorized to edit this script.'}, status=403)

    serializer = ScriptSerializer(script, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)


# Script 삭제 API
@api_view(['POST'])
def deleteScript(request, script_name):
    try:
        script = Script.objects.get(script_name=script_name)
    except Script.DoesNotExist:
        return JsonResponse({'message': 'Script does not exist.'}, status=404)

    if script.reg_user != request.user.username:  # Script 생성자와 요청한 사용자가 다른 경우
        return JsonResponse({'message': 'You are not authorized to delete this script.'}, status=403)

    # soft delete를 위해 use_yn 필드를 False로 업데이트
    script.use_yn = False
    script.save()

    return JsonResponse({'message': 'Script has been deleted.'})
