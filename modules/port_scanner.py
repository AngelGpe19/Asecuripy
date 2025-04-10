import subprocess
from utils.nmap_checker import get_nmap_path

def run_scan(target_ip, scan_type="fast"):
    nmap_path = get_nmap_path()
    if not nmap_path:
        return None, "❌ Nmap no está instalado o no se encontró en las rutas conocidas."

    if scan_type == "fast":
        command = [nmap_path, "-F", target_ip]
    elif scan_type == "full":
        command = [nmap_path, "-p-", target_ip]
    elif scan_type == "aggressive":
        command = [nmap_path, "-A", target_ip]
    else:
        command = [nmap_path, "-T4", target_ip]  # modo por defecto

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
        return output, None
    except subprocess.CalledProcessError as e:
        return None, f"❌ Error al ejecutar Nmap:\n{e.output}"
