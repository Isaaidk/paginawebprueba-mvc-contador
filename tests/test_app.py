"""Pruebas del modelo Contador y de las rutas (Controlador) de la app."""

import pytest

from app import Contador, app, contador


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    contador.reiniciar()
    with app.test_client() as cliente:
        yield cliente
    contador.reiniciar()


def test_modelo_arranca_en_cero():
    assert Contador().valor == 0


def test_modelo_incrementar():
    c = Contador()
    assert c.incrementar() == 1
    assert c.incrementar() == 2
    assert c.valor == 2


def test_modelo_incrementar_con_paso():
    c = Contador(10)
    assert c.incrementar(5) == 15


def test_modelo_reiniciar():
    c = Contador(7)
    assert c.reiniciar() == 0
    assert c.valor == 0


def test_index_muestra_cero(client):
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert b'id="valor">0<' in respuesta.data


def test_increment_suma_uno(client):
    respuesta = client.post("/increment", follow_redirects=True)
    assert respuesta.status_code == 200
    assert b'id="valor">1<' in respuesta.data


def test_increment_acumula(client):
    for esperado in (1, 2, 3):
        respuesta = client.post("/increment", follow_redirects=True)
        assert f'id="valor">{esperado}<'.encode() in respuesta.data


def test_increment_redirige(client):
    respuesta = client.post("/increment")
    assert respuesta.status_code == 302
    assert respuesta.headers["Location"].endswith("/")


def test_reset_vuelve_a_cero(client):
    client.post("/increment")
    client.post("/increment")
    respuesta = client.post("/reset", follow_redirects=True)
    assert b'id="valor">0<' in respuesta.data


def test_css_disponible(client):
    respuesta = client.get("/static/css/styles.css")
    assert respuesta.status_code == 200
    assert b"button:hover" in respuesta.data
