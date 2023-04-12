import gradio as gr
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('todo.db')
c = conn.cursor()

# Create the 'tasks' table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, status TEXT)''')

# Define the function that implements the TODO app
def todo_app(description, status):
    # Insert the new task into the 'tasks' table
    c.execute(f"INSERT INTO tasks (description, status) VALUES ('{description}', '{status}')")
    conn.commit()

    # Retrieve all tasks from the 'tasks' table
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()

    # Display the tasks in separate boxes
    tasks_html = ""
    for task in tasks:
        tasks_html += f"<div style='padding: 10px; margin: 10px; border: 1px solid black;'><b>Task {task[0]}:</b> {task[1]} (<i>{task[2]}</i>)</div>"

    # Return the tasks HTML string
    return tasks_html

# Define the inputs of the Gradio interface
inputs = [
    gr.inputs.Textbox(label="Task description"),
    gr.inputs.Dropdown(label="Task status", choices=["Todo", "Doing", "Done"])
]

# Define the outputs of the Gradio interface
outputs = gr.outputs.HTML(label="Tasks list")

# Define the Gradio interface
iface = gr.Interface(fn=todo_app, inputs=inputs, outputs=outputs, title="TODO App", description="Add, delete, and edit tasks in a TODO list.", live=True)

# Run the Gradio interface
iface.launch()
