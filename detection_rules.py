# detection_rules.py

import re

# Liste d'expressions régulières simples pour détecter les injections SQL
SQLI_PATTERNS = [
    r"(\%27)|(\')|(\-\-)|(\%23)|(#)",                         # quote, comment
    r"(\%22)|(\")",                                           # double quote
    r"(?i)\bOR\b.+\=.+",                                      # OR 1=1
    r"(?i)\bUNION\b.+\bSELECT\b",                             # UNION SELECT
    r"(?i)\bSELECT\b.+\bFROM\b",                              # SELECT ... FROM
    r"(?i)\bINSERT\b.+\bINTO\b",                              # INSERT INTO
    r"(?i)\bUPDATE\b.+\bSET\b",                               # UPDATE ... SET
    r"(?i)\bDELETE\b.+\bFROM\b",                              # DELETE FROM
    r"(?i)\bDROP\b.+\bTABLE\b",                               # DROP TABLE
    r"(?i)\b--\b",                                            # double dash comment
    r"(?i)\bWAITFOR\b.+\bDELAY\b",                            # Time-based attack
    r"(?i)\bSLEEP\((\s*\d+\s*)\)",                            # MySQL SLEEP
    r"(?i)\bINFORMATION_SCHEMA\b",                            # Info schema access
]

def detect_sql_injection(uri):
    """
    Vérifie si l'URI contient un pattern suspect d'injection SQL.
    Retourne True si une correspondance est trouvée.
    """
    for pattern in SQLI_PATTERNS:
        if re.search(pattern, uri):
            return True
    return False
