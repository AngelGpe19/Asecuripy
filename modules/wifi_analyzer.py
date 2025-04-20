# red_utils.py

import subprocess
import re
import socket
import platform
import os
import ipaddress
import logging
from collections import Counter
from typing import Optional, List, Dict
import psutil

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def ejecutar_comando(cmd: str) -> str:
    """Ejecuta un comando del sistema y retorna su salida como string."""
    try:
        output = subprocess.check_output(cmd, shell=True, encoding="cp1252", stderr=subprocess.DEVNULL)
        return output
    except subprocess.CalledProcessError as e:
        logging.warning(f"Comando fallido '{cmd}': {e}")
        return ""


def obtener_ip_local() -> Optional[str]:
    """Retorna la IP local del equipo."""
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.error as e:
        logging.error(f"Error al obtener IP local: {e}")
        return None


def obtener_gateway() -> Optional[str]:
    """Detecta el gateway predeterminado utilizando psutil."""
    try:
        interfaces = psutil.net_if_addrs()
        estados = psutil.net_if_stats()

        for interfaz, estado in estados.items():
            if estado.isup and interfaz in interfaces:
                for addr in interfaces[interfaz]:
                    if addr.family == socket.AF_INET and addr.address != '127.0.0.1':
                        return addr.address
    except Exception as e:
        logging.error(f"Error detectando gateway: {e}")
    
    return None


def obtener_interfaces_activas() -> List[Dict[str, str]]:
    """Obtiene las interfaces de red activas con sus direcciones IPv4."""
    salida = ejecutar_comando("ipconfig")
    bloques = salida.split("\n\n")
    interfaces = []

    for bloque in bloques:
        nombre = re.search(r"Adaptador de (.+):|adapter (.+):", bloque)
        ip = re.search(r"Dirección IPv4[ .:]*([\d.]+)|IPv4 Address[ .:]*([\d.]+)", bloque)
        if nombre and ip:
            interfaces.append({
                "nombre": nombre.group(1) or nombre.group(2),
                "ip": ip.group(1) or ip.group(2)
            })
    return interfaces


def obtener_redes_disponibles() -> str:
    """Escanea y retorna la salida cruda de redes WiFi disponibles."""
    return ejecutar_comando("netsh wlan show networks mode=bssid")


def verificar_cifrado_red() -> Dict[str, int]:
    """Cuenta los tipos de autenticación detectados en redes WiFi."""
    redes = obtener_redes_disponibles()
    cifrados = re.findall(r"Autenticación[ .:]+(.+)|Authentication[ .:]+(.+)", redes)
    tipos = [tipo[0] or tipo[1] for tipo in cifrados]
    return dict(Counter(tipos))


def analizar_canal_wifi() -> Dict[str, int]:
    """Identifica los canales WiFi más utilizados."""
    redes = obtener_redes_disponibles()
    canales = re.findall(r"Canal[ .:]+(\d+)|Channel[ .:]+(\d+)", redes)
    lista = [c[0] or c[1] for c in canales]
    return dict(Counter(lista))


def obtener_tabla_arp() -> str:
    """Obtiene la tabla ARP actual del sistema."""
    return ejecutar_comando("arp -a")


def detectar_spoofing_arp() -> List[str]:
    """Detecta MACs duplicadas en la tabla ARP que podrían indicar spoofing."""
    tabla = obtener_tabla_arp()
    macs = re.findall(r"([a-fA-F0-9\-]{17})", tabla)
    duplicadas = [mac for mac, count in Counter(macs).items() if count > 1]
    return duplicadas


def escanear_dispositivos_red() -> List[str]:
    """Realiza un ping en red /24 para detectar hosts activos."""
    ip_local = obtener_ip_local()
    if not ip_local:
        logging.error("No se pudo determinar la IP local.")
        return []

    red = ipaddress.IPv4Network(ip_local + "/24", strict=False)
    activos = []

    logging.info("Escaneando dispositivos activos en la red...")
    for ip in red.hosts():
        ip_str = str(ip)
        if ip_str == ip_local:
            continue
        if os.system(f"ping -n 1 -w 100 {ip_str} >nul") == 0:
            activos.append(ip_str)
    
    logging.info(f"Dispositivos encontrados: {len(activos)}")
    return activos

if __name__ == "__main__":
    print("[LOG] 🔄 Iniciando análisis de red...")
    redes = obtener_redes_disponibles()
    for r in redes:
        print(r)