from fastapi import FastAPI
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

@app.post("/students")
def add_student(student: Student):

    for s in students:
        if s["code"] == student.code:
            return {"message": "Code đã tồn tại"}

    if student.name == "":
        return {"message": "Name không được rỗng"}

    if student.email == "":
        return {"message": "Email không được rỗng"}

    if student.age <= 0:
        return {"message": "Age phải lớn hơn 0"}

    new_student = {
        "id": len(students) + 1,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }

    students.append(new_student)

    return {
        "message": "Thêm học viên thành công",
        "data": new_student
    }

@app.get("/students")
def get_students(keyword: str = None,
                 min_age: int = None,
                 max_age: int = None):

    result = students

    if keyword:
        result = [
            s for s in result
            if keyword.lower() in s["name"].lower()
            or keyword.lower() in s["code"].lower()
            or keyword.lower() in s["email"].lower()
        ]

    if min_age is not None:
        result = [s for s in result if s["age"] >= min_age]

    if max_age is not None:
        result = [s for s in result if s["age"] <= max_age]

    return {
        "message": "Danh sách học viên",
        "data": result
    }

@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return student

    return {"message": "Student not found"}

@app.put("/students/{student_id}")
def update_student(student_id: int, new_student: Student):

    for student in students:

        if student["id"] == student_id:

            for s in students:
                if s["code"] == new_student.code and s["id"] != student_id:
                    return {"message": "Code đã tồn tại"}

            if new_student.name == "":
                return {"message": "Name không được rỗng"}

            if new_student.email == "":
                return {"message": "Email không được rỗng"}

            if new_student.age <= 0:
                return {"message": "Age phải lớn hơn 0"}

            student["code"] = new_student.code
            student["name"] = new_student.name
            student["email"] = new_student.email
            student["age"] = new_student.age

            return {
                "message": "Cập nhật thành công",
                "data": student
            }

    return {"message": "Student not found"}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return {"message": "Xóa thành công"}

    return {"message": "Student not found"}
