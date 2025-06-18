import webbrowser
from collections import Counter
from tkinter import messagebox, filedialog

def export_to_html(data):
    if not data:
        messagebox.showwarning("Aucune alerte", "Aucune alerte à exporter.")
        return

    methods = [row[1] for row in data]  # méthode HTTP
    dates = [row[3] for row in data]    # date AAAA-MM-JJ
    ips = [row[0] for row in data]      # adresse IP

    count_methods = Counter(methods)
    count_dates = Counter(dates)
    count_ips = Counter(ips).most_common(5)  # top 5 IP

    methods_labels = list(count_methods.keys())
    methods_values = list(count_methods.values())

    dates_labels = list(count_dates.keys())
    dates_values = list(count_dates.values())

    ips_labels = [ip for ip, _ in count_ips]
    ips_values = [count for _, count in count_ips]

    html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8" />
<title>Rapport SQLWatcher</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  body {{ background: #1e1e1e; color: white; font-family: Arial, sans-serif; padding: 20px; }}
  h1 {{ color: #e63946; }}
  table {{ border-collapse: collapse; width: 100%; margin-bottom: 40px; }}
  th, td {{ border: 1px solid #444; padding: 8px; text-align: left; }}
  th {{ background-color: #333; }}
  tr:nth-child(even) {{ background-color: #2a2a2a; }}
  .chart-container {{ width: 600px; margin-bottom: 50px; }}
</style>
</head>
<body>
  <h1>Rapport SQLWatcher</h1>

  <h2>Liste des alertes détectées ({len(data)})</h2>
  <table>
    <thead>
      <tr><th>IP</th><th>Méthode</th><th>URI</th><th>Date</th><th>Détectée à</th></tr>
    </thead>
    <tbody>
      {"".join(f"<tr><td>{ip}</td><td>{method}</td><td>{uri}</td><td>{date}</td><td>{timestamp}</td></tr>" for ip, method, uri, date, timestamp in data)}
    </tbody>
  </table>

  <div class="chart-container">
    <canvas id="methodChart"></canvas>
  </div>

  <div class="chart-container">
    <canvas id="dateChart"></canvas>
  </div>

  <div class="chart-container">
    <canvas id="ipChart"></canvas>
  </div>

<script>
  const methodCtx = document.getElementById('methodChart').getContext('2d');
  const methodChart = new Chart(methodCtx, {{
    type: 'pie',
    data: {{
      labels: {methods_labels},
      datasets: [{{
        label: 'Nombre d\'alertes par méthode',
        data: {methods_values},
        backgroundColor: ['#e63946', '#f1faee', '#a8dadc', '#457b9d', '#1d3557'],
      }}]
    }},
    options: {{
      responsive: true,
      plugins: {{
        legend: {{
          position: 'right',
          labels: {{color: 'white'}}
        }}
      }}
    }}
  }});

  const dateCtx = document.getElementById('dateChart').getContext('2d');
  const dateChart = new Chart(dateCtx, {{
    type: 'bar',
    data: {{
      labels: {dates_labels},
      datasets: [{{
        label: 'Alertes par date',
        data: {dates_values},
        backgroundColor: '#e63946',
      }}]
    }},
    options: {{
      scales: {{
        x: {{ ticks: {{ color: 'white' }} }},
        y: {{ ticks: {{ color: 'white' }}, beginAtZero: true }}
      }},
      plugins: {{
        legend: {{
          labels: {{ color: 'white' }}
        }}
      }}
    }}
  }});

  const ipCtx = document.getElementById('ipChart').getContext('2d');
  const ipChart = new Chart(ipCtx, {{
    type: 'bar',
    data: {{
      labels: {ips_labels},
      datasets: [{{
        label: 'Top 5 IP détectées',
        data: {ips_values},
        backgroundColor: '#f1faee',
      }}]
    }},
    options: {{
      scales: {{
        x: {{ ticks: {{ color: 'white' }} }},
        y: {{ ticks: {{ color: 'white' }}, beginAtZero: true }}
      }},
      plugins: {{
        legend: {{
          labels: {{ color: 'white' }}
        }}
      }}
    }}
  }});
</script>

</body>
</html>
"""

    file_path = filedialog.asksaveasfilename(
        defaultextension=".html",
        filetypes=[("Fichier HTML", "*.html")],
        title="Enregistrer le rapport HTML"
    )
    if not file_path:
        return

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        messagebox.showinfo("Export réussi", f"Rapport HTML généré :\n{file_path}")
        webbrowser.open(f"file://{file_path}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'export HTML : {e}")
