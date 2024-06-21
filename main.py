from flask import Flask, render_template
import pandas as pd

arquivo_csv = 'imdb-movies-dataset.csv'

df = pd.read_csv(arquivo_csv)

app = Flask(__name__)

@app.route('/')
def index():
    return df.to_html()

if __name__ == '__main__':
    app.run(debug=True)
