from rest_framework.response import Response
from rest_framework import status 
from typing import Any, Optional, Dict
def NormalizeResponse(data:Optional[Any]=None, status:int=status.HTTP_200_OK, message:str=""):
    if not data:
        return Response({
            "status": status,
            "message": message
        }, status=status)
    return Response({
        "status": status,
        "data": data,
        "message": message
    }, status=status)