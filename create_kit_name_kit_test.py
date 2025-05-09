import requests
import configuration
import data
import sender_stand_request

def new_kit (kit_data): # Crear un nuevo kit
    response = requests.post(configuration.URL_SERVICE + configuration.KITS_PATH, json=kit_data, headers=data.headers_token)
    print("Código de estado:", response.status_code)
    print("Respuesta:", response.json())

def get_user_body (first_name): # Modificar la variable "first_name" en el cuerpo de la solicitud en cada prueba
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body

def positive_assert (first_name): # Se define la funcion positiva que usaremos en las siguientes pruebas
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

def test_first_name_511_character (): # 511 caracteres en el campo first_name
    positive_assert("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")

def test_first_name_1_character (): # 1 caraster en el campo first_name
    positive_assert("a")

def test_first_name_0_character (): # Campo first_name vacio
    positive_assert("")

def test_first_name_1_character (): # 512 caracteres en el campo first_name
    positive_assert("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabca")

def test_first_name_0_character (): # Caracteres especiales en el campo first_name
    positive_assert("№%@,")

def test_first_name_0_character (): # Espacios en el campo first_name
    positive_assert("A aa")

def test_first_name_0_character (): # Numeros en el campo first_name
    positive_assert("123")

def negative_assert_no_firstname(user_body): # Definicion de prueba negativa
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400

def test_create_user_no_first_name_get_error_response(): # El parametro first_name no existe en la solicitud
    user_body = data.user_body.copy()
    user_body.pop("firstName")

    negative_assert_no_firstname(user_body)
    assert response.status_code == 400

def test_create_user_number_type_first_name_get_error_response(): # El parametro first_name contiene nuemeros
    user_body = get_user_body(123)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400