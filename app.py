"""Página web mínima con patrón MVC y un contador que incrementa al hacer click.

Mapeo MVC en Flask (Flask no impone MVC estricto, aquí se organiza así):

- Modelo:   la clase ``Contador`` (estado + lógica de negocio).
- Vista:    las plantillas Jinja2 (``templates/``) y el CSS (``static/css/``).
- Controlador: las rutas Flask (``index`` y ``increment``).

El estado vive en memoria del proceso: se reinicia al reiniciar el servidor
y no se comparte entre varios workers. Es suficiente para un ejemplo didáctico.
"""

from flask import Flask, redirect, render_template, url_for


class Contador:
    """Modelo: encapsula el valor del contador y su lógica de incremento."""

    def __init__(self, valor_inicial: int = 0) -> None:
        self.valor = valor_inicial

    def incrementar(self, paso: int = 1) -> int:
        """Incrementa el contador y devuelve el nuevo valor."""
        self.valor += paso
        return self.valor

    def reiniciar(self) -> int:
        """Pone el contador a cero y devuelve el valor resultante."""
        self.valor = 0
        return self.valor


app = Flask(__name__)

# Instancia única del modelo (estado global del proceso).
contador = Contador()


@app.route("/", methods=["GET"])
def index():
    """Controlador: muestra la vista con el valor actual del contador."""
    return render_template("index.html", valor=contador.valor)


@app.route("/increment", methods=["POST"])
def increment():
    """Controlador: incrementa el modelo y redirige (patrón Post/Redirect/Get)."""
    contador.incrementar()
    return redirect(url_for("index"))


@app.route("/reset", methods=["POST"])
def reset():
    """Controlador: reinicia el modelo y redirige (patrón Post/Redirect/Get)."""
    contador.reiniciar()
    return redirect(url_for("index"))


if __name__ == "__main__":
    # debug=True solo para desarrollo local; no usar en producción.
    app.run(debug=True)
