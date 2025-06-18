# sqlwatcher.py

import os
import sys
from log_parser import parse_logs
from detection_rules import detect_sql_injection
from db_manager import init_db, insert_alert

LOG_FILE_PATH = "test_logs/access.log"
DB_PATH = "alerts.db"

def main():
    print("[*] Initialisation de SQLWatcher...")

    # Vérification du fichier de logs
    if not os.path.exists(LOG_FILE_PATH):
        print(f"[!] Fichier de log non trouvé : {LOG_FILE_PATH}")
        sys.exit(1)

    # Initialisation de la base de données
    init_db(DB_PATH)

    print(f"[*] Analyse du fichier de log : {LOG_FILE_PATH}")
    requests = parse_logs(LOG_FILE_PATH)

    alert_count = 0

    for req in requests:
        ip, uri, method, date = req['ip'], req['uri'], req['method'], req['date']

        # Vérification d'injection SQL
        if detect_sql_injection(uri):
            print(f"[!] Injection SQL détectée depuis {ip} -> {uri}")
            insert_alert(DB_PATH, ip, method, uri, date)
            alert_count += 1

    print(f"[+] Analyse terminée. {alert_count} alertes SQL détectées.")

if __name__ == "__main__":
    main()
