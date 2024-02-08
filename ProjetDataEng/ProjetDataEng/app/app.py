from flask import Flask, render_template
from ProjetDataEng.pipelines import ProjetdataengPipeline

app = Flask(__name__)

@app.route('/')
def index():
    
    indices = ["cac_40", "sbf_120", "cac_40_esg", "ent_pea_pme_150"]
    context = {}

    for indice in indices:
        data = ProjetdataengPipeline.get_latest_data(indice)
        labels = [d['time'] for d in data]
        dataPoints = [d['price'] for d in data]
        percent_changes = ProjetdataengPipeline.calculate_percentage_change(data)

        context[f'labels_{indice}'] = labels
        context[f'dataPoints_{indice}'] = dataPoints
        context[f'percent_changes_{indice}'] = percent_changes

    return render_template('index.html', **context)

if __name__ == '__main__':
    app.run(debug=True)

