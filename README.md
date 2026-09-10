# paginawebprueba-mvc-contador

Página web mínima en Python con patrón **MVC** y un contador que incrementa al hacer click.

## Stack

- Python 3.11+
- Flask (micro-framework)
- Jinja2 (incluido con Flask, actúa como Vista)
- HTML5 + CSS3 mínimos (sin frameworks)
- Entorno virtual con `venv`

## Estructura

```
paginawebprueba-mvc-contador/
├── app.py                  # Modelo + Controlador
├── requirements.txt        # Dependencias (versión fijada)
├── .gitignore
├── README.md
├── static/
│   └── css/
│       └── styles.css      # Vista (estilos)
├── templates/
│   ├── base.html           # Vista (esqueleto)
│   └── index.html          # Vista (página del contador)
└── tests/
    └── test_app.py         # Pruebas del modelo y las rutas
```

## Aclaración sobre MVC en Flask

Flask **no impone MVC estricto**; es un micro-framework que solo enruta peticiones a funciones.
En este proyecto el patrón MVC se mapea de forma explícita:

| Capa | Dónde vive | Responsabilidad |
|------|------------|-----------------|
| **Modelo** | clase `Contador` en `app.py` | Guarda el valor y expone `incrementar()` / `reiniciar()` |
| **Vista** | `templates/*.html` + `static/css/styles.css` | Presenta el valor y el formulario |
| **Controlador** | rutas Flask en `app.py` (`/`, `/increment`, `/reset`) | Lee el modelo y devuelve la vista |

El formulario usa **POST + redirect** (patrón Post/Redirect/Get) para evitar reenvíos al recargar.

## Instalación

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

## Uso

```bash
python app.py
```

Abre <http://127.0.0.1:5000>:

- El contador arranca en **0**.
- Cada click en **Incrementar** suma 1 (1, 2, 3...).
- **Reiniciar** vuelve a 0.
- Recargar la página mantiene el valor mientras el proceso siga vivo.
- Dos pestañas ven el mismo valor (estado global del proceso).

## Pruebas

```bash
pip install pytest
pytest -q
```

## Riesgos y limitaciones

- **Estado en memoria**: se reinicia al reiniciar el servidor y no funciona con varios workers.
  Para persistencia habría que añadir sesión Flask, SQLite o Redis.
- **Concurrencia**: sin bloqueo, dos peticiones simultáneas podrían perder un incremento.
  Irrelevante en local, relevante en producción.
- **`debug=True`**: solo para desarrollo; el servidor de desarrollo no debe exponerse en producción.
- **CSRF**: el formulario POST no lleva token; aceptable en local, a considerar si se amplía.
- **Alcance**: proyecto deliberadamente mínimo; BD, autenticación o más tests serían iteraciones posteriores.
