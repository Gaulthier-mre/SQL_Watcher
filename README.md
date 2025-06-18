# SQLWatcher : Détecteur d'injections SQL dans les logs Apache/Nginx

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Un outil pour analyser les fichiers de logs web et détecter les tentatives d'injection SQL en temps réel.  

**Fonctionnalités** :  
- Parsing des logs (Apache/Nginx)  
- Détection de 15+ patterns SQLi (règles configurables)  
- Stockage des alertes en base SQLite  
- Interface graphique (Tkinter) avec export CSV/HTML  

## 🚀 Utilisation

### 🔍 1. Analyse des logs
1. Placez vos fichiers de logs dans le dossier `test_logs/` (par exemple `access.log`)
2. Lancez l'analyse :

```bash
python sqlwatcher.py
