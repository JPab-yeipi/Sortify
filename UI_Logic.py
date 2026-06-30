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
ICON_PATH = os.path.join(BASE_DIR, "Assets", "Icon", "Icon_Sortify.ico")
LOGO_IMAGE_PATH = os.path.join(BASE_DIR, "Assets", "Titulos", "Logo_Sortify.png")
LOGO_IMAGE_PATH_2 = os.path.join(BASE_DIR, "Assets", "Titulos", "Logo_menuPrincipal_1.png")
SUBTITLE_IMAGE_PATH = os.path.join(BASE_DIR, "Assets", "Titulos", "Titulo_sorts2.png")
BUTTONS_PATH = os.path.join(BASE_DIR, "Assets", "Botones")
SETTINGS_TITLE_PATH = os.path.join(BASE_DIR, "Assets", "Titulos", "Titulo_Ajustes.png")
CONTROL_TITLE_PATH = os.path.join(BASE_DIR, "Assets", "Titulos", "Titulo_graficadora.png")
COMPLEXITY_TITLE_PATH = os.path.join(BASE_DIR, "Assets", "Titulos", "Titulo_complejidad.png")

# --- Theme constants ---
BACKGROUND_COLOR = "#e8e4e3"
PRESSED_TEXT_COLOR = "#b0b0b0"
DEFAULT_FONT_NAME = "Pixelify Sans"

# --- Sorting methods: (display name, column, row, button color) ---
METHODS = [
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
    ("Pancake Sort", 4, 5, "verde"),
]

# Button color keys must stay in sync with the "SBtn_<color>_on/off.png" assets.
COLORS = sorted({color for _, _, _, color in METHODS})


# =============================================================
# Generic UI helpers
# =============================================================

def center_window(window):
    """Center a window on the screen based on its current size."""
    window.update_idletasks()
    width, height = window.winfo_width(), window.winfo_height()
    screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def bind_button_behavior(canvas, image_id, image_off, image_on, on_click,
                          text_id=None, shadow_id=None, shift=6):
    """Attach press/release visual feedback (image swap + text shift) to a canvas button."""

    def on_press(_event):
        canvas.itemconfig(image_id, image=image_on)
        if text_id is not None:
            canvas.itemconfig(text_id, fill=PRESSED_TEXT_COLOR)
            canvas.move(text_id, 0, shift)
            canvas.move(shadow_id, 0, shift)

    def on_release(_event):
        canvas.itemconfig(image_id, image=image_off)
        if text_id is not None:
            canvas.itemconfig(text_id, fill="white")
            canvas.move(text_id, 0, -shift)
            canvas.move(shadow_id, 0, -shift)
        if on_click:
            on_click()

    items = [image_id] + ([text_id, shadow_id] if text_id is not None else [])
    for item in items:
        canvas.tag_bind(item, "<ButtonPress-1>", on_press)
        canvas.tag_bind(item, "<ButtonRelease-1>", on_release)


def create_pixel_button(canvas, x, y, image_off, image_on, on_click,
                         text=None, font=(DEFAULT_FONT_NAME, 16)):
    """Create a press/release styled button centered at (x, y) on an existing canvas."""
    image_id = canvas.create_image(x, y, image=image_off)
    text_id = shadow_id = None
    if text is not None:
        shadow_id = canvas.create_text(x + 2, y + 2, text=text, font=font, fill="black")
        text_id = canvas.create_text(x, y, text=text, font=font, fill="white")
    bind_button_behavior(canvas, image_id, image_off, image_on, on_click, text_id, shadow_id)
    return image_id, text_id, shadow_id


def create_standalone_button(parent, image_off, image_on, on_click,
                              text=None, font=(DEFAULT_FONT_NAME, 16),
                              side="left", padx=10, pady=0):
    """Create a button inside its own canvas (sized to the image) and pack it into parent."""
    canvas = tk.Canvas(
        parent, width=image_off.width(), height=image_off.height(),
        bg=BACKGROUND_COLOR, highlightthickness=0
    )
    canvas.pack(side=side, padx=padx, pady=pady)
    create_pixel_button(
        canvas, image_off.width() // 2, image_off.height() // 2,
        image_off, image_on, on_click, text=text, font=font
    )
    return canvas


