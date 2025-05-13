from flask import Flask, jsonify
import pandas as pd
import requests
from io import BytesIO

app = Flask(__name__)

# ✅ Lien de téléchargement direct de ton fichier Excel OneDrive
ONEDRIVE_FILE_URL = "https://lgdv-my.sharepoint.com/personal/c_dossa_emova-group_com/_layouts/15/download.aspx?share=EeGGU-HS_L9Kiau6sx3wr8sB3jNMZXd5H3wyFgBQZcGSHA"

@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Télécharger le fichier Excel
        response = requests.get(ONEDRIVE_FILE_URL)
        response.raise_for_status()

        # Lire le contenu Excel avec pandas
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data, sheet_name=0)

        # Nettoyage de base
        df_clean = df.dropna(how='all')
        return jsonify(df_clean.to_dict(orient='records'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
