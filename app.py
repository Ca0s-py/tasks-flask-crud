from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__) # __name__ faz referencia ao nome do arquivo


# CRUD -> Create, Read, Update, Delete

# Variables
tasks = []
task_id_control = 1

# Cria a rota, permite comunicar com outros clients
@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data['title'], description=data.get('description', ''))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({'mensagem': 'Nova tarefa criada com sucesso'})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    #for task in tasks:
    #    task_list.append(task.to_dict())
    
    output = {
                "tasks": task_list,
                "total_tasks": len(task_list)
            }
    return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    
    return jsonify({'message': 'Not Found'}), 404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_tasks(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break # para o loop quando encontrar, não percorre a lista inteira !!! PERFORMANCE !!!
    print(task)
    if task == None:
        return jsonify({'message': 'Not found'}), 404
    
    data =  request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    print(task)
    return jsonify({'message': 'Tarefa atualizada com sucesso'})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_tasks(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break # para o loop quando encontrar, não percorre a lista inteira !!! PERFORMANCE !!!

    if not task:
        return jsonify({'message': 'Tarefa não encontrada'}), 404
    
    tasks.remove(task)
    return jsonify({'message': 'Tarefa deletada com sucesso'})

# Verifica se o servidor está rodando em ambiente de desenvolvimento
if __name__  == '__main__':
    app.run(debug=True) 