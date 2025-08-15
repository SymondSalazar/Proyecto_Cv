import numpy as np
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def calcular_longitud():
    try:
        # Leer datos de la interfaz
        a = float(entry_a.get())
        N = int(entry_n.get())

        # Intervalo del parámetro t
        t_inicial = 0
        t_final = 2 * np.pi
        t = np.linspace(t_inicial, t_final, N + 1)

        # Parametrización de la curva
        x = a * np.cos(t)
        y = a * np.sin(t)
        z = (8 - a * np.cos(t) - a * np.sin(t)) / 2

        # Derivadas numéricas usando diferencias centradas (numpy.gradient)
        dx_dt = np.gradient(x, t)
        dy_dt = np.gradient(y, t)
        dz_dt = np.gradient(z, t)

        # Norma de r'(t)
        velocidad = np.sqrt(dx_dt**2 + dy_dt**2 + dz_dt**2)

        # Suma de Riemann por la izquierda
        delta_t = (t_final - t_inicial) / N
        longitud = np.sum(velocidad[:-1] * delta_t)

        # Mostrar resultado
        resultado.set(f"Longitud aproximada: {longitud:.4f} cm")

    except ValueError:
        resultado.set("Error: ingrese valores numéricos válidos.")


# ---- Interfaz gráfica con ttkbootstrap ----
app = ttk.Window(themename="cyborg")
app.title("Cálculo de Longitud de Curva")
app.geometry("400x300")

ttk.Label(app, text="Cálculo Longitud de Arco", font=("Helvetica", 16, "bold")).pack(
    pady=10
)

frame = ttk.Frame(app)
frame.pack(pady=10)

# Entrada valor de a
ttk.Label(frame, text="Valor de a (cm):").grid(
    row=0, column=0, padx=5, pady=5, sticky=E
)
entry_a = ttk.Entry(frame)
entry_a.grid(row=0, column=1, padx=5, pady=5)

# Entrada número de subintervalos
ttk.Label(frame, text="Número de subintervalos:").grid(
    row=1, column=0, padx=5, pady=5, sticky=E
)
entry_n = ttk.Entry(frame)
entry_n.grid(row=1, column=1, padx=5, pady=5)

# Botón de cálculo
ttk.Button(app, text="Calcular", command=calcular_longitud, bootstyle=SUCCESS).pack(
    pady=10
)

# Resultado
resultado = ttk.StringVar()
ttk.Label(app, textvariable=resultado, font=("Helvetica", 12)).pack(pady=10)

app.mainloop()
