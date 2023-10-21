from rocV import rocV
from rocPD import rocPD
from rocFB import rocFB
from ManejoArchivos import leer_archivo, escribir_archivo
from pathlib import Path
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

# Variable para almacenar los datos del problema
datos = None
resultado = None
ruta = None
nombre_archivo = None


def abrir_archivo() -> str:
    tipos_archivo = [("Archivos ROC", "*.roc"), ("Archivos TXT", "*.txt")]
    # Abrimos el diálogo para seleccionar el archivo
    ruta_archivo = filedialog.askopenfilename(
        defaultextension=".roc", filetypes=tipos_archivo
    )

    return ruta_archivo


def capa_datos():
    global datos
    global ruta
    global nombre_archivo
    ruta = abrir_archivo()
    nombre_archivo = os.path.basename(ruta)
    label_nombre_archivo.config(text=f"Nombre del Archivo: {nombre_archivo}")
    datos = leer_archivo(ruta)

    with open(ruta, "r") as entrada:
        contenido = entrada.read()
        texto_entrada.config(state="normal")
        texto_entrada.delete(1.0, tk.END)
        texto_entrada.insert(tk.END, contenido)
        texto_entrada.config(state="disabled")


def escribir_salida(archivo: str, algoritmo: str):
    dato = archivo.split(".")
    ruta_salida = Path(__file__).parent / f"Salidas/{dato[0]}_{algoritmo}.{dato[1]}"
    with open(ruta_salida, "r") as salida:
        contenido = salida.read()
        texto_salida.config(state="normal")
        texto_salida.delete(1.0, tk.END)
        texto_salida.insert(tk.END, contenido)
        texto_salida.config(state="disabled")


def capa_rocFB():
    global datos, resultado, nombre_archivo
    try:
        resultado = rocFB(datos[0], datos[1], datos[2], datos[3])
        print(resultado[0])
        mostrar_resultados(resultado[0], resultado[1])
        escribir_archivo(nombre_archivo, resultado[0], resultado[1], "rocFB")
        escribir_salida(nombre_archivo, "rocFB")
    except MemoryError:
        messagebox.showerror(
            "Out of Memory",
            "Se acabó la memoria disponible, no se pudo resolver el problema",
        )


def capa_rocV():
    global datos, resultado, nombre_archivo
    try:
        rocV_datos = (datos[2], datos[3])
        resultado = rocV(rocV_datos)
        print(resultado)
        mostrar_resultados(resultado[0], resultado[1])
        escribir_archivo(nombre_archivo, resultado[0], resultado[1], "rocV")
        escribir_salida(nombre_archivo, "rocV")
    except MemoryError:
        messagebox.showerror(
            "Out of Memory",
            "Se acabó la memoria disponible, no se pudo resolver el problema",
        )


def capa_rocPD():
    global datos, resultado, nombre_archivo
    try:
        resultado = rocPD(datos[0], datos[1], datos[2], datos[3])
        print(resultado[0])
        mostrar_resultados(resultado[0], resultado[1])
        escribir_archivo(nombre_archivo, resultado[0], resultado[1], "rocPD")
        escribir_salida(nombre_archivo, "rocPD")
    except MemoryError:
        messagebox.showerror(
            "Out of Memory",
            "Se acabó la memoria disponible, no se pudo resolver el problema",
        )


