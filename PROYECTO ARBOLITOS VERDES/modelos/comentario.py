# modelos/comentario.py
from datetime import datetime
from .publicacion import Contenido

class Comentario(Contenido):
    def __init__(self, contenido, autor):
        super().__init__(contenido)
        self._autor = autor
        self._fecha = datetime.now()

    @property
    def autor(self):
        return self._autor

    @property
    def fecha(self):
        return self._fecha

    def resumen(self):
        return f"{self.autor.nombre} comentó: {self.contenido[:40]}..."