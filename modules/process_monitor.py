import psutil
import os
from datetime import datetime

def es_sospechoso(proc):
    nombre = proc.name().lower()
    ruta = proc.exe().lower() if proc.exe() else ""

    patrones = ["keylogger", "stealer", "rat", "backdoor", "sniffer", "injector", "bitcoin", "miner"]
    return any(pat in nombre or pat in ruta for pat in patrones)

def tiene_alto_consumo(proc):
    try:
        cpu = proc.cpu_percent(interval=0.1)
        memoria = proc.memory_percent()
        return cpu > 10 or memoria > 10
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False

def calcular_score(proc):
    score = 0

    if tiene_alto_consumo(proc):
        score += 30

    if es_sospechoso(proc):
        score += 50

    try:
        conexiones = proc.connections(kind='inet')
        conexiones_establecidas = [c for c in conexiones if c.status == psutil.CONN_ESTABLISHED]
        if conexiones_establecidas:
            score += 20
    except Exception:
        pass

    return min(score, 100)

def obtener_procesos_clasificados():
    procesos = []

    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            nombre = proc.info['name'] or ''
            ruta = proc.info['exe'] or ''
            score = calcular_score(proc)

            if es_sospechoso(proc):
                clasificacion = "Sospechoso"
            elif tiene_alto_consumo(proc):
                clasificacion = "Alto Consumo"
            else:
                clasificacion = "Normal"

            procesos.append({
                "pid": proc.pid,
                "nombre": nombre,
                "ruta": ruta,
                "clasificacion": clasificacion,
                "score": score
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return procesos

def filtrar_procesos_sospechosos(procesos, umbral=50):
    return [p for p in procesos if p["score"] >= umbral]

def guardar_log_sospechosos(procesos, archivo="log_procesos_sospechosos.txt"):
    sospechosos = filtrar_procesos_sospechosos(procesos)

    if not sospechosos:
        return

    with open(archivo, "a", encoding="utf-8") as f:
        f.write(f"\n--- Análisis del {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        for proc in sospechosos:
            f.write(f"PID: {proc['pid']}, Nombre: {proc['nombre']}, Ruta: {proc['ruta']}, Score: {proc.get('score', 'N/A')}\n")
        f.write("\n")
