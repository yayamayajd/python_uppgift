from crypt import methods

from flask import Flask, request
import json

app = Flask(__name__)

#load tasks.json
with open("/Users/yayamaya/PycharmProjects/python_uppgift/tasks.json","r")as f:
    task_list = json.load(f)


#define a category list
categories = []

tasks_under_cate = []


#get tasks
@app.route("/tasks",methods=["GET"])
def show_tasks():
    return task_list


#post a new tasks, task id is the key
@app.route("/tasks",methods=["POST"])
def add_task():
    info_dict = request.get_json()
    new_task = {"id":info_dict["id"],
                "description":info_dict["description"],
                "category":info_dict["category"],
                "status":info_dict["status"]
                }
    for task in task_list:
        if task["id"] == new_task["id"]:
            return {"error": "task already existed"}, 409
    task_list.append(new_task)
    return new_task

#get by task id
@app.route("/tasks/<int:id>",methods=["GET"])
def show_task_by_id(id):
    for task in task_list:
        if task["id"] == id:
            return task
    return {"error":"task not found"},404

#delete task by id
@app.route("/tasks/<int:id>",methods=["DELETE"])
def delete_task_by_id(id):
    for task in task_list:
        if task["id"] == id:
            task_list.remove(task)
            return {"msg":"deleted"}
    return {"error":"task not found"},404

#change a task by id
@app.route("/tasks/<int:id>",methods=["PUT"])
def modify_task_by_id(id):
    description = request.args.get("description")
    category = request.args.get("category")
    if not description and not category:
        return {"error":"invalid data"},404
    for task in task_list:
        if task["id"] == id:
            if description:
                task["description"] = description
            if category:
                task["category"] = category

    return {"msg":f"task {task} modified"}

#put status by id
@app.route("/tasks/<int:id>/complete",methods=["PUT"])
def change_task_status_by_id(id):
    status = request.args.get("status")
    if not status:
        return {"error": "invalid data"}, 404
    for task in task_list:
        if task["id"] == id:
            if task["status"] != status:
                task["status"] = status

    return {"msg":f"the status of {task['id']} is {task['status']}"}

#get catagory list
@app.route("/tasks/categories",methods=["GET"])
def show_categories():
    for task in task_list:
        categories.append(task["category"])
    return categories

#get tasks under a specific catelist
@app.route("/tasks/categories/<category>",methods=["GET"])
def show_tasklist_by_cate(category):
    print(category)
    for task in task_list:
        if task["category"] == category:
            tasks_under_cate.append(task)
    return tasks_under_cate




