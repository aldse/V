from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# Configuração da aplicação Flask
app = Flask(__name__)

# Rotas e funções para cada rota (como mostrado anteriormente)

# Função para inicializar e executar a aplicação Flask
def run_flask_app():
    app.run(debug=True)

# Verifica se este arquivo está sendo executado diretamente
if __name__ == '__main__':
    run_flask_app()

# Carregar o dataset
arquivo_csv = 'imdb-movies-dataset.csv'
df = pd.read_csv(arquivo_csv)

# Tratamento inicial dos dados (opcional)
df.dropna(inplace=True)
df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df_after_2020 = df[df['year'] > 2020]

# Função para plotar gráfico de dispersão
def scatter_plot():
    plt.figure(figsize=(10, 6))
    plt.scatter(df['duration'], df['rating'], alpha=0.5)
    plt.title('Correlação entre Duração e Rating')
    plt.xlabel('Duração (minutos)')
    plt.ylabel('Rating IMDB')
    plt.grid(True)
    
    # Converter o gráfico para um formato que o Flask pode exibir
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

# Função para plotar gráfico de pizza
def pie_chart():
    total_minutes_per_year = df.groupby('year')['duration'].sum()
    plt.figure(figsize=(10, 6))
    plt.pie(total_minutes_per_year, labels=total_minutes_per_year.index, autopct='%1.1f%%', startangle=140)
    plt.title('Distribuição do Total de Minutos por Ano')
    
    # Converter o gráfico para um formato que o Flask pode exibir
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

# Função para calcular a média de rating para filmes lançados após 2020
def average_rating_after_2020():
    avg_rating = df_after_2020['rating'].mean()
    return avg_rating

# Configurar a aplicação Flask
app = Flask(__name__)

# Rota para exibir o gráfico de dispersão
@app.route('/scatter')
def show_scatter_plot():
    plot_url = scatter_plot()
    return render_template('scatter.html', plot_url=plot_url)

# Rota para exibir o gráfico de pizza
@app.route('/pie')
def show_pie_chart():
    plot_url = pie_chart()
    return render_template('pie.html', plot_url=plot_url)

# Rota para exibir a média de rating após 2020
@app.route('/average-rating-after-2020')
def show_average_rating_after_2020():
    avg_rating = average_rating_after_2020()
    return f'A média de rating para filmes lançados após 2020 é {avg_rating:.2f}'

# Rota principal (opcional)
@app.route('/')
def index():
    return 'Hello, world!'

# Executar a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)
