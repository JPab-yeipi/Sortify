"""
UI_Logic.py
Graphical interface logic for Sortify (sorting algorithms visualizer).
"""

# --- Imports ---
import tkinter as tk
from tkinter import PhotoImage
import os
import random
import importlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# --- Asset paths ---
RUTA_ICONO = os.path.join(BASE_DIR, "Assets", "Icon", "Icon_Sortify.ico")
RUTA_IMAGEN_MP = os.path.join(BASE_DIR, "Assets", "Titulos", "Logo_Sortify.png")
RUTA_IMAGEN_MP_2 = os.path.join(BASE_DIR, "Assets", "Titulos", "Logo_menuPrincipal_1.png")
RUTA_IMAGEN_MS = os.path.join(BASE_DIR, "Assets", "Titulos", "Titulo_sorts2.png")
RUTA_BOTONES = os.path.join(BASE_DIR, "Assets", "Botones")
RUTA_TITULO_AJUSTES = os.path.join(BASE_DIR, "Assets", "Titulos", "Titulo_Ajustes.png")
RUTA_TITULO_CTRL = os.path.join(BASE_DIR, "Assets", "Titulos", "Titulo_graficadora.png")
RUTA_TITULO_COMPLEJIDAD = os.path.join(BASE_DIR, "Assets", "Titulos", "Titulo_complejidad.png")

# Definición de métodos de ordenamiento y sus colores asociados
metodos = [
    ("Bubble Sort", 1, 1, "verde"),
    ("Counting Sort", 2, 1, "naranja"),
    ("Insertion Sort", 3, 1, "azul"),
    ("Quick Sort", 4, 1, "morado"),
    ("Selection Sort", 1, 2, "rojo"),
    ("Shell Sort", 2, 2, "oro"),
    ("Heap Sort", 3, 2, "gris"),
    ("Merge Sort", 4, 2, "vino"),
    ("Radix Sort", 1, 3, "amarillo"),
    ("Tim Sort", 2, 3, "cian"),
    ("Intro Sort", 3, 3, "verdeAzul"),
    ("Pigeonhole Sort", 4, 3, "azul_claro"),
    ("Bucket Sort", 1, 4, "green"),
    ("Cycle Sort", 2, 4, "rosa"),
    ("Gnome Sort", 3, 4, "amarillo"),
    ("Bitonic Sort", 4, 4, "purple"),
    ("Comb Sort", 1, 5, "morado"),
    ("Cocktail Sort", 2, 5, "azul"),
    ("Bitwise Sort", 3, 5, "oro"),
    ("Pancake Sort", 4, 5, "verde")
]

# Colores disponibles para los botones
colores = [
    "verde", "naranja", "azul", "morado", "rojo", "oro", "gris", "vino",
    "amarillo", "cian", "verdeAzul", "azul_claro", "green", "rosa", "purple"
]

