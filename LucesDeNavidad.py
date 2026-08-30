import tkinter as tk
import time

NUM_CIRCLES = 7
CIRCLE_RADIUS = 40
CANVAS_SIZE = NUM_CIRCLES * (CIRCLE_RADIUS * 2 + 10)
INTERVAL_MS = 500
is_running = False
current_index = 0

root = tk.Tk()
root.title("🎄 Luces De Navidad 🎄")

canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE//2, bg='black')
canvas.pack(pady=20)

circles = []
colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'orange']
for i in range(NUM_CIRCLES):
    x = CIRCLE_RADIUS + 10 + i * (CIRCLE_RADIUS * 2 + 10)
    y = CIRCLE_RADIUS + 10
    circle_id = canvas.create_oval(x - CIRCLE_RADIUS, y - CIRCLE_RADIUS,
                                   x + CIRCLE_RADIUS, y + CIRCLE_RADIUS,
                                   fill=colors[i % len(colors)], outline='white', width=2)
    circles.append(circle_id)


def update_lights():
    """Actualiza la intensidad de las luces para el efecto de onda."""
    global current_index
    if not is_running:
        return  # Si está detenido, no hace nada

    # 1. Restaurar la intensidad de la luz anterior
    prev_index = (current_index - 1) % NUM_CIRCLES
    canvas.itemconfig(circles[prev_index], fill=colors[prev_index % len(colors)])

    # 2. Aumentar la intensidad de la luz actual (ponerla más brillante/oscura?)
    # Para simplificar, la pondremos de color blanco para simular "más intensidad"
    canvas.itemconfig(circles[current_index], fill='white')

    # 3. Avanzar al siguiente índice
    current_index = (current_index + 1) % NUM_CIRCLES

    # 4. Programar la siguiente actualización
    root.after(INTERVAL_MS, update_lights)

def toggle_lights():
    """Inicia o detiene el efecto de las luces."""
    global is_running
    is_running = not is_running  # Cambia el estado
    if is_running:
        start_stop_btn.config(text="Detener")
        # Asegura que el ciclo empiece desde el primer círculo
        global current_index
        current_index = 0
        # Reinicia los colores antes de empezar
        for i, cid in enumerate(circles):
            canvas.itemconfig(cid, fill=colors[i % len(colors)])
        update_lights()  # Inicia el ciclo
    else:
        start_stop_btn.config(text="Iniciar")
        # Opcional: restaurar todos los círculos a su color base
        for i, cid in enumerate(circles):
            canvas.itemconfig(cid, fill=colors[i % len(colors)])

def change_speed(val):
    """Cambia la velocidad del efecto."""
    global INTERVAL_MS
    # El slider devuelve un string, lo convertimos a int
    INTERVAL_MS = int(val)
    speed_label.config(text=f"Velocidad: {INTERVAL_MS}ms")

# --- Crear los controles (Botones y Sliders) ---
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

start_stop_btn = tk.Button(control_frame, text="Iniciar", command=toggle_lights, width=10, height=2)
start_stop_btn.grid(row=0, column=0, padx=10)

speed_scale = tk.Scale(control_frame, from_=100, to=1000, orient=tk.HORIZONTAL,
                       label="Velocidad (ms)", command=change_speed)
speed_scale.set(INTERVAL_MS)  # Valor por defecto
speed_scale.grid(row=0, column=1, padx=10)

speed_label = tk.Label(control_frame, text=f"Velocidad: {INTERVAL_MS}ms")
speed_label.grid(row=0, column=2, padx=10)

# --- Iniciar el bucle principal de Tkinter ---
root.mainloop()