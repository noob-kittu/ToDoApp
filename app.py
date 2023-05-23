from flask import Flask, request, render_template, redirect, g, url_for
import sqlite3


app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('todo.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
        '''
    )
    db.commit()

# Fetch all tasks from the database
def fetch_tasks_from_database():
    db = get_db()
    cursor = db.execute('SELECT * FROM tasks')
    tasks = []
    for row in cursor.fetchall():
        tasks.append(dict(row))
    return tasks


# Save a new task to the database
def save_task_to_database(task):
    db = get_db()
    db.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    db.commit()

# Delete a task from the database
def delete_task_from_database(task_id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()

# Update a task in the database
def update_task_in_database(task_id, updated_task):
    db = get_db()
    db.execute('UPDATE tasks SET task = ? WHERE id = ?', (updated_task, task_id))
    db.commit()


@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()



@app.route('/', methods=['GET'])
def home():
    # Fetch tasks from the database and pass them to the template
    # to display them to the user
    tasks = fetch_tasks_from_database()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    # Save the task to the database
    save_task_to_database(task)  # Implement this function
    return redirect('/')

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    # Delete the task from the database
    delete_task_from_database(task_id)  # Implement this function
    return redirect('/')

@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    updated_task = request.form.get('updated_task')
    # Update the task in the database
    update_task_in_database(task_id, updated_task)  # Implement this function
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
    
