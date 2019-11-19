import pickle
import pyodbc
import numpy as np
import pandas as pd
from flask import Flask
from flask import request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

model = pickle.load(open('SalaryPrediction.pkl','rb'))

@app.route("/heathrow", methods=['POST'])
def post():
    # Get the data from the POST request.
    data = request.get_json(force=True)  # Make prediction using model loaded from disk as per the data.
    ## Get the Input from DB to predict.
    server = 'heathrowsqlserver.database.windows.net'
    database = 'heathrowsqldb'
    username = 'anjanwahwar'
    password = 'Anjan$1234'
    driver = '{FreeTDS}'
    cnxn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    dfdata = pd.read_sql("SELECT * FROM dbo.InputEmpData", cnxn)

    prediction = model.predict(dfdata[["Experiance"]])  # Take the first value of prediction
    cursor = cnxn.cursor()
    for i in range(len(prediction)):
        cursor.execute('''
                    INSERT INTO dbo.OutputEmpData (Salary)
                    VALUES
                    (?)
                    ''', int(prediction[i][0]))
        cnxn.commit()
    cursor.close()
    cnxn.close()
    return jsonify(['OK'])

if __name__ == "__main__":
    app.run(debug=True)
