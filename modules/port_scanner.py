import socket
import threading
from queue import Queue

# Diccionario de servicios comunes
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP Proxy"
}

# Cola para manejar múltiples puertos
cola_puertos = Queue()

# Lista donde se almacenarán los resultados
resultados = []

def escanear_puerto(ip, puerto, timeout=1.0):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        resultado = sock.connect_ex((ip, puerto))
        if resultado == 0:
            servicio = COMMON_PORTS.get(puerto, "Desconocido")
            resultados.append((puerto, servicio))
        sock.close()
    except Exception:
        pass  # Silenciar errores de red

def trabajador(ip):
    while not cola_puertos.empty():
        puerto = cola_puertos.get()
        escanear_puerto(ip, puerto)
        cola_puertos.task_done()

def escanear_puertos(ip, rango_inicio=1, rango_fin=1024, hilos=100):
    global resultados
    resultados = []

    for puerto in range(rango_inicio, rango_fin + 1):
        cola_puertos.put(puerto)

    threads = []
    for _ in range(hilos):
        thread = threading.Thread(target=trabajador, args=(ip,))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    cola_puertos.join()
    return resultados
