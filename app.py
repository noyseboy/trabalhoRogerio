from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Variável global para armazenar as tarefas
tarefas = []

@app.route('/')
def index():
    return render_template('index.html', tarefas=tarefas)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_tarefa():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        tarefa = {'id': len(tarefas) + 1, 'titulo': titulo, 'descricao': descricao}
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
        return redirect(url_for('index'))

    return render_template('edit.html', tarefa=tarefa)

@app.route('/deletar/<int:id>')
def deletar_tarefa(id):
    global tarefas
    tarefas = [tarefa for tarefa in tarefas if tarefa['id'] != id]
    return redirect(url_for('index'))

if __name__ == "_main_":
    app.run(debug=True)