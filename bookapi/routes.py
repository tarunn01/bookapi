from flask import Blueprint, request, jsonify, session,render_template

# Create a Blueprint instance.
# 'my_app_routes' is the name of the blueprint.
# __name__ is used to locate resources like templates relative to the blueprint.
bp = Blueprint('my_app_routes', __name__, template_folder='templates')
tasks = [{"id": 1, "title": "Learn Flask Blueprints", "completed": False},
    {"id": 2, "title": "Understand REST APIs", "completed": False}]

next_task_id = 3 # To assign unique IDs for new tasks

@bp.route('/todos', methods = ['GET'])
def get_todos():
    # render_template still looks in the 'templates' folder, relative to the blueprint.
    return jsonify(tasks)

@bp.route('/todos<int:task_id>')
def get_todo(task_id):
    try:
        #find the task with the matching id
        found_task = None
        for task in tasks:
            if task["id"] == task_id:
                found_task = task
                break
        if found_task:
            return jsonify(found_task),200 #OK
        else:
            #if task not found, return 404 not found
            return jsonify({"message": f"Task with ID{task_id} not found"}), 404
    except Exception as e:
        #catch any unexpected errors during retrieval
        return jsonify({"message": f"An error occured:{str(e)}"}), 500 #internal server error

@bp.route('/todos', methods = ['POST'])
def add_todo():
    global next_task_id
    try:
        # render_template still looks in the 'templates' folder, relative to the blueprint.
        if not request.is_json: #request.is_json for more robust check
            return jsonify({"error": "Request Content-type must be application/json"}), 400

        data = request.json
        new_task_title = data.get('title')

        if not new_task_title or not isinstance(new_task_title,str) or new_task_title.strip() == "":
            return jsonify({"error": "Title is required for a new task"}), 400

        new_task = {
            "id" : next_task_id,
            "title": new_task_title,
            "completed": request.json.get('completed',False) # default to false if not provided
        }
        tasks.append(new_task)
        next_task_id += 1
        return jsonify(new_task), 201 #return the created tasks with 201 created status
    except Exception as e:
        #catch any unexpected errors during task creation
        return jsonify({"message": f"An error occured during task creation {str(e)}"}), 500 #internal server error


# Define the home route using the blueprint
@bp.route('/')
def home():
    # render_template still looks in the 'templates' folder, relative to the blueprint.
    return render_template('index.html', message="Welcome to the refactored Flask app!")

# Route with a Dynamic Parameter
@bp.route('/users/<int:user_id>')
def get_user_profile(user_id):
    # Flask automatically converts the dynamic part to an integer due to '<int:user_id>'
    # Example usage of request.args:
    # If you access /users/123?name=Alice, request.args.get('name') would be 'Alice'
    name_param = request.args.get('name', 'Guest')
    return f"Displaying profile for User ID: {user_id}. Query parameter name: {name_param}"

# Implement a POST Request Route (previous example, now also demonstrates request.form)
@bp.route('/submit_data', methods=['POST'])
def submit_data():
    # For form data (Content-Type: application/x-www-form-urlencoded)
    if request.form:
        print("Received form data (request.form):", request.form)
        return jsonify({"status": "success", "message": "Form data received!", "data": request.form.to_dict()})
    # For JSON data (Content-Type: application/json)
    elif request.json:
        print("Received JSON data (request.json):", request.json)
        return jsonify({"status": "success", "message": "JSON data received!", "data": request.json})
    else:
        return jsonify({"status": "error", "message": "No data received!"}), 400

