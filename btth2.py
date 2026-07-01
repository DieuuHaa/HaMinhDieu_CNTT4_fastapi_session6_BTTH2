from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]

class Student(BaseModel):
    code: str
    name: str
    email: str
    age: int

def find_student(student_id):
    for student in students:
        if student["id"] == student_id:
            return student
    return None

@app.post("/students")
def add_student(student: Student):
    if student.name.strip() == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if student.email.strip() == "":
        raise HTTPException(status_code=400, detail="Email cannot be empty")
    if student.age <= 0:
        raise HTTPException(status_code=400, detail="Age must be greater than 0")
    for s in students:
        if s["code"] == student.code:
            raise HTTPException(status_code=400, detail="Code already exists")
    new_student = student.dict()
    new_student["id"] = len(students) + 1
    students.append(new_student)
    return {
        "message": "Student added successfully",
        "student": new_student
    }

@app.get("/students")
def get_students(
    keyword: str = Query(None),
    min_age: int = Query(None),
    max_age: int = Query(None)
):
    result = students
    if keyword:
        keyword = keyword.lower()
        result = [
            s for s in result
            if keyword in s["name"].lower()
            or keyword in s["code"].lower()
            or keyword in s["email"].lower()
        ]
    if min_age is not None:
        result = [s for s in result if s["age"] >= min_age]
    if max_age is not None:
        result = [s for s in result if s["age"] <= max_age]
    return result

@app.get("/students/{student_id}")
def get_student(student_id: int):
    student = find_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    student = find_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if updated_student.name.strip() == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if updated_student.email.strip() == "":
        raise HTTPException(status_code=400, detail="Email cannot be empty")
    if updated_student.age <= 0:
        raise HTTPException(status_code=400, detail="Age must be greater than 0")
    for s in students:
        if s["code"] == updated_student.code and s["id"] != student_id:
            raise HTTPException(status_code=400, detail="Code already exists")
    student["code"] = updated_student.code
    student["name"] = updated_student.name
    student["email"] = updated_student.email
    student["age"] = updated_student.age
    return {
        "message": "Student updated successfully",
        "student": student
    }

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    student = find_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    students.remove(student)
    return {
        "message": "Student deleted successfully"
    }