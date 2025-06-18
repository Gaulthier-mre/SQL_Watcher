# log_parser.py

import re

def parse_logs(log_path):
    """
    Parse un fichier de logs Apache/Nginx et extrait les requêtes HTTP.
    Retourne une liste de dictionnaires avec : IP, méthode, URI, date.
    """
    pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s'                     # IP
        r'.*?\[(?P<date>.*?)\]\s'                           # Date
        r'"(?P<method>GET|POST|PUT|DELETE|HEAD)\s'          # Méthode
        r'(?P<uri>[^ ]+)'                                   # URI
    )

    results = []

    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                results.append({
                    'ip': match.group('ip'),
                    'method': match.group('method'),
                    'uri': match.group('uri'),
                    'date': match.group('date')
                })

    return results