# =============================================================
# Algorithm loading helpers
# =============================================================

def load_sort_module(method_name):
    """Dynamically import the module that implements the given sorting method."""
    module_name = method_name.title().replace(" ", "_")
    try:
        # Folder name kept as "Metodos_Ordenamiento" to match the existing module structure.
        return importlib.import_module(f"Metodos_Ordenamiento.{module_name}")
    except ModuleNotFoundError as error:
        print(f"Could not load module for '{method_name}': {error}")
        return None


def load_sort_function(method_name):
    """Return the sorting function (animated version) for the given method, or None."""
    module = load_sort_module(method_name)
    if module is None:
        return None
    function_name = method_name.lower().replace(" ", "_")
    function = getattr(module, function_name, None)
    if function is None:
        print(f"Function '{function_name}' not found for '{method_name}'.")
    return function


def load_study_function(method_name):
    """Return the complexity-study function for the given method, or None.

    Kept with the "_estudio" suffix to match the naming convention used in the
    Metodos_Ordenamiento files; update both sides together if that changes.
    """
    module = load_sort_module(method_name)
    if module is None:
        return None
    function_name = method_name.lower().replace(" ", "_") + "_estudio"
    function = getattr(module, function_name, None)
    if function is None:
        print(f"Function '{function_name}' not found for '{method_name}'.")
    return function


# =============================================================
# MAIN MENU
# =============================================================

def main_menu():
    window = tk.Tk()
    window.title("SORTIFY - MAIN MENU")
    window.geometry("1050x650")
    window.configure(bg=BACKGROUND_COLOR)
    window.iconbitmap(ICON_PATH)

    # Title images
    logo_image = PhotoImage(file=LOGO_IMAGE_PATH).subsample(6, 6)
    logo_image_2 = PhotoImage(file=LOGO_IMAGE_PATH_2).subsample(2, 2)
    subtitle_image = PhotoImage(file=SUBTITLE_IMAGE_PATH)

    title_frame = tk.Frame(window, bg=BACKGROUND_COLOR)
    title_frame.pack(pady=10)
    tk.Label(title_frame, image=logo_image, bg=BACKGROUND_COLOR).pack(side="left", padx=5)
    tk.Label(title_frame, image=logo_image_2, bg=BACKGROUND_COLOR).pack(side="left", padx=5)
    tk.Label(window, image=subtitle_image, bg=BACKGROUND_COLOR).pack(pady=10)

    canvas_frame = tk.Frame(window, bg=BACKGROUND_COLOR)
    canvas_frame.pack()

    canvas = tk.Canvas(canvas_frame, width=1100, height=430, bg=BACKGROUND_COLOR, highlightthickness=0)
    canvas.pack()

    images_on = {color: PhotoImage(file=os.path.join(BUTTONS_PATH, f"SBtn_{color}_on.png")) for color in COLORS}
    images_off = {color: PhotoImage(file=os.path.join(BUTTONS_PATH, f"SBtn_{color}_off.png")) for color in COLORS}

    font = (DEFAULT_FONT_NAME, 20)
    spacing_x = 260
    spacing_y = 85

    for name, col, row, color in METHODS:
        x = spacing_x * col - spacing_x / 2
        y = spacing_y * row - spacing_y / 2
        create_pixel_button(
            canvas, x, y,
            images_off[color], images_on[color],
            on_click=lambda option=name: settings_window(option, window),
            text=name, font=font
        )

    footer_label = tk.Label(
        window,
        text="| Install the Pixelify Sans font located in Assets for a better look |"
             "                     Sortify-v.1.2.0",
        font=font,
        fg="black",
        bg=BACKGROUND_COLOR
    )
    footer_label.pack(pady=5)

    center_window(window)
    window.mainloop()


# =============================================================
# SETTINGS WINDOW
# =============================================================

