from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    students = db.get_all_students()
    return jsonify(students), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    # Getting the request body - replace with your implementation
    student_data = request.json
    if not student_data or "name" not in student_data or "course" not in student_data:
        return jsonify({"error": "name and course are required"}), 404

    # Get the students' name,course and mark from dict
    name = student_data["name"]
    course = student_data["course"]
    mark = student_data.get("mark")

    try:
        student = db.insert_student(name, course, mark)
        return jsonify(student), 200
    except Exception:
        return jsonify({"error": "Failed to create student!"}),  404


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    # replace with your implementation
    student_data = request.json

    # Check whether is empty
    if not student_data:
        return jsonify({"error": "Request body is required!"}), 404

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark")

    # Use internal method to update student
    updated = db.update_student(student_id, name=name, course=course, mark=mark)
    # Error fallback
    if updated is None:
        return jsonify({"error": "Student not found!"}), 404
    return jsonify(updated), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    # replace with your implementation
    result = db.delete_student(student_id)
    if result is None:
        return jsonify({"error": "Student not found!"}), 404

    return jsonify(result), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    # replace with your implementation
    students = db.get_all_students()
    # Iter marks
    marks = [s["mark"] for s in students  if isinstance(s.get("mark"), int)]

    if not marks:
        return jsonify({"count": 0, "average": 0, "min": 0, "max": 0}), 200
    return jsonify({
        "count": len(marks),
        "average": round(sum(marks) / len(marks), 2),
        "min": min(marks),
        "max": max(marks),
    }), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
