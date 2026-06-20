import os
from functools import wraps
from flask import Flask, jsonify, request, send_from_directory, session

from student import get_students, add_student, delete_student, update_student, find_student

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = os.getenv('SECRET_KEY', 'devsecret123')

VALID_USERNAME = 'admin'
VALID_PASSWORD = 'admin123'


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get('authenticated'):
            return jsonify({'error': 'Authentication required'}), 401
        return view_func(*args, **kwargs)
    return wrapped


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/session', methods=['GET'])
def api_session():
    return jsonify({'authenticated': session.get('authenticated', False)})


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        session['authenticated'] = True
        return jsonify({'status': 'ok'})

    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'status': 'logged_out'})


@app.route('/api/students', methods=['GET'])
@login_required
def api_get_students():
    return jsonify(get_students())


@app.route('/api/students', methods=['POST'])
@login_required
def api_add_student():
    data = request.get_json() or {}
    name = data.get('name')
    age = data.get('age')
    department = data.get('department')
    percentage = data.get('percentage')

    if not name or age is None or not department or percentage is None:
        return jsonify({'error': 'Missing required fields'}), 400

    student = add_student(name, age, department, percentage)
    return jsonify(student), 201


@app.route('/api/students/<student_id>', methods=['GET'])
@login_required
def api_get_student(student_id):
    student = find_student(student_id)
    if student:
        return jsonify(student)
    return jsonify({'error': 'Student not found'}), 404


@app.route('/api/students/<student_id>', methods=['PUT'])
@login_required
def api_update_student(student_id):
    data = request.get_json() or {}
    name = data.get('name')
    age = data.get('age')
    department = data.get('department')
    percentage = data.get('percentage')

    if not name or age is None or not department or percentage is None:
        return jsonify({'error': 'Missing required fields'}), 400

    if update_student(student_id, name, age, department, percentage):
        student = find_student(student_id)
        return jsonify(student)

    return jsonify({'error': 'Student not found'}), 404


@app.route('/api/students/<student_id>', methods=['DELETE'])
@login_required
def api_delete_student(student_id):
    if delete_student(student_id):
        return jsonify({'status': 'deleted'})
    return jsonify({'error': 'Student not found'}), 404


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)


if __name__ == '__main__':
    app.run(debug=True)
