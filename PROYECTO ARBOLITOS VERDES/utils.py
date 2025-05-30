import json
from modelos.usuario import Usuario

def cargar_usuarios(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
            usuarios = [Usuario(u['nombre'], u['correo'], u['contrasena']) for u in data]
            # Reconstruir relaciones de amistad por correo
            correo_usuario = {u.correo: u for u in usuarios}
            for u, u_data in zip(usuarios, data):
                u.amigos.extend([correo_usuario[c] for c in u_data.get('amigos', []) if c in correo_usuario])
            return usuarios
    except FileNotFoundError:
        return []

def guardar_usuarios(ruta_archivo, usuarios):
    data = []
    for u in usuarios:
        data.append({
            'nombre': u.nombre,
            'correo': u.correo,
            'contrasena': u.contrasena,
            'amigos': [amigo.correo for amigo in u.amigos]
        })
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)