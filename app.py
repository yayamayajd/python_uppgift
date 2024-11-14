from crypt import methods

from flask import Flask, request, render_template, jsonify
import json


app = Flask(__name__)

#load tasks.json
with open("/Users/yayamaya/PycharmProjects/python_uppgift/tasks.json","r")as f:
    task_list = json.load(f)



#index page
@app.route("/")
def show_index():
    print(task_list)
    return render_template("todo_index.html",task_list=task_list)

#get tasks
@app.route("/tasks",methods=["GET"])
def show_tasks():
    #the result of request.args or .get_json is a dict, so need to use get to take out the value
    status = request.args.get("status")
    filteded_task_list_pending = []
    filteded_task_list_completed = []
    for task in task_list:
        if task["status"] == "pending":
            filteded_task_list_pending.append(task)
        elif task["status"] == "finished":
            filteded_task_list_completed.append(task)

    if status == "pending":
        return jsonify(filteded_task_list_pending),200
    elif status == "complete":
        return jsonify(filteded_task_list_completed),200
    else:
        return jsonify(task_list),200

#post a new tasks, task id is the key
@app.route("/tasks",methods=["POST"])
def add_task():
    # I added json format för att kör test program
    info_dict = request.form or request.args or request.get_json()

    try:
        new_task = {"id":int(info_dict["id"]),
                    "description":info_dict["description"],
                    "category":info_dict["category"],
                    "status":"pending" #pending is the default status
                    }
    except ValueError:
        return jsonify({"error":"invalid id"}),400

    for task in task_list: #check if the id is already in list
        if task["id"] == new_task["id"]:
            return jsonify({"error": "task already existed"}, 409)
    task_list.append(new_task)
    return jsonify(f"a new task{new_task['id']} has been added"),201

#get by task id
@app.route("/tasks/<int:id>",methods=["GET"])
def show_task_by_id(id):
    for task in task_list:
        if task["id"] == id:
            return jsonify(task),200
    return jsonify({"error":"task not found"}),404


@app.route("/tasks/<int:id>",methods=["PUT"])
def modify_task_by_id(id):
    #need ti create a dict to put the information in it, because request.get.json can not get specific key:value
    dict_new_info = request.args or request.get_json()
    description = dict_new_info.get("description")
    category = dict_new_info.get("category")
    if not description and not category:
        return jsonify({"error":"invalid data"}),400
    for task in task_list:
        if task["id"] == id:
            if description:
                task["description"] = description
            if category:
                task["category"] = category
            return jsonify("the task has been updated"),200
    return jsonify({"error":"no such task"}),404


#the decorator to check the tocken. correct password = 123
#1.sent the func to pass_check as parameter
#2.create a inner fun to gathering every thing as parameter
#3.set the if to check if the password is correct, if true then run the delete, if not return 401, whi mneas unauthorized
def pass_check(delete_task_by_id):
    def wrapper(*args,**kwargs):
        password = request.args or request.get_json()
        if password.get("password") == "123":
            return delete_task_by_id(*args,**kwargs)
        else:
            return jsonify({"error":"can not delete task, wrong password"}),401
    return wrapper

@app.route("/tasks/<int:id>", methods=["DELETE"])
@pass_check
def delete_task_by_id(id):
    for task in task_list:
        if task["id"] == id:
            task_list.remove(task)
            return jsonify("task deleted"),200
    return jsonify({"error":"task not found"},404)



@app.route("/tasks/<int:id>/complete",methods=["PUT"])
def change_task_status_by_id(id):
    for task in task_list:
        if task["id"] == id:
            task["status"] = "completed"
            return jsonify({"msg":f"the status of {task['id']} is {task['status']}"}),200
        return jsonify({"error":"no such task"}),404



#get catagory list
@app.route("/tasks/categories",methods=["GET"])
def show_categories():
    # use a set to limit the same category only shows once
    categories_set = set()
    for task in task_list:
        categories_set.add(task["category"])
    # change the set back to the list
    categories = list(categories_set)
    return jsonify(categories),200

#get tasks under a specific catelist
@app.route("/tasks/categories/<category>",methods=["GET"])
def show_tasklist_by_cate(category):
    tasks_under_cate = []
    for task in task_list:
        if task["category"] == category:
            tasks_under_cate.append(task)
            return jsonify(tasks_under_cate),200
    return jsonify("no such category"),404






