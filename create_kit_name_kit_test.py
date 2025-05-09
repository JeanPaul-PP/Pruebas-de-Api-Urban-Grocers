import requests
import configuration
import data
import sender_stand_request


# Función para obtener token válido
def get_new_user_token():
    user_body = data.user_body
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 201
    return response.json()["authToken"]


# Función para crear el cuerpo del kit con nombre
def get_kit_body(name):
    return {
        "name": name
    }


# Función para verificar respuesta positiva (status code 201)
def positive_assert(kit_body):
    token = get_new_user_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(
        url=configuration.URL_SERVICE + configuration.KITS_PATH,
        json=kit_body,
        headers=headers
    )
    print("Código de estado:", response.status_code)
    print("Respuesta:", response.json())
    assert response.status_code == 201
    assert response.json()["name"] == kit_body["name"]


# Función para verificar respuesta negativa (status code 400)
def negative_assert_code_400(kit_body):
    token = get_new_user_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(
        url=configuration.URL_SERVICE + configuration.KITS_PATH,
        json=kit_body,
        headers=headers
    )
    print("Código de estado:", response.status_code)
    print("Respuesta:", response.json())
    assert response.status_code == 400


# ---------- TESTS POSITIVOS ----------

def test_create_kit_name_1_character():
    positive_assert(get_kit_body("A"))


def test_create_kit_name_511_characters():
    name = "A" * 511
    positive_assert(get_kit_body(name))


def test_create_kit_name_with_spaces():
    positive_assert(get_kit_body("Kit de prueba"))


def test_create_kit_name_with_numbers():
    positive_assert(get_kit_body("Kit123"))


def test_create_kit_name_with_special_characters():
    positive_assert(get_kit_body("Kit@#$_"))


# ---------- TESTS NEGATIVOS ----------

def test_create_kit_name_empty():
    negative_assert_code_400(get_kit_body(""))


def test_create_kit_name_more_than_511_characters():
    name = "A" * 512
    negative_assert_code_400(get_kit_body(name))


def test_create_kit_name_missing_parameter():
    token = get_new_user_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    # Kit sin parámetro "name"
    kit_body = {}
    response = requests.post(
        url=configuration.URL_SERVICE + configuration.KITS_PATH,
        json=kit_body,
        headers=headers
    )
    print("Código de estado:", response.status_code)
    print("Respuesta:", response.json())
    assert response.status_code == 400