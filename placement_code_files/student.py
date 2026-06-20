import json
import os
import uuid

DATA_FILE = os.path.join(os.path.dirname(__file__), 'students.json')


def load_students():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_students(students):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(students, file, indent=4)


def get_students():
    return load_students()


def add_student(name, age, department, percentage):
    students = load_students()
    student = {
        'id': str(uuid.uuid4()),
        'name': name,
        'age': age,
        'department': department,
        'percentage': percentage
    }
    students.append(student)
    save_students(students)
    return student


def find_student(student_id):
    students = load_students()
    for student in students:
        if student['id'] == student_id:
            return student
    return None


def update_student(student_id, name, age, department, percentage):
    students = load_students()
    updated = False
    for student in students:
        if student['id'] == student_id:
            student['name'] = name
            student['age'] = age
            student['department'] = department
            student['percentage'] = percentage
            updated = True
            break

    if updated:
        save_students(students)
    return updated


def delete_student(student_id):
    students = load_students()
    new_students = [s for s in students if s['id'] != student_id]

    if len(new_students) == len(students):
        return False

    save_students(new_students)
    return True


# CLI helpers

def add_student_cli():
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    department = input("Enter Department: ")
    percentage = float(input("Enter Percentage: "))
    add_student(name, age, department, percentage)
    print("✅ Student added successfully!\n")


def view_students():
    students = get_students()
    if not students:
        print("⚠ No student records found.\n")
        return

    print("\n--- Student Records ---")
    for i, student in enumerate(students, start=1):
        print(f"\nStudent {i}:")
        print(f"Name       : {student['name']}")
        print(f"Age        : {student['age']}")
        print(f"Department : {student['department']}")
        print(f"Percentage : {student['percentage']}")
    print()


def search_student():
    name = input("Enter student name to search: ")
    students = get_students()
    for student in students:
        if student['name'].lower() == name.lower():
            print("\n✅ Student Found:")
            print(student)
            return

    print("❌ Student not found.\n")


def update_student_cli():
    student_id = input("Enter student ID to update: ")
    student = find_student(student_id)
    if not student:
        print("❌ Student not found.\n")
        return

    print("Enter new details:")
    student['name'] = input("Enter Name: ")
    student['age'] = int(input("Enter Age: "))
    student['department'] = input("Enter Department: ")
    student['percentage'] = float(input("Enter Percentage: "))
    update_student(student_id, student['name'], student['age'], student['department'], student['percentage'])
    print("✅ Student updated successfully!\n")


def delete_student_cli():
    student_id = input("Enter student ID to delete: ")
    if delete_student(student_id):
        print("✅ Student deleted successfully!\n")
    else:
        print("❌ Student not found.\n")


def main():
    while True:
        print("===== Student Database Menu =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student_cli()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student_cli()
        elif choice == "5":
            delete_student_cli()
        elif choice == "6":
            print("Exiting program...")
            break
        else:
            print("❌ Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()

