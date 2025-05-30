# modelos/publicacion.py
from datetime import datetime

class Contenido:
    def __init__(self, contenido):
        self._contenido = contenido

    @property
    def contenido(self):
        return self._contenido

    def resumen(self):
        return f"Contenido: {self.contenido[:30]}..."


class Publicacion(Contenido):
    def __init__(self, contenido, autor):
        super().__init__(contenido)
        self._autor = autor
        self._fecha = datetime.now()
        self._likes = []
        self._comentarios = []

    @property
    def autor(self):
        return self._autor

    @property
    def fecha(self):
        return self._fecha

    @property
    def likes(self):
        return self._likes

    @property
    def comentarios(self):
        return self._comentarios

    def resumen(self):
        return f"{self.autor.nombre} publicó: {self.contenido[:40]}... ({len(self.likes)} likes, {len(self.comentarios)} comentarios)"