def settings_window(option_name, previous_window):
    if previous_window is not None:
        previous_window.destroy()

    window = tk.Tk()
    window.title("SETTINGS")
    window.geometry("800x650")
    window.configure(bg=BACKGROUND_COLOR)
    window.iconbitmap(ICON_PATH)

    settings_title_image = PhotoImage(file=SETTINGS_TITLE_PATH)
    tk.Label(window, image=settings_title_image, bg=BACKGROUND_COLOR).pack(pady=20)

    text_font = (DEFAULT_FONT_NAME, 24)
    tk.Label(
        window, text=f"Selected option: {option_name}",
        font=text_font, bg=BACKGROUND_COLOR, fg="black"
    ).pack(pady=10)

    controls_frame = tk.Frame(window, bg=BACKGROUND_COLOR)
    controls_frame.pack(pady=20)

    speed_var = tk.DoubleVar(value=1)
    tk.Scale(
        controls_frame, from_=0.1, to=5.0, resolution=0.1, orient="horizontal",
        variable=speed_var, label="Speed", bg=BACKGROUND_COLOR, font=(DEFAULT_FONT_NAME, 16), fg="black",
        troughcolor="#ed5b37", activebackground=BACKGROUND_COLOR, length=300, width=30, sliderlength=40
    ).pack(side="left", padx=40)

    elements_var = tk.IntVar(value=100)
    tk.Scale(
        controls_frame, from_=10, to=1000, resolution=10, orient="horizontal",
        variable=elements_var, label="Elements", bg=BACKGROUND_COLOR, font=(DEFAULT_FONT_NAME, 16), fg="black",
        troughcolor="#375eed", activebackground=BACKGROUND_COLOR, length=300, width=30, sliderlength=40
    ).pack(side="left", padx=40)

    buttons_frame = tk.Frame(window, bg=BACKGROUND_COLOR)
    buttons_frame.pack(pady=80)

    chart_off = PhotoImage(file=os.path.join(BUTTONS_PATH, "btn_graficadora_off.png"))
    chart_on = PhotoImage(file=os.path.join(BUTTONS_PATH, "btn_graficadora_on.png"))
    complexity_off = PhotoImage(file=os.path.join(BUTTONS_PATH, "btn_complejidad_off.png"))
    complexity_on = PhotoImage(file=os.path.join(BUTTONS_PATH, "btn_complejidad_on.png"))

    def open_complexity():
        window.destroy()
        complexity_window(option_name)

    def open_chart():
        window.destroy()
        chart_window(option_name, speed_var.get(), elements_var.get())

    create_standalone_button(buttons_frame, complexity_off, complexity_on, open_complexity, side="left", padx=40)
    create_standalone_button(buttons_frame, chart_off, chart_on, open_chart, side="left", padx=40)

    # Back button
    back_off_image = PhotoImage(file=os.path.join(BUTTONS_PATH, "SBtn_rojo_off.png"))
    back_on_image = PhotoImage(file=os.path.join(BUTTONS_PATH, "SBtn_rojo_on.png"))

    back_frame = tk.Frame(window, bg=BACKGROUND_COLOR)
    back_frame.pack(side="bottom", anchor="w", padx=20, pady=10)

    def go_back():
        window.destroy()
        main_menu()

    create_standalone_button(
        back_frame, back_off_image, back_on_image, go_back,
        text="\u2190 Back", font=(DEFAULT_FONT_NAME, 20), side="left", padx=0, pady=0
    )

    center_window(window)
    window.mainloop()


# =============================================================
# CHART (VISUALIZATION) WINDOW
# =============================================================

