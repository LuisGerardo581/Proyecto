# modelos/usuario.py
class Persona:
    def __init__(self, nombre, correo):
        self._nombre = nombre
        self._correo = correo

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    def resumen(self):
        return f"Persona: {self.nombre} ({self.correo})"


class Usuario(Persona):
    def __init__(self, nombre, correo, contrasena):
        super().__init__(nombre, correo)
        self._contrasena = contrasena
        self._amigos = []
        self._publicaciones = []

    @property
    def contrasena(self):
        return self._contrasena

    @property
    def amigos(self):
        return self._amigos

    @property
    def publicaciones(self):
        return self._publicaciones

    def resumen(self):
        return f"Usuario: {self.nombre}, tiene {len(self.amigos)} amigos y {len(self.publicaciones)} publicaciones"