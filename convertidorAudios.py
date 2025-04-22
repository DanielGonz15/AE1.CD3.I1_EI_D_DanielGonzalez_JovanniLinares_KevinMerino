import pyttsx3

# Crear motor de voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Velocidad
engine.setProperty('voice', 'spanish')  # Puedes cambiar según voces instaladas

# Texto y archivo
texto = "Billete de 500 pesos"
engine.save_to_file(texto, 'sonidos/cara500.wav')
engine.runAndWait()
texto = "Billete de 100 pesos"
engine.save_to_file(texto, 'sonidos/cara100.wav')
engine.runAndWait()
texto = "Billete de 50 pesos"
engine.save_to_file(texto, 'sonidos/cara50.wav')
engine.runAndWait()
texto = "Billete de 20 pesos"
engine.save_to_file(texto, 'sonidos/cara20.wav')
engine.runAndWait()