# --- MENÚ PRINCIPAL ---
def Menu_Principal():
    ventana = tk.Tk()
    ventana.title("SORTIFY - MENÚ PRINCIPAL")
    ventana.geometry("1050x650")
    ventana.configure(bg="#e8e4e3")
    ventana.iconbitmap(RUTA_ICONO)

    # Carga de imágenes de los títulos
    img_mp = PhotoImage(file=RUTA_IMAGEN_MP).subsample(6, 6)
    img_mp_2 = PhotoImage(file=RUTA_IMAGEN_MP_2).subsample(2, 2)
    img_ms = PhotoImage(file=RUTA_IMAGEN_MS)

    frame_titulo = tk.Frame(ventana, bg="#e8e4e3")
    frame_titulo.pack(pady=10)
    tk.Label(frame_titulo, image=img_mp, bg="#e8e4e3").pack(side="left", padx=5)
    tk.Label(frame_titulo, image=img_mp_2, bg="#e8e4e3").pack(side="left", padx=5)
    tk.Label(ventana, image=img_ms, bg="#e8e4e3").pack(pady=10)

    # Frame que contiene canvas y texto inferior
    frame_canvas = tk.Frame(ventana, bg="#e8e4e3")
    frame_canvas.pack()

    # Canvas para botones
    canvas = tk.Canvas(frame_canvas, width=1100, height=430, bg="#e8e4e3", highlightthickness=0)
    canvas.pack()

    # Carga de imágenes para los botones
    imagenes_on = {color: PhotoImage(file=os.path.join(RUTA_BOTONES, f"SBtn_{color}_on.png")) for color in colores}
    imagenes_off = {color: PhotoImage(file=os.path.join(RUTA_BOTONES, f"SBtn_{color}_off.png")) for color in colores}

    fuente = ("Pixelify Sans", 20)
    espacio_x = 260
    espacio_y = 85

    for texto, col, fila, color in metodos:
        x = espacio_x * col - espacio_x / 2
        y = espacio_y * fila - espacio_y / 2

        imagen_id = canvas.create_image(x, y + 2, image=imagenes_off[color])
        sombra_id = canvas.create_text(x + 2, y + 2, text=texto, font=fuente, fill="black")
        texto_id = canvas.create_text(x, y, text=texto, font=fuente, fill="white")

        def al_presionar(event, img=imagen_id, txt=texto_id, sombra=sombra_id, col=color):
            canvas.itemconfig(img, image=imagenes_on[col])
            canvas.itemconfig(txt, fill="#b0b0b0")
            canvas.move(txt, 0, 6)
            canvas.move(sombra, 0, 6)

        def al_soltar(event, img=imagen_id, txt=texto_id, sombra=sombra_id, col=color, nombre=texto):
            canvas.itemconfig(img, image=imagenes_off[col])
            canvas.itemconfig(txt, fill="white")
            canvas.move(txt, 0, -6)
            canvas.move(sombra, 0, -6)
            Ajustes(nombre, ventana)

        for item in [imagen_id, texto_id, sombra_id]:
            canvas.tag_bind(item, "<ButtonPress-1>", al_presionar)
            canvas.tag_bind(item, "<ButtonRelease-1>", al_soltar)

    # Texto final debajo del canvas
    texto_final = tk.Label(
        ventana,
        text="| Instala la fuente Pixelify Sans ubicada en Assets para mejorar la estetica |         Sortify-v.1.2.0",
        font=fuente,
        fg="black",
        bg="#e8e4e3"
    )
    texto_final.pack(pady=5)

    # Centrar la ventana
    ventana.update_idletasks()
    w, h = ventana.winfo_width(), ventana.winfo_height()
    sw, sh = ventana.winfo_screenwidth(), ventana.winfo_screenheight()
    x, y = (sw - w) // 2, (sh - h) // 2
    ventana.geometry(f"{w}x{h}+{x}+{y}")

    ventana.mainloop()


