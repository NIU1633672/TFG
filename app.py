from flask import Flask, send_file, Response
import requests, re, os
from bs4 import BeautifulSoup

app = Flask(__name__)
BASE_URL = "https://attack.mitre.org"
PAGE_URL = BASE_URL + "/versions/v16/resources/attack-data-and-tools/#excel-attack"

@app.route("/api/mitre-xlsx")
def mitre_xlsx():
    r = requests.get(PAGE_URL)
    soup = BeautifulSoup(r.content, "html.parser")
    link = soup.find("a", href=re.compile(r"enterprise-attack-v[\d\.]+\.xlsx"))
    if not link:
        return Response("No se encontró el Excel", status=500)

    url = BASE_URL + link['href']
    resp = requests.get(url)
    if resp.status_code != 200:
        return Response("Error al descargar", status=500)

    tmp = "enterprise-latest.xlsx"
    with open(tmp, "wb") as f:
        f.write(resp.content)

    return send_file(tmp, as_attachment=True, download_name="enterprise-attack-latest.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# 🔽 ESTA LÍNEA ES FUNDAMENTAL
if __name__ == "__main__":
    app.run(debug=True)
