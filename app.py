from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Variáveis globais para armazenar as tarefas
tarefas = []
tarefas_concluidas = []

def parse_data(data_str):
    """Função para tentar diferentes formatos de data."""
    for fmt in ('%d-%m-%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(data_str, fmt).strftime('%d-%m-%Y')
        except ValueError:
            continue
    raise ValueError(f"Formato de data não reconhecido: {data_str}")

@app.route('/')
def index():
    return render_template('index.html', tarefas=tarefas)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_tarefa():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data = request.form['data']
        tarefa = {
            'id': len(tarefas) + 1,
            'titulo': titulo,
            'descricao': descricao,
            'data': parse_data(data),
            'concluida': False
        }
        tarefas.append(tarefa)
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_tarefa(id):
    tarefa = next((tarefa for tarefa in tarefas if tarefa['id'] == id), None)
    if tarefa is None:
        return 'Tarefa não encontrada!', 404

    if request.method == 'POST':
        tarefa['titulo'] = request.form['titulo']
        tarefa['descricao'] = request.form['descricao']
        tarefa['data'] = parse_data(request.form['data'])
        return redirect(url_for('index'))

    return render_template('edit.html', tarefa=tarefa)

@app.route('/deletar/<int:id>')
def deletar_tarefa(id):
    global tarefas
    tarefas = [tarefa for tarefa in tarefas if tarefa['id'] != id]
    return redirect(url_for('index'))

@app.route('/concluir/<int:id>', methods=['POST'])
def concluir_tarefa(id):
    global tarefas, tarefas_concluidas
    tarefa = next((tarefa for tarefa in tarefas if tarefa['id'] == id), None)
    if tarefa:
        tarefa['concluida'] = not tarefa['concluida']
        if tarefa['concluida']:
            tarefas.remove(tarefa)
            tarefas_concluidas.append(tarefa)
        else:
            tarefas_concluidas.remove(tarefa)
            tarefas.append(tarefa)
    return redirect(url_for('index'))

@app.route('/lista_concluidas')
def lista_tarefas_concluidas():
    return render_template('concluidas.html', tarefas=tarefas_concluidas)

if __name__ == '__main__':
    app.run(debug=True)
