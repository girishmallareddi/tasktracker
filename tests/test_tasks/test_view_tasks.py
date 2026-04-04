import sqlite3
def test_view_tasks(client):
    response = client.post('/addtask', data={
        'task_name': 'Test Task 1',
        'task_description': 'Test Desc',
        'due_date': '2026-03-20',
        'status': 'Open'
    })
    response = client.post('/addtask', data={
        'task_name': 'Test Task 2',
        'task_description': 'Test Desc',
        'due_date': '2026-03-20',
        'status': 'Completed'
    })

    response = client.post('/addtask', data={
        'task_name': 'Test Task 3',
        'task_description': 'Test Desc',
        'due_date': '2025-03-20',
        'status': 'Open'
    })

    response = client.post('/addtask', data={
        'task_name': 'Test Task 4',
        'task_description': 'Test Desc',
        'due_date': '',
        'status': 'Open'
    })

    response = client.post('/addtask', data={
        'task_name': 'Test Task 5',
        'task_description': 'Test Desc',
        'due_date': '2027-06-06',
        'status': 'Open'
    })

    response = client.get('/')

    assert response.status_code == 200

    html = response.data.decode()

    assert "Overdue Task" in html
    assert "Upcoming Task" in html
    assert "Completed Task" in html

    assert "Test Task 1" in html
    assert "Test Task 2" in html
    assert "Test Task 3" in html