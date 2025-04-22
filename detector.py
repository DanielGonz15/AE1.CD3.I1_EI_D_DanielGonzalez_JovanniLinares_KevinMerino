import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from playsound import playsound
from keras.models import load_model
import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
import os

# Cargar el modelo .h5
model = load_model('modelo/modeloCNN8D.h5')
pesos = "modelo/pesos.weights.h5"
model.load_weights(pesos)

# Las clases de salida (ajústalo según tu entrenamiento)
clases = ['Cara billete 20','Cara billete 100','Cara billete 200', 'Cara billete 50','Cara billete 500', 'Cruz billete 20','Cruz billete 100','Cruz billete 200','Cruz billete 50' ,'Cruz billete 500']
# Sonidos
sonidos_billetes = {
    'Cara billete 20': 'sonidos/cara20.wav',
    'Cara billete 100': 'sonidos/cara100.wav',
    'Cara billete 200': 'sonidos/cara200.wav',
    'Cara billete 50': 'sonidos/cara50.wav',
    'Cara billete 500': 'sonidos/cara500.wav',
    'Cruz billete 20': 'sonidos/cara20.wav',
    'Cruz billete 100': 'sonidos/cara100.wav',
    'Cruz billete 200': 'sonidos/cara200.wav',
    'Cruz billete 50': 'sonidos/cara50.wav',
    'Cruz billete 500': 'sonidos/cara500.wav',
    '':''
}
# Evitar que el sonido se repita continuamente
ultima_clasificacion = None
tiempo_ultima = 0
intervalo_sonido = 4  # segundos
correr = False
global cap 
cap = cv2.VideoCapture(0)


def reproducir_sonido(clasificacion):
    ruta = sonidos_billetes.get(clasificacion)
    if ruta:
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"❌ Error al reproducir {ruta}: {e}")
    else:
        print(f"⚠️ No se encontró la ruta para la clasificación '{clasificacion}'")
def cerrar_ventana():
    global correr
    correr = False
    ventana.destroy()
def predecir_desde_ruta():
    ruta = entry_ruta.get()
    try:
        #Transformar la imagen a clasificar
        imagen = cv2.imread(ruta)
        imagen = load_img(ruta, target_size=(150,150))
        imagen = img_to_array(imagen)
        imagen = np.expand_dims(imagen, axis=0) / 255.0
        #Predecir
        resultado = model.predict(imagen)
        print(resultado)
        max = np.argmax(resultado)
        clase = clases[np.argmax(resultado)]
        confianza = resultado[0][max]
        if confianza > 0.8:
            lbl_resultado.config(text=f"{clase}")
            img_display = Image.open(ruta).resize((250, 250))
            img_tk = ImageTk.PhotoImage(img_display)
            lbl_img.configure(image=img_tk)
            lbl_img.image = img_tk
        else:
            lbl_resultado.config(text=f"No se reconoce el billete")
            img_display = Image.open(ruta).resize((250, 250))
            img_tk = ImageTk.PhotoImage(img_display)
            lbl_img.configure(image=img_tk)
            lbl_img.image = img_tk      

    except Exception as e:
        lbl_resultado.config(text=f"Error: {e}")
