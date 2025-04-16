import psutil
import platform
import datetime

def obtener_procesos_sospechosos():
    procesos = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'exe', 'cmdline', 'create_time']):
        try:
            info = proc.info
            sospechoso = False

            # Heurística simple para detección de procesos sospechosos
            if info['exe'] is None or 'AppData' in str(info['exe']) or 'Temp' in str(info['exe']):
                sospechoso = True

            procesos.append({
                'pid': info['pid'],
                'nombre': info['name'],
                'usuario': info['username'],
                'ruta': info['exe'],
                'comando': ' '.join(info['cmdline']) if info['cmdline'] else '',
                'inicio': datetime.datetime.fromtimestamp(info['create_time']).strftime('%Y-%m-%d %H:%M:%S'),
                'sospechoso': sospechoso
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return procesos

def info_sistema():
    return {
        'SO': platform.system(),
        'Version': platform.version(),
        'Arquitectura': platform.machine()
    }
