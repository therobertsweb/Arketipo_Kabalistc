#!/usr/bin/env python3
# Interfaz gráfica mejorada para Arquetipo (Tkinter)
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import datetime

try:
    # Importamos las funciones principales del script existente
    from Arquetipo_2 import generar_informe_kabalista
except Exception:
    generar_informe_kabalista = None

# Intentamos usar tkcalendar.DateEntry para un selector de fecha más amigable
HAVE_TKCAL = False
try:
    from tkcalendar import DateEntry
    HAVE_TKCAL = True
except Exception:
    HAVE_TKCAL = False


def validar_fecha(fecha_str):
    """Acepta DD/MM/AAAA o AAAA-MM-DD"""
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(fecha_str.strip(), fmt)
        except Exception:
            continue
    return None


class DateFallback(ttk.Frame):
    """Fallback: tres comboboxes para día, mes y año si no está tkcalendar."""
    def __init__(self, master=None, start_year=1900, end_year=None, **kw):
        super().__init__(master, **kw)
        if end_year is None:
            end_year = datetime.date.today().year

        self.day_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.year_var = tk.StringVar()

        days = [str(i) for i in range(1, 32)]
        months = [str(i) for i in range(1, 13)]
        years = [str(i) for i in range(end_year, start_year - 1, -1)]

        self.cb_day = ttk.Combobox(self, values=days, width=4, textvariable=self.day_var)
        self.cb_month = ttk.Combobox(self, values=months, width=4, textvariable=self.month_var)
        self.cb_year = ttk.Combobox(self, values=years, width=6, textvariable=self.year_var)

        self.cb_day.grid(column=0, row=0, padx=(0, 4))
        self.cb_month.grid(column=1, row=0, padx=(0, 4))
        self.cb_year.grid(column=2, row=0)

    def get(self):
        d = self.day_var.get()
        m = self.month_var.get()
        y = self.year_var.get()
        if not (d and m and y):
            return None
        try:
            dt = datetime.date(int(y), int(m), int(d))
            return dt
        except Exception:
            return None


class ArquetipoGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Arquetipo Kabalista — Interfaz")
        self.geometry("820x560")

        # Estilo
        style = ttk.Style(self)
        try:
            style.theme_use('clam')
        except Exception:
            pass

        container = ttk.Frame(self, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        header = ttk.Label(container, text="Informe de Arquetipo y Tikkun", font=(None, 14, 'bold'))
        header.grid(column=0, row=0, columnspan=4, sticky=tk.W)

        ttk.Separator(container, orient=tk.HORIZONTAL).grid(column=0, row=1, columnspan=4, sticky='ew', pady=8)

        # Nombre
        ttk.Label(container, text="Nombre completo:").grid(column=0, row=2, sticky=tk.W, pady=4)
        self.nombre_var = tk.StringVar()
        ttk.Entry(container, textvariable=self.nombre_var, width=60).grid(column=1, row=2, columnspan=3, sticky=tk.W)

        # Fecha
        ttk.Label(container, text="Fecha de nacimiento:").grid(column=0, row=3, sticky=tk.W, pady=4)
        if HAVE_TKCAL:
            self.date_widget = DateEntry(container, date_pattern='dd/MM/yyyy')
            self.date_widget.grid(column=1, row=3, sticky=tk.W)
        else:
            self.date_widget = DateFallback(container)
            self.date_widget.grid(column=1, row=3, sticky=tk.W)

        # Buttons
        btn_generate = ttk.Button(container, text="Generar informe", command=self.on_generar)
        btn_generate.grid(column=2, row=3, sticky=tk.W, padx=(8, 0))

        btn_copy = ttk.Button(container, text="Copiar al portapapeles", command=self.on_copiar)
        btn_copy.grid(column=3, row=3, sticky=tk.W)

        # Area de texto
        self.txt = ScrolledText(container, wrap=tk.WORD, width=96, height=24)
        self.txt.grid(column=0, row=4, columnspan=4, pady=(12, 0))

        # Bottom buttons
        btn_frame = ttk.Frame(container)
        btn_frame.grid(column=0, row=5, columnspan=4, pady=(8, 0), sticky=tk.W)
        ttk.Button(btn_frame, text="Guardar informe...", command=self.on_guardar).grid(column=0, row=0, padx=(0, 8))
        ttk.Button(btn_frame, text="Limpiar", command=self.on_limpiar).grid(column=1, row=0, padx=(0, 8))
        ttk.Button(btn_frame, text="Salir", command=self.destroy).grid(column=2, row=0)

        # status bar
        self.status_var = tk.StringVar(value="Listo")
        status = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status.pack(side=tk.BOTTOM, fill=tk.X)

    def _get_fecha_str(self):
        if HAVE_TKCAL:
            # DateEntry returns datetime.date
            dt = self.date_widget.get_date()
            return dt.strftime('%d/%m/%Y')
        else:
            dt = self.date_widget.get()
            if dt is None:
                return ''
            return dt.strftime('%d/%m/%Y')

    def on_generar(self):
        nombre = self.nombre_var.get().strip()
        fecha = self._get_fecha_str().strip()

        if not nombre:
            messagebox.showwarning("Falta nombre", "Por favor ingresa un nombre completo.")
            return

        if not fecha or validar_fecha(fecha) is None:
            messagebox.showwarning("Fecha inválida", "Selecciona o ingresa la fecha en formato válido.")
            return

        if generar_informe_kabalista is None:
            messagebox.showerror("Error de importación", "No se pudo importar funciones desde Arquetipo_2.py. Revisa el módulo y vuelve a intentar.")
            return

        try:
            self.status_var.set("Generando informe...")
            self.update_idletasks()
            informe = generar_informe_kabalista(nombre, fecha)
        except Exception as e:
            messagebox.showerror("Error al generar", f"Ocurrió un error al generar el informe:\n{e}")
            self.status_var.set("Error")
            return

        self.txt.delete(1.0, tk.END)
        self.txt.insert(tk.END, informe)
        self.status_var.set("Informe generado")

    def on_guardar(self):
        contenido = self.txt.get(1.0, tk.END).strip()
        if not contenido:
            messagebox.showinfo("Sin contenido", "No hay informe para guardar.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt"), ("All files","*.*")])
        if not ruta:
            return
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)
            messagebox.showinfo("Guardado", f"Informe guardado en:\n{ruta}")
            self.status_var.set(f"Guardado: {ruta}")
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudo guardar el archivo:\n{e}")
            self.status_var.set("Error al guardar")

    def on_limpiar(self):
        self.txt.delete(1.0, tk.END)
        self.status_var.set("Listo")

    def on_copiar(self):
        contenido = self.txt.get(1.0, tk.END).strip()
        if not contenido:
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(contenido)
            messagebox.showinfo("Portapapeles", "Informe copiado al portapapeles.")
            self.status_var.set("Copiado al portapapeles")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar al portapapeles:\n{e}")
            self.status_var.set("Error copiar")


if __name__ == "__main__":
    app = ArquetipoGUI()
    app.mainloop()