def chart_window(option_name, speed, amount):
    vis_window = tk.Tk()
    vis_window.title("Algorithm Visualization")
    vis_window.geometry("1000x470+200+100")
    vis_window.configure(bg=BACKGROUND_COLOR)

    # Shared state between the control functions: "stopped", "running" or "paused".
    state = {"value": "stopped"}

    canvas = tk.Canvas(vis_window, width=980, height=450, bg="white", highlightthickness=0)
    canvas.pack(padx=10, pady=10)

    data = random.sample(range(1, amount + 1), amount)

    def draw_bars(values, colors):
        """Draw the bars on the canvas based on the given values and colors."""
        canvas.delete("all")

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        count = len(values)
        if count == 0:
            return

        bar_width = canvas_width / count
        max_value = max(values) if max(values) != 0 else 1

        for index, value in enumerate(values):
            x0 = int(index * bar_width)
            x1 = int((index + 1) * bar_width)
            y1 = canvas_height
            y0 = int(canvas_height - (value / max_value) * (canvas_height - 50))  # top margin
            canvas.create_rectangle(x0, y0, x1, y1, fill=colors[index], outline="")

        vis_window.update_idletasks()

    draw_bars.canvas = canvas
    draw_bars.state = state

    def start_sorting():
        """Start the selected sorting algorithm."""
        if state["value"] != "stopped":
            return
        state["value"] = "running"
        sort_function = load_sort_function(option_name)
        if sort_function is None:
            return
        sort_function(data, draw_func=draw_bars, delay=speed)

    def pause_resume():
        """Pause or resume the algorithm execution depending on the current state."""
        if state["value"] == "running":
            state["value"] = "paused"
        elif state["value"] == "paused":
            state["value"] = "running"

    def stop():
        """Stop the algorithm execution."""
        state["value"] = "stopped"

    def go_back_to_settings():
        """Close the current windows and go back to the settings screen."""
        control_window.destroy()
        vis_window.destroy()
        settings_window(option_name, None)

    info_text = f"Method: {option_name} | Speed: {speed} | Elements: {amount}"
    info_font = (DEFAULT_FONT_NAME, 20)

    tk.Label(vis_window, text=info_text, font=info_font, fg="black", bg=BACKGROUND_COLOR).pack(side="bottom", pady=5)

    control_window = tk.Toplevel(vis_window)
    control_window.title("Algorithm Controls")
    control_window.geometry("1000x200+200+600")
    control_window.configure(bg=BACKGROUND_COLOR)

    control_title_image = PhotoImage(file=CONTROL_TITLE_PATH)
    control_title_label = tk.Label(control_window, image=control_title_image, bg=BACKGROUND_COLOR)
    control_title_label.image = control_title_image  # keep a reference to avoid garbage collection
    control_title_label.pack(pady=5)

    buttons_info = [
        ("\u2190 Back", go_back_to_settings, "rojo"),
        ("Start", start_sorting, "verde"),
        ("Pause/Resume", pause_resume, "azul"),
        ("Stop", stop, "naranja"),
    ]

    button_images = {}
    for _, _, color in buttons_info:
        off_image = PhotoImage(file=os.path.join(BUTTONS_PATH, f"SBtn_{color}_off.png"))
        on_image = PhotoImage(file=os.path.join(BUTTONS_PATH, f"SBtn_{color}_on.png"))
        button_images[color] = (off_image, on_image)

    buttons_frame = tk.Frame(control_window, bg=BACKGROUND_COLOR)
    buttons_frame.pack(pady=10)

    button_font = (DEFAULT_FONT_NAME, 16)

    for text, action, color in buttons_info:
        off_image, on_image = button_images[color]
        create_standalone_button(
            buttons_frame, off_image, on_image, action,
            text=text, font=button_font, side="left", padx=10, pady=5
        )

    tk.Label(
        control_window, text=info_text, font=info_font, fg="black", bg=BACKGROUND_COLOR
    ).pack(side="bottom", pady=5)

    vis_window.mainloop()


# =============================================================
# COMPLEXITY WINDOW
# =============================================================

