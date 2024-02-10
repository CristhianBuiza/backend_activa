import face_recognition as fr
import numpy as np
from profiles.models import Profile


def is_ajax(request):
  return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def get_encoded_faces(username):
    """
    This function loads all user 
    profile images and encodes their faces
    """
    # Retrieve all user profiles from the database
    try:
        user_profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        print(f"No se encontró el perfil para el usuario: {username}")
        return None
    if not user_profile.photo:
        print(f"No hay foto asociada al perfil de {username}")
        return None


    # Create a dictionary to hold the encoded face for each user
    try:
        # Carga la imagen del perfil y codifica la cara
        face_image = fr.load_image_file(user_profile.photo.path)
        face_encodings = fr.face_encodings(face_image)

        if face_encodings:
            # Devuelve la primera codificación facial encontrada
            return face_encodings[0]
        else:
            print(f"No se encontró ninguna cara en la imagen de {username}")
            return None
    except Exception as e:
        print(f"Error al cargar o codificar la foto de {username}: {e}")
        return None

def classify_face(img_path, username):
    """
    Compara la imagen proporcionada con la imagen de perfil del usuario especificado,
    y retorna el nombre del usuario si las caras coinciden, o "Unknown" si no.
    """
    user_face_encoding = get_encoded_faces(username)  # Obtiene la codificación de la cara del usuario especificado

    if user_face_encoding is None:
        print(f"No se encontró la codificación de la cara para el usuario {username}")
        return "Unknown"

    # Carga la imagen proporcionada y encuentra codificaciones faciales
    img_to_classify = fr.load_image_file(img_path)
    unknown_face_encodings = fr.face_encodings(img_to_classify)

    for unknown_face_encoding in unknown_face_encodings:
        results = fr.compare_faces([user_face_encoding], unknown_face_encoding)
        if True in results:
            return username  # La cara coincide con la del usuario

    return "Unknown"
