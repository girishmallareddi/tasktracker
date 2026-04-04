import sqlite3

def test_delete_task(client):
    # Add a task first
    client.post('/addtask', data={
        'task_name': 'To delete',
        'task_description': 'desc',
        'due_date': '',
        'status': 'Open'
    })

    response = client.post('/delete_task/1')

    assert response.status_code == 302

    conn = sqlite3.connect("test_tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE task_name = ?", ("To delete",))
    task = cursor.fetchone()

    conn.close()

    assert response.status_code == 302  
    assert task is None


def test_delete_task_not_found(client):
    response = client.post('/delete_task/999')
    assert response.status_code == 302


