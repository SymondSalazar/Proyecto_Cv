import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class RiemannSumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Longitud de Arco - Suma de Riemann")
        self.root.geometry("1000x700")
        self.root.configure(bg="#FFFFFF")

        # Configurar estilo minimalista moderno
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configurar estilos con Montserrat y esquema blanco/negro
        self.style.configure(
            "TFrame", background="#FFFFFF", relief="flat", borderwidth=0
        )

        self.style.configure(
            "Title.TLabel",
            background="#FFFFFF",
            foreground="#000000",
            font=("Montserrat", 18, "bold"),
        )

        self.style.configure(
            "Heading.TLabel",
            background="#FFFFFF",
            foreground="#000000",
            font=("Montserrat Medium", 12),
        )

        self.style.configure(
            "Body.TLabel",
            background="#FFFFFF",
            foreground="#000000",
            font=("Montserrat", 10),
        )

        self.style.configure(
            "Modern.TButton",
            background="#FFFFFF",
            foreground="#000000",
            font=("Montserrat SemiBold", 11),
            borderwidth=2,
            relief="solid",
            padding=(20, 10),
        )

        self.style.map(
            "Modern.TButton",
            background=[("active", "#F5F5F5"), ("pressed", "#E0E0E0")],
            relief=[("pressed", "solid"), ("!pressed", "solid")],
        )

        self.style.configure(
            "Modern.TEntry",
            fieldbackground="#FFFFFF",
            foreground="#000000",
            borderwidth=2,
            relief="solid",
            insertcolor="#000000",
            font=("Montserrat", 10),
        )

        self.style.configure(
            "Modern.TLabelframe", background="#FFFFFF", borderwidth=2, relief="solid"
        )

        self.style.configure(
            "Modern.TLabelframe.Label",
            background="#FFFFFF",
            foreground="#000000",
            font=("Montserrat Medium", 11),
        )

        # Crear marco principal
        main_frame = ttk.Frame(root, padding=30, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(
            main_frame, text="Proyecto Calculo Vectorial", style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # Panel de entrada de datos
        input_frame = ttk.LabelFrame(
            main_frame, text="Parámetros de Entrada", style="Modern.TLabelframe"
        )
        input_frame.grid(row=1, column=0, padx=(0, 15), pady=(0, 20), sticky="nsew")
        input_frame.configure(padding=20)

        # Entrada para 'a'
        ttk.Label(
            input_frame, text="Radio del cilindro (a cm):", style="Body.TLabel"
        ).grid(row=0, column=0, padx=(0, 10), pady=(0, 15), sticky="w")
        self.a_entry = ttk.Entry(input_frame, width=20, style="Modern.TEntry")
        self.a_entry.grid(row=0, column=1, padx=0, pady=(0, 15), sticky="ew")
        self.a_entry.insert(0, "1.0")

        # Entrada para número de subintervalos
        ttk.Label(
            input_frame, text="Número de subintervalos (N):", style="Body.TLabel"
        ).grid(row=1, column=0, padx=(0, 10), pady=(0, 20), sticky="w")
        self.n_entry = ttk.Entry(input_frame, width=20, style="Modern.TEntry")
        self.n_entry.grid(row=1, column=1, padx=0, pady=(0, 20), sticky="ew")
        self.n_entry.insert(0, "1000")

        # Configurar expansión de columnas en input_frame
        input_frame.columnconfigure(1, weight=1)

        # Botón de cálculo
        self.calc_button = ttk.Button(
            input_frame,
            text="Calcular Longitud",
            command=self.calculate_length,
            style="Modern.TButton",
        )
        self.calc_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # Panel de resultados
        result_frame = ttk.LabelFrame(
            main_frame, text="Resultados", style="Modern.TLabelframe"
        )
        result_frame.grid(row=1, column=1, padx=(15, 0), pady=(0, 20), sticky="nsew")
        result_frame.configure(padding=20)

        self.result_text = tk.Text(
            result_frame,
            height=6,
            width=45,
            bg="#FFFFFF",
            fg="#000000",
            font=("Montserrat", 10),
            relief=tk.SOLID,
            borderwidth=2,
            wrap=tk.WORD,
            padx=15,
            pady=15,
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.insert(
            tk.END, "Los resultados aparecerán aquí después del cálculo..."
        )
        self.result_text.config(state=tk.DISABLED)

        # Área de gráficos
        graph_frame = ttk.LabelFrame(
            main_frame, text="Visualización 3D", style="Modern.TLabelframe"
        )
        graph_frame.grid(
            row=2, column=0, columnspan=2, padx=0, pady=(0, 0), sticky="nsew"
        )
        graph_frame.configure(padding=20)

        self.fig = Figure(figsize=(10, 6), dpi=100, facecolor="#FFFFFF")
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.set_facecolor("#FFFFFF")

        # Configurar colores del gráfico 3D para mantener contraste
        try:
            self.ax.xaxis.pane.fill = False
            self.ax.yaxis.pane.fill = False
            self.ax.zaxis.pane.fill = False
        except Exception:
            pass  # En caso de que la versión de matplotlib no soporte estas propiedades

        self.ax.tick_params(colors="#000000", labelsize=9)
        self.ax.xaxis.label.set_color("#000000")
        self.ax.yaxis.label.set_color("#000000")
        try:
            self.ax.zaxis.label.set_color("#000000")
        except Exception:
            pass  # En caso de problemas con zaxis

        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Configurar expansión de columnas
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

    def calculate_length(self):
        try:
            a = float(self.a_entry.get())
            N = int(self.n_entry.get())

            if a <= 0 or N <= 0:
                raise ValueError("Valores deben ser positivos")

            # Parámetro t de 0 a 2π
            t = np.linspace(0, 2 * np.pi, N + 1)
            dt = t[1] - t[0]  # Tamaño del subintervalo

            # Parametrización de la curva
            x = a * np.cos(t)
            y = a * np.sin(t)
            z = (8 - x - y) / 2

            # Derivadas numéricas usando diferencias finitas
            dx_dt = np.gradient(x, dt)
            dy_dt = np.gradient(y, dt)
            dz_dt = np.gradient(z, dt)

            # Norma del vector derivada
            norm_r_prime = np.sqrt(dx_dt**2 + dy_dt**2 + dz_dt**2)

            # Suma de Riemann (aproximación por la izquierda)
            riemann_sum = np.sum(norm_r_prime[:-1] * dt)

            # Actualizar resultados
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)

            # Crear un formato más elegante para los resultados
            result_content = f"""PARÁMETROS UTILIZADOS
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Radio del cilindro (a): {a:.4f} cm
• Número de subintervalos (N): {N:,}

RESULTADO DEL CÁLCULO
━━━━━━━━━━━━━━━━━━━━━━━━━━
Longitud aproximada: {riemann_sum:.6f} cm

La curva de intersección entre el cilindro 
x² + y² = {a}² y el plano x + y + 2z = 8 
tiene una longitud aproximada de 
{riemann_sum:.4f} centímetros."""

            self.result_text.insert(tk.END, result_content)
            self.result_text.config(state=tk.DISABLED)

            # Actualizar gráfico
            self.update_plot(x, y, z, a)

        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def update_plot(self, x, y, z, a):
        self.ax.clear()

        # Curva de intersección - usamos un color que contraste bien con fondo blanco
        self.ax.plot(x, y, z, "#FF6B35", linewidth=3, label="Curva de intersección")

        # Cilindro - color azul semitransparente
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(min(z) - 1, max(z) + 1, 50)
        U, V = np.meshgrid(u, v)
        X_cyl = a * np.cos(U)
        Y_cyl = a * np.sin(U)
        Z_cyl = V
        self.ax.plot_surface(
            X_cyl, Y_cyl, Z_cyl, color="#4A90E2", alpha=0.3, label="Cilindro"
        )

        # Plano - color verde semitransparente
        x_plane = np.linspace(-a * 1.5, a * 1.5, 20)
        y_plane = np.linspace(-a * 1.5, a * 1.5, 20)
        X_plane, Y_plane = np.meshgrid(x_plane, y_plane)
        Z_plane = (8 - X_plane - Y_plane) / 2
        self.ax.plot_surface(
            X_plane, Y_plane, Z_plane, color="#7ED321", alpha=0.3, label="Plano"
        )

        # Configurar el gráfico con colores para fondo blanco
        self.ax.set_xlabel("X", fontsize=11, color="#000000")
        self.ax.set_ylabel("Y", fontsize=11, color="#000000")
        try:
            self.ax.set_zlabel("Z", fontsize=11, color="#000000")
        except Exception:
            pass  # En caso de problemas con set_zlabel

        self.ax.set_title(
            f"Intersección: Cilindro $x^2 + y^2 = {a}^2$ y Plano $x + y + 2z = 8$",
            fontsize=12,
            fontweight="bold",
            color="#000000",
            pad=20,
        )

        # Configurar la leyenda
        legend = self.ax.legend(loc="upper right", fontsize=10)
        legend.get_frame().set_facecolor("#FFFFFF")
        legend.get_frame().set_edgecolor("#000000")

        # Configurar grid con color apropiado
        self.ax.grid(True, linestyle="--", alpha=0.5, color="#CCCCCC")

        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = RiemannSumApp(root)
    root.mainloop()
