import sqlite3

def test_edit_task(client):
    # First add a task
    client.post('/addtask', data={
        'task_name': 'Old',
        'task_description': 'Old desc',
        'due_date': '',
        'status': 'Open'
    })

    response = client.post('/edittask/1', data={
        'task_name': 'Updated',
        'task_description': 'Updated desc'
    })

    assert response.status_code == 302

    conn = sqlite3.connect("test_tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE task_name = ?", ("Updated",))
    task = cursor.fetchone()
    conn.close()
    assert task is not None
    
def test_edit_duplicate_task(client):
    # Add an initial task
    client.post('/addtask', data={
        'task_name': 'Original',
        'task_description': 'Original desc',
        'due_date': '2026-03-20',
        'status': 'Open'
    })

    client.post('/addtask', data={
        'task_name': 'Original1',
        'task_description': 'Original desc',
        'due_date': '2026-03-20',
        'status': 'Open'
    })

    response = client.post('/edittask/1', data={
        'task_name': 'Original1',  # This name already exists
        'task_description': 'Updated desc',
        'due_date': '2026-03-30',
        'status': 'Completed'
    })

    conn = sqlite3.connect("test_tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT count(*) FROM tasks WHERE task_name = ?", ("Original1",))
    task = cursor.fetchone()
    conn.close()
    assert task[0] == 1


    assert response.status_code == 302


def test_edit_task_not_found(client):
    response = client.post('/edittask/999', data={
        'task_name': 'Does not exist',
        'task_description': 'Nope',
        'due_date': '2026-03-30',
        'status': 'Completed'
    })
    assert response.status_code == 302

def test_edit_task_partial_update(client):
    client.post('/addtask', data={
        'task_name': 'Task',
        'task_description': 'Desc',
        'due_date': '2026-03-20',
        'status': 'Open'
    })

    # Only update status
    response = client.post('/edittask/1', data={
        'status': 'Completed'
    })

    conn = sqlite3.connect("test_tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE task_name = ? and status = ?", ("Task", "Completed"))
    task = cursor.fetchone()
    conn.close()

    assert response.status_code == 302
    assert task is not None