def actualizar_frame():
    global correr
    if not correr:
        cap.release()
        return
    ret, frame = cap.read()
    if not ret:
        return
    
    # Dibujar una zona de interés (ROI)
    x, y, w, h = 130, 100, 400, 200  # puedes ajustar estos valores
    roi = frame[y:y+h, x:x+w]
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Preprocesar solo la zona de interés
    imagen = cv2.resize(roi, (150,150))
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    imagen = img_to_array(imagen)
    imagen = np.expand_dims(imagen, axis=0)
    imagen = imagen / 255.0
    #imagen = np.expand_dims(imagen, axis=0)
    # Predicción
    resultado = model.predict(imagen)
    max_index = np.argmax(resultado)
    confianza = resultado[0][max_index]
    clase_detectada=''
    # Mostrar solo si la confianza supera 90%
    if confianza > 0.9:
        clase_detectada = clases[max_index]
        print(f"Detectado: {clase_detectada} ({confianza:.2f})")
        cv2.putText(frame, f'{clase_detectada} ({confianza:.2f})', (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        print("No se detecta billete con suficiente confianza")

    # Reproducir sonido si ha pasado suficiente tiempo
    tiempo_actual = time.time()
    global ultima_clasificacion, tiempo_ultima
    if clase_detectada != ultima_clasificacion or (tiempo_actual - tiempo_ultima > intervalo_sonido):
        if clase_detectada in sonidos_billetes:
            reproducir_sonido(clase_detectada)
            ultima_clasificacion = clase_detectada
            tiempo_ultima = tiempo_actual
    # Convertir a imagen para tkinter
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    imgtk = ImageTk.PhotoImage(image=img)

    lbl_video.imgtk = imgtk
    lbl_video.configure(image=imgtk)
    lbl_video.after(10, actualizar_frame)
# Función para cerrar ventana
def cerrar_ventana():
    global correr
    correr = False
    ventana.destroy()

# Cambiar de frame
def mostrar_frame(frame):
    global correr
    frame.tkraise()
    if frame == frame_camara:
        correr = True
        cap.open(0)  # Reabrir en caso de que se haya cerrado
        actualizar_frame()
    else:
        correr = False

# Ventana principal
ventana = tk.Tk()
ventana.title("Detector de Billetes")
ventana.geometry("700x600")

# Frames
frame_inicio = tk.Frame(ventana)
frame_inicio.place(relx=0.5, rely=0.5, anchor='center')
frame_camara = tk.Frame(ventana)
frame_camara.place(relx=0.5, rely=0.5, anchor='center')
frame_carga = tk.Frame(ventana)
frame_carga.place(relx=0.5, rely=0.5, anchor='center')
frame_carga.grid(row=0, column=0, sticky='nsew')


for frame in (frame_inicio, frame_camara, frame_carga):
    frame.grid(row=0, column=0, sticky='nsew')
def mostrar_frame(frame):
    frame.tkraise()
#frame video
lbl_video = tk.Label(frame_camara)
lbl_video.pack(pady=10)
#frame carga
lbl_img = tk.Label(frame_carga)
lbl_img.pack()
# Entrada de ruta
label = tk.Label(frame_carga, text="Ruta de la imagen")
label.pack(pady=10)
entry_ruta = tk.Entry(frame_carga, width=50)
entry_ruta.pack(pady=20)

# Etiqueta para mostrar la imagen
lbl_img = tk.Label(frame_carga)
lbl_img.pack()
lbl_resultado = tk.Label(frame_carga, text="", font=("Arial", 14))
lbl_resultado.pack(pady=10)
#boton para mostrar resultado
btn_predecir = tk.Button(frame_carga, text="Predecir Imagen", command=predecir_desde_ruta)
btn_predecir.pack(pady=10)

# Botón de regreso al inicio
def regresar_al_inicio():
    global correr
    correr = False
    cap.release()
    mostrar_frame(frame_inicio)
    
btn_regresar = tk.Button(frame_camara, text="Regresar al inicio", command=regresar_al_inicio)
btn_regresar.pack()

btn_regresar = tk.Button(frame_carga, text="Regresar al inicio", command=regresar_al_inicio)
btn_regresar.pack()
def abrir_camara():
    global correr
    correr = True
    global cap 
    cap = cv2.VideoCapture(0)
    mostrar_frame(frame_camara)
    actualizar_frame()
def abrir_imagen():
    mostrar_frame(frame_carga)
    
# Botones en frame_inicio
titulo = tk.Label(frame_inicio, text="Detector de Billetes", font=("Arial", 18))
titulo.pack(pady=20)

btn_camara = tk.Button(frame_inicio, text="Detección con cámara", font=("Arial", 14), command=abrir_camara)
btn_camara.pack(pady=20)

btn_imagen = tk.Button(frame_inicio, text="Detección Por imagen", font=("Arial", 14), command=abrir_imagen)
btn_imagen.pack(pady=20)

btn_salir = tk.Button(frame_inicio, text="Salir", command=cerrar_ventana)
btn_salir.pack(pady=10)

# Iniciar en el menú principal
mostrar_frame(frame_inicio)
ventana.mainloop()