def mostrar_resultados(resultados: dict, insatisfaccion: float):
    ventana_resultados = tk.Toplevel(ventana)
    ventana_resultados.resizable(width=0, height=0)
    WIDTH = 420
    HEIGHT = 250

    x = int((ventana_resultados.winfo_screenwidth() / 2) - (WIDTH / 2))
    y = int((ventana_resultados.winfo_screenheight() / 3) - (HEIGHT / 2))

    ventana_resultados.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

    ventana_resultados.title("Resultados")
    tree_resultados = ttk.Treeview(
        ventana_resultados, columns=("Estudiantes", "Asignatura"), selectmode="browse"
    )
    tree_resultados.pack(side="left")

    scrollbar = ttk.Scrollbar(
        ventana_resultados, orient="vertical", command=tree_resultados.yview
    )
    scrollbar.pack(side="right", fill="y")

    tree_resultados.configure(yscrollcommand=scrollbar.set)

    tree_resultados["columns"] = ("1", "2")
    tree_resultados["show"] = "headings"
    tree_resultados.column("1", width=200, anchor="center")
    tree_resultados.column("2", width=200, anchor="center")

    tree_resultados.heading("#1", text="Estudiantes")
    tree_resultados.heading("#2", text="Asignatura")

    # Insertar los datos en el Treeview
    for estudiante, asignaciones in resultados.items():
        codigos_materias = []
        for asignacion in asignaciones:
            codigos_materias.append(asignacion[0])
        # asignatura_str = ", ".join(asignatura)
        tree_resultados.insert("", "end", values=(estudiante, codigos_materias))

    tree_resultados.insert("", "end", values=("Insatisfacción", insatisfaccion))

    tree_resultados.pack()


ventana = tk.Tk()

WIDTH = 350
HEIGHT = 600

x = int((ventana.winfo_screenwidth() / 2) - (WIDTH / 2))
y = int((ventana.winfo_screenheight() / 2) - (HEIGHT / 2))

ventana.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
ventana.title("Repartición Óptima de Cupos")

advertencia = tk.Label(text="Repartición Óptima de Cupos", padx=10)
advertencia.pack()

frame = tk.Frame(ventana, padx=10, pady=5)
frame.pack()

frame_cargar_datos = tk.LabelFrame(frame, text="Entrada", padx=10, pady=5)
frame_cargar_datos.grid(row=0, column=0)

boton_cargar = tk.Button(frame_cargar_datos, text="Cargar Datos", command=capa_datos)
boton_cargar.grid(row=0, column=0)

label_nombre_archivo = tk.Label(frame_cargar_datos, text="Nombre del Archivo: ")
label_nombre_archivo.grid(row=1, column=0)

label_advertencia_algoritmo = tk.Label(
    frame,
    text="Seleccione el algoritmo a usar:",
)
label_advertencia_algoritmo.grid(row=1, column=0)

frame_seleccionar_algoritmo = tk.LabelFrame(
    frame, text="Tipo de Algoritmo", padx=10, pady=5
)
frame_seleccionar_algoritmo.grid(row=2, column=0)

boton_fb = tk.Button(
    frame_seleccionar_algoritmo, text="Algoritmo\nFuerza Bruta", command=capa_rocFB
)
boton_fb.grid(row=0, column=0, padx=0, pady=0)

boton_voraz = tk.Button(
    frame_seleccionar_algoritmo, text="Algoritmo\nVoráz", command=capa_rocV
)
boton_voraz.grid(row=0, column=1)

boton_dinamica = tk.Button(
    frame_seleccionar_algoritmo, text="Programación\nDinámica", command=capa_rocPD
)
boton_dinamica.grid(row=0, column=2)

frame_texto_entrada = tk.LabelFrame(frame, text="Entrada del Problema")
frame_texto_entrada.grid(row=3, column=0)

texto_entrada = ScrolledText(frame_texto_entrada, width=30, height=10)
texto_entrada.insert(tk.END, "Acá se muestran\nlos datos de entrada")
texto_entrada.grid(row=0, column=0, padx=10, pady=5)

frame_texto_salida = tk.LabelFrame(frame, text="Salida del Problema")
frame_texto_salida.grid(row=4, column=0)

texto_salida = ScrolledText(frame_texto_salida, width=30, height=10)
texto_salida.insert(tk.END, "Acá se muestran\nlos datos de salida")
texto_salida.grid(row=0, column=0, padx=10, pady=5)

ventana.mainloop()