# --- VENTANA DE AJUSTES ---
def Ajustes(nombre_opcion, ventana_anterior):
    if ventana_anterior is not None:
        ventana_anterior.destroy()

    ventana = tk.Tk()
    ventana.title("AJUSTES")
    ventana.geometry("800x600")
    ventana.configure(bg="#e8e4e3")
    ventana.iconbitmap(RUTA_ICONO)

    titulo_ajustes = PhotoImage(file=RUTA_TITULO_AJUSTES)
    tk.Label(ventana, image=titulo_ajustes, bg="#e8e4e3").pack(pady=20)

    fuente_texto = ("Pixelify Sans", 24)
    texto = f"Opción seleccionada: {nombre_opcion}"
    tk.Label(ventana, text=texto, font=fuente_texto, bg="#e8e4e3", fg="black").pack(pady=10)

    frame_controles = tk.Frame(ventana, bg="#e8e4e3")
    frame_controles.pack(pady=20)

    # Slider para ajustar la velocidad
    velocidad_var = tk.DoubleVar(value=1)
    tk.Scale(frame_controles, from_=0.1, to=5.0, resolution=0.1, orient="horizontal",
             variable=velocidad_var, label="Velocidad", bg="#e8e4e3", font=("Pixelify Sans", 16), fg="black",
             troughcolor="#ed5b37", activebackground="#e8e4e3", length=300, width=30, sliderlength=40
             ).pack(side="left", padx=40)

    # Slider para ajustar la cantidad de elementos
    elementos_var = tk.IntVar(value=100)
    tk.Scale(frame_controles, from_=10, to=1000, resolution=10, orient="horizontal",
             variable=elementos_var, label="Elementos", bg="#e8e4e3", font=("Pixelify Sans", 16), fg="black",
             troughcolor="#375eed", activebackground="#e8e4e3", length=300, width=30, sliderlength=40
             ).pack(side="left", padx=40)

    frame_botones = tk.Frame(ventana, bg="#e8e4e3")
    frame_botones.pack(pady=80)

    graficadora_off = PhotoImage(file=os.path.join(BASE_DIR, "Assets", "Botones", "btn_graficadora_off.png"))
    graficadora_on = PhotoImage(file=os.path.join(BASE_DIR, "Assets", "Botones", "btn_graficadora_on.png"))
    complejidad_off = PhotoImage(file=os.path.join(BASE_DIR, "Assets", "Botones", "btn_complejidad_off.png"))
    complejidad_on = PhotoImage(file=os.path.join(BASE_DIR, "Assets", "Botones", "btn_complejidad_on.png"))

    # Botón para Complejidad
    canvas_b1 = tk.Canvas(frame_botones, width=complejidad_off.width(), height=complejidad_off.height(),
                          bg="#e8e4e3", highlightthickness=0)
    canvas_b1.pack(side="left", padx=40)
    b1_img = canvas_b1.create_image(complejidad_off.width() // 2, complejidad_off.height() // 2, image=complejidad_off)

    def presionar_b1(event):
        canvas_b1.itemconfig(b1_img, image=complejidad_on)

    def soltar_b1(event):
        canvas_b1.itemconfig(b1_img, image=complejidad_off)
        Ventana_Complejidad(nombre_opcion)

    canvas_b1.tag_bind(b1_img, "<ButtonPress-1>", presionar_b1)
    canvas_b1.tag_bind(b1_img, "<ButtonRelease-1>", soltar_b1)

    #Boton para graficadora
    canvas_b2 = tk.Canvas(frame_botones, width=graficadora_off.width(), height=graficadora_off.height(),
                          bg="#e8e4e3", highlightthickness=0)
    canvas_b2.pack(side="left", padx=40)
    b2_img = canvas_b2.create_image(graficadora_off.width() // 2, graficadora_off.height() // 2, image=graficadora_off)

    def presionar_b2(event):
        canvas_b2.itemconfig(b2_img, image=graficadora_on)

    def soltar_b2(event):
        canvas_b2.itemconfig(b2_img, image=graficadora_off)
        ventana.destroy()
        Graficadora(nombre_opcion, velocidad_var.get(), elementos_var.get())

    canvas_b2.tag_bind(b2_img, "<ButtonPress-1>", presionar_b2)
    canvas_b2.tag_bind(b2_img, "<ButtonRelease-1>", soltar_b2)

    # Botón para regresar al menú principal
    img_btn_normal = PhotoImage(file=os.path.join(RUTA_BOTONES, "SBtn_rojo_off.png"))
    img_btn_presionado = PhotoImage(file=os.path.join(RUTA_BOTONES, "SBtn_rojo_on.png"))

    frame_regresar = tk.Frame(ventana, bg="#e8e4e3")
    frame_regresar.pack(side="bottom", anchor="w", padx=20, pady=10)

    canvas_btn = tk.Canvas(frame_regresar, width=img_btn_normal.width(), height=img_btn_normal.height(),
                           bg="#e8e4e3", highlightthickness=0)
    canvas_btn.pack()

    img_id = canvas_btn.create_image(img_btn_normal.width() // 2, img_btn_normal.height() // 2, image=img_btn_normal)
    sombra_id = canvas_btn.create_text(img_btn_normal.width() // 2 + 2, img_btn_normal.height() // 2 + 2,
                                       text="← Regresar", font=("Pixelify Sans", 20), fill="black")
    texto_id = canvas_btn.create_text(img_btn_normal.width() // 2, img_btn_normal.height() // 2,
                                      text="← Regresar", font=("Pixelify Sans", 20), fill="white")

    def presionar_regresar(event):
        canvas_btn.itemconfig(img_id, image=img_btn_presionado)
        canvas_btn.itemconfig(texto_id, fill="#b0b0b0")
        canvas_btn.move(texto_id, 0, 6)
        canvas_btn.move(sombra_id, 0, 6)

    def soltar_regresar(event):
        canvas_btn.itemconfig(img_id, image=img_btn_normal)
        canvas_btn.itemconfig(texto_id, fill="white")
        canvas_btn.move(texto_id, 0, -6)
        canvas_btn.move(sombra_id, 0, -6)
        ventana.destroy()
        Menu_Principal()

    for item in [img_id, texto_id, sombra_id]:
        canvas_btn.tag_bind(item, "<ButtonPress-1>", presionar_regresar)
        canvas_btn.tag_bind(item, "<ButtonRelease-1>", soltar_regresar)

    ventana.update_idletasks()
    w, h = ventana.winfo_width(), ventana.winfo_height()
    sw, sh = ventana.winfo_screenwidth(), ventana.winfo_screenheight()
    x, y = (sw - w) // 2, (sh - h) // 2
    ventana.geometry(f"{w}x{h}+{x}+{y}")

    ventana.mainloop()


# --- VENTANAS DE GRAFICADORA ---
def Graficadora(nombre_opcion, velocidad, cantidad):
    ventana_vis = tk.Tk()
    ventana_vis.title("Visualización del Método")
    ventana_vis.geometry("1000x470+200+100")
    ventana_vis.configure(bg="#e8e4e3")

    # Estado compartido entre las funciones: 'detenido', 'corriendo' o 'pausado'
    estado = {"valor": "detenido"}

    # Área de dibujo para visualizar las barras
    canvas = tk.Canvas(ventana_vis, width=980, height=450, bg="white", highlightthickness=0)
    canvas.pack(padx=10, pady=10)

    # Generación de datos aleatorios para graficar
    datos = random.sample(range(1, cantidad + 1), cantidad)

    def dibujar_barras(arr, colores):
        # Dibuja las barras en el canvas según los datos y colores proporcionados.

        canvas.delete("all")

        c_width = canvas.winfo_width()
        c_height = canvas.winfo_height()

        n = len(arr)
        if n == 0:
            return

        ancho = c_width / n
        max_val = max(arr) if max(arr) != 0 else 1

        for i, val in enumerate(arr):
            x0 = int(i * ancho)
            x1 = int((i + 1) * ancho)
            y1 = c_height
            y0 = int(c_height - (val / max_val) * (c_height - 50))  # margen arriba

            canvas.create_rectangle(x0, y0, x1, y1, fill=colores[i], outline="")

        ventana_vis.update_idletasks()

    dibujar_barras.canvas = canvas
    dibujar_barras.estado = estado

    # Funciones de control del estado
    def iniciar_ordenamiento():
        #Inicia el algoritmo de ordenamiento seleccionado.

        if estado["valor"] == "detenido":
            estado["valor"] = "corriendo"
            try:
                # Carga dinámica del módulo y la función del algoritmo
                modulo = nombre_opcion.title().replace(" ", "_")
                funcion = nombre_opcion.lower().replace(" ", "_")
                ruta_completa = f"Metodos_Ordenamiento.{modulo}"
                algoritmo = importlib.import_module(ruta_completa)
                algoritmo_funcion = getattr(algoritmo, funcion)
                algoritmo_funcion(datos, draw_func=dibujar_barras, delay=velocidad)
            except (ModuleNotFoundError, AttributeError) as e:
                print(f"No se pudo cargar el algoritmo para: {nombre_opcion}")
                print("Error:", e)

    def pausar_reanudar():
        # Pausa o reanuda la ejecución del algoritmo según el estado actual.

        if estado["valor"] == "corriendo":
            estado["valor"] = "pausado"
        elif estado["valor"] == "pausado":
            estado["valor"] = "corriendo"

    def detener():
        # Detiene la ejecución del algoritmo.

        estado["valor"] = "detenido"

    def regresar_ajustes():
        # Cierra las ventanas actuales y regresa a la configuración.

        ventana_ctrl.destroy()
        ventana_vis.destroy()
        Ajustes(nombre_opcion, None)

    # Etiqueta con información sobre el metodo seleccionado
    info_text = f"Método: {nombre_opcion} | Velocidad: {velocidad} | Elementos: {cantidad}"
    fuente_info = ("Pixelify Sans", 20)

    label_info_vis = tk.Label(
        ventana_vis,
        text=info_text,
        font=fuente_info,
        fg="black",
        bg="#e8e4e3"
    )
    label_info_vis.pack(side="bottom", pady=5)

    # Configuración de la ventana de controles
    ventana_ctrl = tk.Toplevel(ventana_vis)
    ventana_ctrl.title("Controles del Algoritmo")
    ventana_ctrl.geometry("1000x200+200+600")  # Posición debajo de la ventana principal
    ventana_ctrl.configure(bg="#e8e4e3")

    # Imagen de título de la ventana de control
    titulo_ctrl = PhotoImage(file=RUTA_TITULO_CTRL)
    tk.Label(ventana_ctrl, image=titulo_ctrl, bg="#e8e4e3").pack(pady=5)
    ventana_ctrl.titulo_ctrl = titulo_ctrl  # Referencia para evitar pérdida de la imagen

    # Configuración de los botones personalizados
    botones_info = [
        ("← Regresar", regresar_ajustes, "rojo"),
        ("Iniciar", iniciar_ordenamiento, "verde"),
        ("Pausar/Reanudar", pausar_reanudar, "azul"),
        ("Detener", detener, "naranja")
    ]

    imagenes_botones = {}
    for _, _, color in botones_info:
        img_off = PhotoImage(file=os.path.join(RUTA_BOTONES, f"SBtn_{color}_off.png"))
        img_on = PhotoImage(file=os.path.join(RUTA_BOTONES, f"SBtn_{color}_on.png"))
        imagenes_botones[color] = (img_off, img_on)

    frame_botones = tk.Frame(ventana_ctrl, bg="#e8e4e3")
    frame_botones.pack(pady=10)

    fuente_boton = ("Pixelify Sans", 16)
    desplazamiento = 6

    for texto, funcion, color in botones_info:
        img_off, img_on = imagenes_botones[color]
        btn_canvas = tk.Canvas(
            frame_botones,
            width=img_off.width(),
            height=img_off.height(),
            bg="#e8e4e3",
            highlightthickness=0
        )
        btn_canvas.pack(side="left", padx=10, pady=5)

        btn_img_id = btn_canvas.create_image(img_off.width() // 2, img_off.height() // 2, image=img_off)
        btn_sombra_id = btn_canvas.create_text(
            img_off.width() // 2 + 2,
            img_off.height() // 2 + 2,
            text=texto,
            font=fuente_boton,
            fill="black"
        )
        btn_texto_id = btn_canvas.create_text(
            img_off.width() // 2,
            img_off.height() // 2,
            text=texto,
            font=fuente_boton,
            fill="white"
        )

        def presionar(event, canvas=btn_canvas, img_id=btn_img_id, texto_id=btn_texto_id, sombra_id=btn_sombra_id, col=color):
            canvas.itemconfig(img_id, image=imagenes_botones[col][1])
            canvas.itemconfig(texto_id, fill="#b0b0b0")
            canvas.move(texto_id, 0, desplazamiento)
            canvas.move(sombra_id, 0, desplazamiento)

        def soltar(event, canvas=btn_canvas, img_id=btn_img_id, texto_id=btn_texto_id, sombra_id=btn_sombra_id, col=color, func=funcion):
            canvas.itemconfig(img_id, image=imagenes_botones[col][0])
            canvas.itemconfig(texto_id, fill="white")
            canvas.move(texto_id, 0, -desplazamiento)
            canvas.move(sombra_id, 0, -desplazamiento)
            func()

        for item in [btn_img_id, btn_texto_id, btn_sombra_id]:
            btn_canvas.tag_bind(item, "<ButtonPress-1>", presionar)
            btn_canvas.tag_bind(item, "<ButtonRelease-1>", soltar)

    # Etiqueta con información en la ventana de control
    label_info_ctrl = tk.Label(
        ventana_ctrl,
        text=info_text,
        font=fuente_info,
        fg="black",
        bg="#e8e4e3"
    )
    label_info_ctrl.pack(side="bottom", pady=5)

    ventana_vis.mainloop()


# --- VENTANA DE COMPLEJIDAD ---
def Ventana_Complejidad(nombre_opcion):

    def cargar_algoritmo(nombre):
        modulo = nombre.title().replace(" ", "_")
        funcion = nombre.lower().replace(" ", "_") + "_estudio"
        try:
            mod = importlib.import_module(f"Metodos_Ordenamiento.{modulo}")
            return getattr(mod, funcion)
        except Exception as e:
            print(f"Error cargando '{nombre}': {e}")
            return None

    def generar_lista(tamano):
        return (random.sample(range(1, tamano + 1), tamano)
                if tipo_lista.get() == "aleatoria"
                else list(range(tamano, 0, -1)))

    def actualizar_grafica():
        ax.clear()
        ax.set_title(f"Complejidad de {nombre_opcion}")
        ax.set_xlabel("Cantidad de elementos")
        ax.set_ylabel("Pasos")
        ax.grid(True)
        return ax.plot([], [], color="black", linewidth=2)[0]

    def ejecutar_paso():
        nonlocal tam_actual, id_paso
        if not ejecutando.get():
            id_paso = ventana_vis.after(100, ejecutar_paso)
            return
        lista = generar_lista(tam_actual)
        pasos.append(algoritmo_funcion(lista.copy()))
        cantidades.append(tam_actual)
        linea_plot.set_data(cantidades, pasos)
        ax.relim()
        ax.autoscale_view()
        canvas.draw()
        tam_actual += 20
        id_paso = ventana_vis.after(100, ejecutar_paso)

    def iniciar_analisis(reset=False):
        nonlocal tam_actual, cantidades, pasos, linea_plot, id_paso
        if reset and id_paso:
            ventana_vis.after_cancel(id_paso)
        tam_actual = 20
        cantidades.clear()
        pasos.clear()
        linea_plot = actualizar_grafica()
        canvas.draw()
        ejecutar_paso()

    def cambiar_tipo(nuevo):
        tipo_lista.set(nuevo)
        iniciar_analisis(reset=True)

    def toggle_pausa():
        ejecutando.set(not ejecutando.get())
        txt = "Pausa/Reanudar"
        canvas_pausar.itemconfig(pausar_text_id, text=txt)

    # --- Ventana de visualización ---
    ventana_vis = tk.Toplevel()
    ventana_vis.title("Pasos del Algoritmo")
    ventana_vis.geometry("1000x470+200+100")
    ventana_vis.configure(bg="#e8e4e3")

    fig, ax = plt.subplots(figsize=(7.5, 5))
    fig.patch.set_facecolor("#e8e4e3")
    canvas = FigureCanvasTkAgg(fig, master=ventana_vis)
    canvas.get_tk_widget().pack(pady=10)

    tipo_lista = tk.StringVar(value="aleatoria")
    ejecutando = tk.BooleanVar(value=True)
    cantidades, pasos = [], []
    tam_actual, id_paso = 20, None
    linea_plot = None

    algoritmo_funcion = cargar_algoritmo(nombre_opcion)
    if not algoritmo_funcion:
        ventana_vis.destroy()
        return

    # --- Ventana de controles ---
    ventana_ctrl = tk.Toplevel(ventana_vis)
    ventana_ctrl.title("Controles del Algoritmo")
    ventana_ctrl.geometry("1000x200+200+600")
    ventana_ctrl.configure(bg="#e8e4e3")

    titulo_img = PhotoImage(file=RUTA_TITULO_COMPLEJIDAD)
    lbl_titulo = tk.Label(ventana_ctrl, image=titulo_img, bg="#e8e4e3")
    lbl_titulo.image = titulo_img
    lbl_titulo.pack(pady=10)

    frame_botones = tk.Frame(ventana_ctrl, bg="#e8e4e3")
    frame_botones.pack(pady=10)

    fuente_boton = ("Pixelify Sans", 16)
    desplazamiento = 6

    # --- Botón Aleatoria ---
    btn_aleatoria_off_img = PhotoImage(file=os.path.join(RUTA_BOTONES, "SBtn_verde_off.png"))
    btn_aleatoria_on_img = PhotoImage(file=os.path.join(RUTA_BOTONES, "SBtn_verde_on.png"))
    canvas_aleatoria = tk.Canvas(frame_botones, width=btn_aleatoria_off_img.width(),
                                 height=btn_aleatoria_off_img.height(), bg="#e8e4e3", highlightthickness=0)
    canvas_aleatoria.pack(side="left", padx=10)
    aleatoria_img_id = canvas_aleatoria.create_image(btn_aleatoria_off_img.width()//2,
                                                     btn_aleatoria_off_img.height()//2,
                                                     image=btn_aleatoria_off_img)
    aleatoria_sombra_id = canvas_aleatoria.create_text(btn_aleatoria_off_img.width()//2 + 2,
                                                       btn_aleatoria_off_img.height()//2 + 2,
                                                       text="Aleatoria", font=fuente_boton, fill="black")
    aleatoria_text_id = canvas_aleatoria.create_text(btn_aleatoria_off_img.width()//2,
                                                     btn_aleatoria_off_img.height()//2,
                                                     text="Aleatoria", font=fuente_boton, fill="white")
    def on_press_aleatoria(event):
        canvas_aleatoria.itemconfig(aleatoria_img_id, image=btn_aleatoria_on_img)
        canvas_aleatoria.itemconfig(aleatoria_text_id, fill="#b0b0b0")
        canvas_aleatoria.move(aleatoria_text_id, 0, desplazamiento)
        canvas_aleatoria.move(aleatoria_sombra_id, 0, desplazamiento)

    def on_release_aleatoria(event):
        canvas_aleatoria.itemconfig(aleatoria_img_id, image=btn_aleatoria_off_img)
        canvas_aleatoria.itemconfig(aleatoria_text_id, fill="white")
        canvas_aleatoria.move(aleatoria_text_id, 0, -desplazamiento)
        canvas_aleatoria.move(aleatoria_sombra_id, 0, -desplazamiento)
        cambiar_tipo("aleatoria")

    for item in canvas_aleatoria.find_all():
        canvas_aleatoria.tag_bind(item, "<ButtonPress-1>", on_press_aleatoria)
        canvas_aleatoria.tag_bind(item, "<ButtonRelease-1>", on_release_aleatoria)

    # --- Botón Inversa ---
    btn_inversa_off_img = PhotoImage(file=os.path.join(RUTA_BOTONES, "SBtn_oro_off.png"))
    btn_inversa_on_img = PhotoImage(file=os.path.join(RUTA_BOTONES, "SBtn_oro_on.png"))
    canvas_inversa = tk.Canvas(frame_botones, width=btn_inversa_off_img.width(),
                               height=btn_inversa_off_img.height(), bg="#e8e4e3", highlightthickness=0)
    canvas_inversa.pack(side="left", padx=10)
    inversa_img_id = canvas_inversa.create_image(btn_inversa_off_img.width()//2,
                                                 btn_inversa_off_img.height()//2,
                                                 image=btn_inversa_off_img)
    inversa_sombra_id = canvas_inversa.create_text(btn_inversa_off_img.width()//2 + 2,
                                                   btn_inversa_off_img.height()//2 + 2,
                                                   text="Inversa", font=fuente_boton, fill="black")
    inversa_text_id = canvas_inversa.create_text(btn_inversa_off_img.width()//2,
                                                 btn_inversa_off_img.height()//2,
                                                 text="Inversa", font=fuente_boton, fill="white")

    def on_press_inversa(event):
        canvas_inversa.itemconfig(inversa_img_id, image=btn_inversa_on_img)
        canvas_inversa.itemconfig(inversa_text_id, fill="#b0b0b0")
        canvas_inversa.move(inversa_text_id, 0, desplazamiento)
        canvas_inversa.move(inversa_sombra_id, 0, desplazamiento)

    def on_release_inversa(event):
        canvas_inversa.itemconfig(inversa_img_id, image=btn_inversa_off_img)
        canvas_inversa.itemconfig(inversa_text_id, fill="white")
        canvas_inversa.move(inversa_text_id, 0, -desplazamiento)
        canvas_inversa.move(inversa_sombra_id, 0, -desplazamiento)
        cambiar_tipo("inversa")

    for item in canvas_inversa.find_all():
        canvas_inversa.tag_bind(item, "<ButtonPress-1>", on_press_inversa)
        canvas_inversa.tag_bind(item, "<ButtonRelease-1>", on_release_inversa)

    # --- Botón Pausar/Reanudar ---
    btn_pausar_off_img = PhotoImage(file=os.path.join(RUTA_BOTONES, "SBtn_azul_off.png"))
    btn_pausar_on_img = PhotoImage(file=os.path.join(RUTA_BOTONES, "SBtn_azul_on.png"))
    canvas_pausar = tk.Canvas(frame_botones, width=btn_pausar_off_img.width(),
                              height=btn_pausar_off_img.height(), bg="#e8e4e3", highlightthickness=0)
    canvas_pausar.pack(side="left", padx=10)
    pausar_img_id = canvas_pausar.create_image(btn_pausar_off_img.width()//2,
                                               btn_pausar_off_img.height()//2,
                                               image=btn_pausar_off_img)
    pausar_sombra_id = canvas_pausar.create_text(btn_pausar_off_img.width()//2 + 2,
                                                 btn_pausar_off_img.height()//2 + 2,
                                                 text="Pausa/Reanudar", font=fuente_boton, fill="black")
    pausar_text_id = canvas_pausar.create_text(btn_pausar_off_img.width()//2,
                                               btn_pausar_off_img.height()//2,
                                               text="Pausa/Reanudar", font=fuente_boton, fill="white")

    def on_press_pausar(event):
        canvas_pausar.itemconfig(pausar_img_id, image=btn_pausar_on_img)
        canvas_pausar.itemconfig(pausar_text_id, fill="#b0b0b0")
        canvas_pausar.move(pausar_text_id, 0, desplazamiento)
        canvas_pausar.move(pausar_sombra_id, 0, desplazamiento)

    def on_release_pausar(event):
        canvas_pausar.itemconfig(pausar_img_id, image=btn_pausar_off_img)
        canvas_pausar.itemconfig(pausar_text_id, fill="white")
        canvas_pausar.move(pausar_text_id, 0, -desplazamiento)
        canvas_pausar.move(pausar_sombra_id, 0, -desplazamiento)
        toggle_pausa()

    for item in canvas_pausar.find_all():
        canvas_pausar.tag_bind(item, "<ButtonPress-1>", on_press_pausar)
        canvas_pausar.tag_bind(item, "<ButtonRelease-1>", on_release_pausar)

    # --- TEXTO PERSONALIZADO ---
    lbl_texto = tk.Label(
        ventana_ctrl,
        text="| Cierra la ventana superior para eliminar esta ventana |",
        font=("Pixelify Sans", 16),
        fg="black",
        bg="#e8e4e3"
    )
    lbl_texto.pack(pady=10)

    ventana_vis.mainloop()