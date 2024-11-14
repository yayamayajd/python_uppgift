

import pytest
from app import app


#inplement a client server to test
@pytest.fixture()
def client():
    app.config["Testing"] = True
    with app.test_client() as client:
        #the client server's status will be purged after yield
        yield client


def test_get_tasks(client):
    response = client.get("/tasks")
    print(response.get_json())
    assert response.status_code == 200

def test_post_a_new_task_on_tasks(client):
    response = client.post("/tasks",json={
        "id":125,
        "description":"Buy more ice cream!",
        "category":"Shopping",

    })
    print(response.get_json())
    assert response.status_code == 201

#if only try this function, it'll only return 404 because have not run add task 125
@pytest.mark.try_first
def test_get_task_by_id(client):
    response = client.get("/tasks/125")
    print(response.get_json())
    assert response.status_code == 200

def test_modify_task_by_id_json(client):
    response = client.put("tasks/125",json={
        "description":"Water the plants",
        "category":"Watering"
    })
    print(response.get_json())
    assert response.status_code == 200

def test_modify_task_by_id_url(client):
    response = client.put("/tasks/125?description=Water+The+Plants&category=Watering")
    print(response.get_json())
    assert response.status_code == 200

def test_delete_task_by_id_json(client):
    response = client.delete("tasks/125",json={"password":"123"})
    print(response.get_json())
    assert response.status_code == 200

def test_change_task_status_by_id(client):
    response = client.put("/tasks/123/complete")
    assert response.status_code == 200

def test_show_categories(client):
    response = client.get("/tasks/categories")
    assert response.status_code == 200
    assert isinstance(response.json,list)

def test_show_tasklist_by_cate(client):
    response = client.get("/tasks/categories/Cleaning")
    print(response.get_json())
    assert response.status_code == 200