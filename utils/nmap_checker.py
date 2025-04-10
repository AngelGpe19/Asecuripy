import os
import shutil

def get_nmap_path():
    path = shutil.which("nmap")
    if path:
        return path

    posibles_rutas = [
        r"C:\Program Files (x86)\Nmap\nmap.exe",
        r"C:\Program Files\Nmap\nmap.exe"
    ]
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            return ruta

    return None

def is_nmap_installed():
    return get_nmap_path() is not None
