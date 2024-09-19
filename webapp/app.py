from flask import Flask, render_template, request, redirect, url_for
import joblib
import numpy as np

# Charger le modèle ML entrainé
model = joblib.load('model.pkl')

# Initier l'app Flask
app = Flask(__name__)

# Définir le route et retourner notre template index.html
@app.route('/', methods=['GET'])
def index():
    # Pas de prédiction à afficher à l'arrivée sur la page
    return render_template('index.html', prediction=None)

#Definir le route de la seconde page
@app.route('/exploration', methods=['GET'])
def second_page():
    return render_template('exploration.html')

# Définir un route pour recevoir les données du formulaire et faire la prédiction
@app.route('/submit_form', methods=['POST'])
def predict():
    # Vérifier si les données du formulaire sont présentes
    if request.method == 'POST':
        try:
            CreditScore = float(request.form['CreditScore'])
            Age = int(request.form['Age'])
            Tenure = int(request.form['Tenure'])
            Balance = float(request.form['Balance'])
            NumOfProducts = int(request.form['NumOfProducts'])
            HasCrCard = int(request.form['HasCrCard'])
            IsActiveMember = int(request.form['IsActiveMember'])
            EstimatedSalary = float(request.form['EstimatedSalary'])
            
            Gender = request.form['Gender']
            Geography = request.form['Geography']
            
            # Convertir les valeurs catégorielles en variables binaires
            Gender_Male = True if Gender == 'Male' else False
            Gender_Female = True if Gender == 'Female' else False
            Geography_France = True if Geography == 'France' else False
            Geography_Germany = True if Geography == 'Germany' else False
            Geography_Spain = True if Geography == 'Spain' else False

            # Créer un tableau avec ces données pour les passer au modèle ML
            input_data = np.array([[CreditScore, Age, Tenure, Balance, NumOfProducts, HasCrCard,IsActiveMember, EstimatedSalary, Gender_Male, Gender_Female, Geography_France, Geography_Germany, Geography_Spain]])
            
            # Faire une prédiction avec le modèle chargé
            prediction = model.predict(input_data)
            prediction_result = 'Cette personne restera dans la banque' if prediction[0] == 0 else 'Cette personne quittera la banque'
        except Exception as e:
            # En cas d'erreur, afficher un message générique ou l'erreur
            prediction_result = f"Erreur lors de la prédiction: {str(e)}"
    else:
        # Pas de données soumises
        prediction_result = None
    
    # Retourner la prédiction sur une nouvelle page ou la même page avec un message
    return render_template('index.html', prediction=prediction_result)

# Run app
if __name__ == '__main__':
    app.run(port=3000, debug=True)
