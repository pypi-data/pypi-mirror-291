from .app import app
from .clean import clean
from .config import config
from .push import push
from .version import app as app_version
from .venv import app as app_venv


__all__ = [
    'app',
]


app.add_typer(app_version, name='version')
app.add_typer(app_venv, name='venv')
