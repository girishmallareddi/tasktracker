import sqlite3

def test_add_task(client):
    response = client.post('/addtask', data={
        'task_name': 'Test Task',
        'task_description': 'Test Desc',
        'due_date': '2026-03-20',
        'status': 'Open'
    })

    conn = sqlite3.connect("test_tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE task_name = ?", ("Test Task",))
    task = cursor.fetchone()

    conn.close()

    assert response.status_code == 302  
    assert task is not None

def test_duplicate_task(client):
    response = client.post('/addtask', data={
        'task_name': 'Test Task',
        'task_description': 'Test Desc',
        'due_date': '2026-03-20',
        'status': 'Open'
    })

    response = client.post('/addtask', data={
        'task_name': 'Test Task',
        'task_description': 'Test Desc',
        'due_date': '2026-03-20',
        'status': 'Open'
    })

    conn = sqlite3.connect("test_tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT count(*) FROM tasks WHERE task_name = ?", ("Test Task",))
    task = cursor.fetchone()
    conn.close()
    assert task[0] == 1
    assert response.status_code == 302  



def test_add_task_missing_fields(client):
    # Missing both name and description
    response = client.post('/addtask', data={
        'task_name': '',
        'task_description': ''
    })
    assert response.status_code == 302
    conn = sqlite3.connect("test_tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE task_name is null and task_description is null")
    task = cursor.fetchone()

    conn.close()
    assert task is None

    # Missing name
    response = client.post('/addtask', data={
        'task_name': '',
        'task_description': 'Desc'
    })
    assert response.status_code == 302
    conn = sqlite3.connect("test_tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE task_name is null")
    task = cursor.fetchone()

    conn.close()
    assert task is None

    # Missing description
    response = client.post('/addtask', data={
        'task_name': 'Name',
        'task_description': ''
    })
    assert response.status_code == 302
    conn = sqlite3.connect("test_tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE task_description is null")
    task = cursor.fetchone()

    conn.close()
    assert task is None

