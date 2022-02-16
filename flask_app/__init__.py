from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

def create_app():
    app = Flask(__name__)
    model = pickle.load(open('./flask_app/enc_linear_model.pkl', 'rb'))
    @app.route('/', methods = ['Post', 'Get'])
    def home():
        return render_template('first.html')


    @app.route('/predict', methods = ['Post', 'Get'])
    def predict():
        data1 = request.form['a']
        data2 = request.form['b']
        data3 = request.form['c']
        data4 = request.form['d']
        arr = np.array([[data1, data2, data3, data4]])
        df = pd.DataFrame(arr, columns=['Brand', 'Component', 'Movement', 'Glass']) 
        pred = model.predict(df)
        return render_template('second.html', 
        option = f' Brand: {data1} / Component: {data2} / Movement: {data3} / Glass: {data4}',
        data= "{:,}".format(int(pred)))


    if __name__ == "__main__":
        app.run(debug=True)
    
    return app