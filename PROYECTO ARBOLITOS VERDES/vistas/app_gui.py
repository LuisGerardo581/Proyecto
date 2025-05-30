from utils import cargar_usuarios, guardar_usuarios
import tkinter as tk
from tkinter import ttk, messagebox
from modelos.usuario import Usuario
from modelos.publicacion import Publicacion
from modelos.comentario import Comentario

class RedSocialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Red Social POO")
        self.root.geometry("800x600")

        self.ruta_usuarios = "usuarios.json"
        self.usuarios = cargar_usuarios(self.ruta_usuarios)

        pub1 = Publicacion("¡Hola a todos! Esta es mi primera publicación", self.usuarios[1])
        pub2 = Publicacion("Aprendiendo Python con POO", self.usuarios[2])
        self.usuarios[1].publicaciones.append(pub1)
        self.usuarios[2].publicaciones.append(pub2)

        self.usuario_actual = None
        self.mostrar_login()

    def mostrar_login(self):
        self.limpiar_pantalla()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)
        ttk.Label(frame, text="Inicio de Sesión", font=('Helvetica', 16)).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(frame, text="Correo:").grid(row=1, column=0, sticky=tk.W)
        self.correo_entry = ttk.Entry(frame, width=30)
        self.correo_entry.grid(row=1, column=1, pady=5)
        ttk.Label(frame, text="Contraseña:").grid(row=2, column=0, sticky=tk.W)
        self.contrasena_entry = ttk.Entry(frame, width=30, show="*")
        self.contrasena_entry.grid(row=2, column=1, pady=5)
        ttk.Button(frame, text="Iniciar Sesión", command=self.iniciar_sesion).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Registrarse", command=self.mostrar_registro).grid(row=4, column=0, columnspan=2)

    def mostrar_registro(self):
        self.limpiar_pantalla()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)
        ttk.Label(frame, text="Registro de Usuario", font=('Helvetica', 16)).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W)
        self.reg_nombre_entry = ttk.Entry(frame, width=30)
        self.reg_nombre_entry.grid(row=1, column=1, pady=5)
        ttk.Label(frame, text="Correo:").grid(row=2, column=0, sticky=tk.W)
        self.reg_correo_entry = ttk.Entry(frame, width=30)
        self.reg_correo_entry.grid(row=2, column=1, pady=5)
        ttk.Label(frame, text="Contraseña:").grid(row=3, column=0, sticky=tk.W)
        self.reg_contrasena_entry = ttk.Entry(frame, width=30, show="*")
        self.reg_contrasena_entry.grid(row=3, column=1, pady=5)
        ttk.Button(frame, text="Registrar", command=self.registrar_usuario).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Volver", command=self.mostrar_login).grid(row=5, column=0, columnspan=2)

    def mostrar_muro(self):
        self.limpiar_pantalla()
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        left_frame = ttk.Frame(main_frame, width=200, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        ttk.Label(left_frame, text=f"Perfil de {self.usuario_actual.nombre}", font=('Helvetica', 12, 'bold')).pack(pady=5)
        ttk.Label(left_frame, text=f"Correo: {self.usuario_actual.correo}").pack(anchor=tk.W)
        ttk.Label(left_frame, text=f"Amigos: {len(self.usuario_actual.amigos)}").pack(anchor=tk.W)
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(left_frame, text="Amigos:").pack(anchor=tk.W)
        for amigo in self.usuario_actual.amigos[:5]:
            ttk.Label(left_frame, text=f"- {amigo.nombre}").pack(anchor=tk.W)
        ttk.Button(left_frame, text="Buscar Amigos", command=self.mostrar_buscar_amigos).pack(pady=10)
        ttk.Button(left_frame, text="Cerrar Sesión", command=self.mostrar_login).pack(pady=10)
        ttk.Button(left_frame, text="Ver Resumen", command=self.mostrar_resumen).pack(pady=10)
        right_frame = ttk.Frame(main_frame, padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        ttk.Label(right_frame, text="Nueva Publicación:").pack(anchor=tk.W)
        self.nueva_publicacion_entry = tk.Text(right_frame, height=3, width=50)
        self.nueva_publicacion_entry.pack(pady=5)
        ttk.Button(right_frame, text="Publicar", command=self.crear_publicacion).pack(anchor=tk.E, pady=5)
        ttk.Label(right_frame, text="Publicaciones", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W, pady=10)
        self.publicaciones_frame = ttk.Frame(right_frame)
        self.publicaciones_frame.pack(fill=tk.BOTH, expand=True)
        self.actualizar_publicaciones()

    def actualizar_publicaciones(self):
        for widget in self.publicaciones_frame.winfo_children():
            widget.destroy()
        todas_publicaciones = self.usuario_actual.publicaciones[:]
        for amigo in self.usuario_actual.amigos:
            todas_publicaciones.extend(amigo.publicaciones)
        todas_publicaciones.sort(key=lambda x: x.fecha, reverse=True)
        for pub in todas_publicaciones:
            pub_frame = ttk.Frame(self.publicaciones_frame, borderwidth=1, relief="solid", padding="10")
            pub_frame.pack(fill=tk.X, pady=5)
            ttk.Label(pub_frame, text=f"{pub.autor.nombre} - {pub.fecha.strftime('%d/%m/%Y %H:%M')}", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
            ttk.Label(pub_frame, text=pub.contenido, wraplength=400).pack(anchor=tk.W, pady=5)
            stats_frame = ttk.Frame(pub_frame)
            stats_frame.pack(anchor=tk.W)
            ttk.Label(stats_frame, text=f"❤️ {len(pub.likes)}").pack(side=tk.LEFT, padx=5)
            ttk.Label(stats_frame, text=f"💬 {len(pub.comentarios)}").pack(side=tk.LEFT, padx=5)
            btn_frame = ttk.Frame(pub_frame)
            btn_frame.pack(anchor=tk.E, pady=5)
            ttk.Button(btn_frame, text="Like", command=lambda p=pub: self.dar_like(p)).pack(side=tk.LEFT, padx=2)
            ttk.Button(btn_frame, text="Comentar", command=lambda p=pub: self.mostrar_comentarios(p)).pack(side=tk.LEFT, padx=2)

    def mostrar_buscar_amigos(self):
        self.limpiar_pantalla()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)
        ttk.Label(frame, text="Buscar Amigos", font=('Helvetica', 16)).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(frame, text="Buscar por nombre:").grid(row=1, column=0, sticky=tk.W)
        self.buscar_entry = ttk.Entry(frame, width=30)
        self.buscar_entry.grid(row=1, column=1, pady=5)
        ttk.Button(frame, text="Buscar", command=self.buscar_amigos).grid(row=2, column=0, columnspan=2, pady=10)
        self.resultados_frame = ttk.Frame(frame)
        self.resultados_frame.grid(row=3, column=0, columnspan=2)
        ttk.Button(frame, text="Volver al Muro", command=self.mostrar_muro).grid(row=4, column=0, columnspan=2, pady=10)

    def mostrar_comentarios(self, publicacion):
        self.limpiar_pantalla()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)
        ttk.Label(frame, text="Comentarios", font=('Helvetica', 16)).pack()
        ttk.Label(frame, text=f"{publicacion.autor.nombre}: {publicacion.contenido}").pack(pady=10)
        comentarios_frame = ttk.Frame(frame)
        comentarios_frame.pack(fill=tk.X, pady=10)
        for comentario in publicacion.comentarios:
            ttk.Label(comentarios_frame, text=f"{comentario.autor.nombre}: {comentario.contenido}").pack(anchor=tk.W)
        ttk.Label(frame, text="Añadir comentario:").pack(anchor=tk.W)
        self.nuevo_comentario_entry = ttk.Entry(frame, width=50)
        self.nuevo_comentario_entry.pack(pady=5)
        ttk.Button(frame, text="Publicar Comentario", command=lambda: self.agregar_comentario(publicacion)).pack(pady=5)
        ttk.Button(frame, text="Volver", command=self.mostrar_muro).pack(pady=10)

    def iniciar_sesion(self):
        correo = self.correo_entry.get()
        contrasena = self.contrasena_entry.get()
        for usuario in self.usuarios:
            if usuario.correo == correo and usuario.contrasena == contrasena:
                self.usuario_actual = usuario
                self.mostrar_muro()
                return
        messagebox.showerror("Error", "Correo o contraseña incorrectos")

    def registrar_usuario(self):
        nombre = self.reg_nombre_entry.get()
        correo = self.reg_correo_entry.get()
        contrasena = self.reg_contrasena_entry.get()
        if not nombre or not correo or not contrasena:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        if any(u.correo == correo for u in self.usuarios):
            messagebox.showerror("Error", "El correo ya está registrado")
            return
        nuevo_usuario = Usuario(nombre, correo, contrasena)
        self.usuarios.append(nuevo_usuario)
        self.usuario_actual = nuevo_usuario
        messagebox.showinfo("Éxito", "Registro completado", guardar_usuarios(self.ruta_usuarios, self.usuarios))
        self.mostrar_muro()

    def crear_publicacion(self):
        contenido = self.nueva_publicacion_entry.get("1.0", tk.END).strip()
        if contenido:
            nueva_publicacion = Publicacion(contenido, self.usuario_actual)
            self.usuario_actual.publicaciones.append(nueva_publicacion)
            self.nueva_publicacion_entry.delete("1.0", tk.END)
            self.actualizar_publicaciones()

    def dar_like(self, publicacion):
        if self.usuario_actual not in publicacion.likes:
            publicacion.likes.append(self.usuario_actual)
            self.actualizar_publicaciones()

    def agregar_comentario(self, publicacion):
        contenido = self.nuevo_comentario_entry.get().strip()
        if contenido:
            nuevo_comentario = Comentario(contenido, self.usuario_actual)
            publicacion.comentarios.append(nuevo_comentario)
            self.mostrar_comentarios(publicacion)

    def buscar_amigos(self):
        busqueda = self.buscar_entry.get().lower()
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()
        resultados = [u for u in self.usuarios if busqueda in u.nombre.lower() and u != self.usuario_actual and u not in self.usuario_actual.amigos]
        if not resultados:
            ttk.Label(self.resultados_frame, text="No se encontraron resultados").pack()
            return
        for usuario in resultados:
            user_frame = ttk.Frame(self.resultados_frame)
            user_frame.pack(fill=tk.X, pady=5)
            ttk.Label(user_frame, text=usuario.nombre).pack(side=tk.LEFT)
            ttk.Button(user_frame, text="Agregar", command=lambda u=usuario: self.agregar_amigo(u)).pack(side=tk.RIGHT)

    def agregar_amigo(self, amigo):
        if amigo not in self.usuario_actual.amigos:
            self.usuario_actual.amigos.append(amigo)
            amigo.amigos.append(self.usuario_actual)
            messagebox.showinfo("Éxito", guardar_usuarios(self.ruta_usuarios, self.usuarios), f"Ahora eres amigo de {amigo.nombre}")
            self.mostrar_muro()

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def mostrar_resumen(self):
        resumenes = []

    # Resumen del usuario actual
        resumenes.append(self.usuario_actual.resumen())

    # Resumen de publicaciones
        for pub in self.usuario_actual.publicaciones:
            resumenes.append(pub.resumen())

    # Resumen de comentarios hechos por el usuario en publicaciones propias
        for pub in self.usuario_actual.publicaciones:
            for comentario in pub.comentarios:
                if comentario.autor == self.usuario_actual:
                    resumenes.append(comentario.resumen())

    # Mostrar todos los resumenes
        messagebox.showinfo("Resumen de Actividad", "\n\n".join(resumenes))
            