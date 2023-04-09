# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

from .models import Script, ScriptPermission
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


@api_view(['POST'])
def authorizeScript(request):
    try:
        script_id = request.data.get("script_id")
        script = Script.objects.get(id=script_id, use_yn=True)
    except Script.DoesNotExist:
        return JsonResponse({'message': 'Script does not exist.'}, status=404)

    user_ids = request.data.get('user_ids', [])
    print(user_ids)
    if not isinstance(user_ids, list):
        return JsonResponse({'message': 'user_ids must be a list.'}, status=400)

    # 권한 부여 대상 사용자 리스트를 만듭니다.
    users = []
    for user_id in user_ids:
        try:
            user = User.objects.get(username=user_id) # 여기서 바꿔주면 됨
            users.append(user)
        except User.DoesNotExist:
            pass

    # 대상 사용자에게 권한을 부여합니다.
    created_count = 0
    for user in users:
        permission, created = ScriptPermission.objects.get_or_create(script=script, user=user)
        if created:
            created_count += 1

    return JsonResponse({'message': f'{created_count} permission(s) created.'})


@api_view(['POST'])
def removeScriptPermission(request):
    try:
        script_id = request.data.get("script_id")
        script = Script.objects.get(id=script_id, use_yn=True)
    except Script.DoesNotExist:
        return JsonResponse({'message': 'Script does not exist.'}, status=404)

    user_name = request.data.get('user_name', [])
    if not isinstance(user_name, list):
        return JsonResponse({'message': 'user_ids must be a list.'}, status=400)

    # 권한 삭제 대상 사용자 리스트를 만듭니다.
    users = []
    for user_id in user_name:
        try:
            user = User.objects.get(username=user_id)
            users.append(user)
        except User.DoesNotExist:
            pass

    # 대상 사용자의 권한을 삭제합니다.
    deleted_count = 0
    for user in users:
        try:
            permission = ScriptPermission.objects.get(script=script, user=user)
            permission.delete()
            deleted_count += 1
        except ScriptPermission.DoesNotExist:
            pass

    return JsonResponse({'message': f'{deleted_count} permission(s) deleted.'})
