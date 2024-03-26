from typing import Any, Optional
from rest_framework.response import Response
from rest_framework import status
def NormalizeResponse(data:Optional[Any]=None, status:int=status.HTTP_200_OK, message:str=""):
    if not data:
        return Response({
            "status": status,
            "message": message
        }, status=status)
    return Response({
        "status": status,
        "message": message,
        "data": data
    }, status=status)