def complexity_window(option_name):
    def generate_list(size):
        return (
            random.sample(range(1, size + 1), size)
            if list_type.get() == "random"
            else list(range(size, 0, -1))
        )

    def update_chart():
        ax.clear()
        ax.set_title(f"Complexity of {option_name}")
        ax.set_xlabel("Number of elements")
        ax.set_ylabel("Steps")
        ax.grid(True)
        return ax.plot([], [], color="black", linewidth=2)[0]

    def run_step():
        nonlocal current_size, after_id
        if not running.get():
            after_id = vis_window.after(100, run_step)
            return
        sample_list = generate_list(current_size)
        steps.append(study_function(sample_list.copy()))
        sizes.append(current_size)
        plot_line.set_data(sizes, steps)
        ax.relim()
        ax.autoscale_view()
        canvas.draw()
        current_size += 20
        after_id = vis_window.after(100, run_step)

    def start_analysis(reset=False):
        nonlocal current_size, sizes, steps, plot_line, after_id
        if reset and after_id:
            vis_window.after_cancel(after_id)
        current_size = 20
        sizes.clear()
        steps.clear()
        plot_line = update_chart()
        canvas.draw()
        run_step()

    def change_list_type(new_type):
        list_type.set(new_type)
        start_analysis(reset=True)

    def toggle_pause():
        running.set(not running.get())

    def on_close():
        """Cancel any pending callback and close both windows cleanly."""
        if after_id:
            vis_window.after_cancel(after_id)
        control_window.destroy()
        vis_window.destroy()

    # --- Visualization window ---
    vis_window = tk.Toplevel()
    vis_window.title("Algorithm Steps")
    vis_window.geometry("1000x470+200+100")
    vis_window.configure(bg=BACKGROUND_COLOR)

    figure, ax = plt.subplots(figsize=(7.5, 5))
    figure.patch.set_facecolor(BACKGROUND_COLOR)
    canvas = FigureCanvasTkAgg(figure, master=vis_window)
    canvas.get_tk_widget().pack(pady=10)

    list_type = tk.StringVar(value="random")
    running = tk.BooleanVar(value=True)
    sizes, steps = [], []
    current_size, after_id = 20, None
    plot_line = None

    study_function = load_study_function(option_name)
    if study_function is None:
        vis_window.destroy()
        return

    vis_window.protocol("WM_DELETE_WINDOW", on_close)

    # --- Control window ---
    control_window = tk.Toplevel(vis_window)
    control_window.title("Algorithm Controls")
    control_window.geometry("1000x200+200+600")
    control_window.configure(bg=BACKGROUND_COLOR)

    complexity_title_image = PhotoImage(file=COMPLEXITY_TITLE_PATH)
    title_label = tk.Label(control_window, image=complexity_title_image, bg=BACKGROUND_COLOR)
    title_label.image = complexity_title_image
    title_label.pack(pady=10)

    buttons_frame = tk.Frame(control_window, bg=BACKGROUND_COLOR)
    buttons_frame.pack(pady=10)

    button_font = (DEFAULT_FONT_NAME, 16)

    random_off = PhotoImage(file=os.path.join(BUTTONS_PATH, "SBtn_verde_off.png"))
    random_on = PhotoImage(file=os.path.join(BUTTONS_PATH, "SBtn_verde_on.png"))
    create_standalone_button(
        buttons_frame, random_off, random_on, lambda: change_list_type("random"),
        text="Random", font=button_font, side="left", padx=10
    )

    reverse_off = PhotoImage(file=os.path.join(BUTTONS_PATH, "SBtn_oro_off.png"))
    reverse_on = PhotoImage(file=os.path.join(BUTTONS_PATH, "SBtn_oro_on.png"))
    create_standalone_button(
        buttons_frame, reverse_off, reverse_on, lambda: change_list_type("reverse"),
        text="Reverse", font=button_font, side="left", padx=10
    )

    pause_off = PhotoImage(file=os.path.join(BUTTONS_PATH, "SBtn_azul_off.png"))
    pause_on = PhotoImage(file=os.path.join(BUTTONS_PATH, "SBtn_azul_on.png"))
    create_standalone_button(
        buttons_frame, pause_off, pause_on, toggle_pause,
        text="Pause/Resume", font=button_font, side="left", padx=10
    )

    tk.Label(
        control_window,
        text="| Close the window above to remove this one |",
        font=(DEFAULT_FONT_NAME, 16), fg="black", bg=BACKGROUND_COLOR
    ).pack(pady=10)

    vis_window.mainloop()