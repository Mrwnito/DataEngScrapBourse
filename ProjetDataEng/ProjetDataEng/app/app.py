from flask import Flask, render_template
from ProjetDataEng.pipelines import ProjetdataengPipeline

# Initialisation de l'application Flask
app = Flask(__name__)

@app.route('/')
def index():
    """
    Route principale qui rend la page d'accueil avec les graphiques des indices financiers.
    
    Pour chaque indice financier, récupère les données les plus récentes depuis MongoDB,
    prépare les données pour les graphiques, calcule les changements en pourcentage,
    et passe les données au template HTML pour l'affichage.
    """
    # Liste des indices financiers à afficher
    indices = ["cac_40", "sbf_120", "cac_40_esg", "ent_pea_pme_150"]
    context = {}

    for indice in indices:
        # Récupération des données depuis MongoDB
        data = ProjetdataengPipeline.get_latest_data(indice)
        
        # Préparation des étiquettes (labels) et des points de données pour les graphiques
        labels = [d['time'] for d in data]
        dataPoints = [d['price'] for d in data]
        
        # Calcul des changements en pourcentage pour l'affichage dans un graphique séparé
        percent_changes = ProjetdataengPipeline.calculate_percentage_change(data)

        # Ajout des données préparées au contexte pour le passage au template
        context[f'labels_{indice}'] = labels
        context[f'dataPoints_{indice}'] = dataPoints
        context[f'percent_changes_{indice}'] = percent_changes

    # Rendu du template HTML avec les données préparées
    return render_template('index.html', **context)

# Point d'entrée pour l'exécution de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
