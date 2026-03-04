import json
import os
import time

# Colors
RED, GREEN, YELLOW, CYAN, RESET = "\033[91m", "\033[92m", "\033[93m", "\033[96m", "\033[0m"

# File
student_history = "Assignment/student_history.json"

# Majors (only 2)
MAJORS = ["Computer Science", "Network Engineering"]

# Year handling
YEAR_NAMES = ["1", "2", "3", "4"]
YEAR_DISPLAY = {"1":"Year 1","2":"Year 2","3":"Year 3","4":"Year 4"}

# Curriculum
CURRICULUM = {
    "Computer Science": {
        "Year 1": ["Programming", "Math", "Computer Basics"],
        "Year 2": ["Data Structures", "Algorithms", "Operating Systems"],
        "Year 3": ["Databases", "Software Engineering", "Networks"],
        "Year 4": ["AI", "Project", "Advanced Topics"]
    },
    "Network Engineering": {
        "Year 1": ["Networking Basics", "Hardware", "Math"],
        "Year 2": ["Routing", "Protocols", "Linux"],
        "Year 3": ["Wireless", "Security", "Cloud"],
        "Year 4": ["Advanced Networks", "Cyber Defense", "Project"]
    }
}

# ========== FILE FUNCTIONS ==========
def load_data():
    os.makedirs("Assignment", exist_ok=True)
    try:
        return json.load(open(student_history)) if os.path.exists(student_history) else []
    except:
        return []

def save_data(students):
    json.dump(students, open(student_history, 'w'), indent=2)

def find_student(students, sid):
    """Find student by ID - returns index and student"""
    for i in range(len(students)):
        if students[i]['id'] == sid:
            return i, students[i]
    return None, None

# ========== LOGIN ==========
def login():
    print("=" * 48)
    print("\t WELCOME TO NORTON UNIVERSITY")
    print("\t  STUDENT MANAGEMENT SYSTEM")
    print("=" * 48)
    print("=" * 18, "Login Page", "=" * 18)
    print("   Please login to get access to the system")
    print("-" * 48, "\n")
    
    for attempt in range(3, 0, -1):
        if input("Enter PIN: ") == "1234":
            print(GREEN + "Access granted." + RESET)
            print("Loading", end="", flush=True)
            for _ in range(3):
                time.sleep(0.3)
                print(".", end="", flush=True)
            print(GREEN + "\n✓ Login successful!" + RESET)
            return True
        print(RED + f"Wrong PIN! {attempt-1} attempts left." + RESET)
    print(RED + "System locked. You Are Scam😁😁" + RESET)
    return False


# ========== MENU ==========
def show_menu():
    print("\n" + "="*50)
    print("\t    STUDENT MANAGEMENT SYSTEM")
    print("="*50)
    print("1.  Student Management System")
    print("2.  Add / Search Student by ID")
    print("3.  Update / Delete Student (By ID)")
    print("4.  Exit")
    print("-"*50)
    

# ========== OPTION 1: VIEW STUDENTS MENU ==========
def Student_Management_System(students):
    print("View students menu with options")
    while True:
        print("\n" + "="*40)
        print(" Student Management System")
        print("="*40)
        print("1. View Student By Major (with Subjects) 🧑‍🎓")
        print("2. View All Students")
        print("3. Back to Main Menu")
        print("-"*40)
        
        choice = input("To view in each of our system, Choose (1-3): ")
        
        if choice == "1":
            view_student_by_major(students)
        elif choice == "2":
            view_all_students(students)
        elif choice == "3":
            break
        else:
            print(RED + "Invalid choice." + RESET)
        
        input("\nPress Enter to continue...")

# ========== VIEW FUNCTIONS ==========
def view_student_by_major(students):
    print("View students grouped by major with curriculum")
    if not students:
        print(RED + "No students found." + RESET)
        return
    
    # Group students by major
    computer_science_student = []
    network_engineering_student = []
    
    for s in students:
        if s.get('major') == "Computer Science":
            computer_science_student.append(s)
        elif s.get('major') == "Network Engineering":
            network_engineering_student.append(s)
    
    # Show Computer Science students
    if computer_science_student:
        print(f"\n{YELLOW}{'='*45}")
        print("  COMPUTER SCIENCE")
        print('='*45 + RESET)
        print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Year':<10}")
        print("-"*45)
        
        for s in computer_science_student:
            year = YEAR_DISPLAY.get(s.get('year', 'N/A'), s.get('year', 'N/A'))
            print(f"{s.get('id','N/A'):<10} {s.get('name','N/A'):<20} "
                  f"{s.get('age','N/A'):<5} {year:<10}")
        
        # Show Computer Science curriculum
        print(f"\n{CYAN}Curriculum:{RESET}")
        for year in ["Year 1", "Year 2", "Year 3", "Year 4"]:
            if year in CURRICULUM["Computer Science"]:
                print(f"  {year}:")
                for subject in CURRICULUM["Computer Science"][year]:
                    print(f"    • {subject}")
    
    # Show Network Engineering students
    if network_engineering_student:
        print(f"\n{YELLOW}{'='*45}")
        print("  NETWORK ENGINEERING")
        print('='*45 + RESET)
        print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Year':<10}")
        print("-"*45)
        
        for s in network_engineering_student:
            year = YEAR_DISPLAY.get(s.get('year', 'N/A'), s.get('year', 'N/A'))
            print(f"{s.get('id','N/A'):<10} {s.get('name','N/A'):<20} "
                  f"{s.get('age','N/A'):<5} {year:<10}")
        
        # Show Network Engineering curriculum
        print(f"\n{CYAN}Curriculum:{RESET}")
        for year in ["Year 1", "Year 2", "Year 3", "Year 4"]:
            if year in CURRICULUM["Network Engineering"]:
                print(f"  {year}:")
                for subject in CURRICULUM["Network Engineering"][year]:
                    print(f"    • {subject}")

def view_all_students(students):
    """View all students in a table"""
    if not students:
        print(RED + "No students found." + RESET)
        return
    
    print(f"\n{'ID':<10} {'Name':<20} {'Age':<5} {'Year':<10} {'Major':<25}")
    print("-"*70)
    for s in students:
        year = YEAR_DISPLAY.get(s.get('year', 'N/A'), s.get('year', 'N/A'))
        print(f"{s.get('id','N/A'):<10} {s.get('name','N/A'):<20} {s.get('age','N/A'):<5} "
              f"{year:<10} {s.get('major','N/A'):<25}")

# ========== OPTION 2: ADD / SEARCH MENU ==========
def add_search_menu(students):
    """Menu for Add and Search options"""
    print("Manu For Add & Search Options")
    while True:
        print("\n" + "="*40)
        print(" ADD & SEARCH STUDENT")
        print("="*40)
        print("1. Add New Student")
        print("2. Search Student by ID")
        print("3. Back to Main Menu")
        print("-"*40)
        
        choice = input("Choose (1-3): ").strip()
        
        if choice == "1":
            add_student(students)
        elif choice == "2":
            search_student(students)
        elif choice == "3":
            break
        else:
            print(RED + "Invalid choice." + RESET)
        
        input("\nPress Enter to continue...")

# ========== ADD STUDENT ==========
def add_student(students):
    sid = input("Student ID: ").strip()
    
    # Check if ID exists
    index, existing = find_student(students, sid)
    if index is not None:
        print(RED + "ID exists!" + RESET)
        return
    
    name = input("Name: ").strip()
    age = input("Age: ").strip()
    
    # Select year
    print("\nYears:")
    for i, year in enumerate(YEAR_NAMES, 1):
        print(f"{i}. {YEAR_DISPLAY[year]}")
    try:
        year_idx = int(input("Select year (1-4): ")) - 1
        year = YEAR_NAMES[year_idx]
    except:
        print(YELLOW + "Using Year 1." + RESET)
        year = "1"
    
    # Select major
    print("\nMajors:")
    for i, major in enumerate(MAJORS, 1):
        print(f"{i}. {major}")
    try:
        major_idx = int(input("Select major (1-2): ")) - 1
        major = MAJORS[major_idx]
    except:
        print(YELLOW + "Using Computer Science." + RESET)
        major = "Computer Science"
    
    # Add student
    students.append({
        "id": sid,
        "name": name,
        "age": age,
        "year": year,
        "major": major,
        "scores": {}
    })
    save_data(students)
    print(CYAN + "✓ Student added!" + RESET)

# ========== SEARCH STUDENT ==========
def search_student(students):
    sid = input("Enter Student ID to search: ").strip()
    index, student = find_student(students, sid)
    
    if student is None:
        print(RED + "Student not found." + RESET)
        return
    
    year = YEAR_DISPLAY.get(student.get('year', 'N/A'), 'N/A')
    print(f"\nID: {student.get('id')}")
    print(f"Name: {student.get('name')}")
    print(f"Age: {student.get('age')}")
    print(f"Year: {year}")
    print(f"Major: {student.get('major')}")

# ========== OPTION 3: UPDATE / DELETE MENU ==========
def update_delete_menu(students):
    """Menu for Update and Delete options"""
    while True:
        print("\n" + "="*40)
        print(" UPDATE / DELETE STUDENT")
        print("="*40)
        print("1. Update Student Information")
        print("2. Delete Student")
        print("3. Back to Main Menu")
        print("-"*40)
        
        choice = input("Choose (1-3): ").strip()
        
        if choice == "1":
            update_student(students)
        elif choice == "2":
            delete_student(students)
        elif choice == "3":
            break
        else:
            print(RED + "Invalid choice." + RESET)
        
        input("\nPress Enter to continue...")

# ========== UPDATE STUDENT ==========
def update_student(students):
    """Update student information"""
    sid = input("Enter Student ID to update: ").strip()
    index, student = find_student(students, sid)
    
    if student is None:
        print(RED + "Student not found!" + RESET)
        return
    
    print(f"\nUpdating: {student.get('name')}")
    print("(Press Enter to keep current value)")
    
    # Update name
    new_name = input(f"Name [{student.get('name')}]: ").strip()
    if new_name:
        student['name'] = new_name
    
    # Update age
    new_age = input(f"Age [{student.get('age')}]: ").strip()
    if new_age:
        student['age'] = new_age
    
    # Update year
    print("\nSelect new year (or Enter to skip):")
    for i, year in enumerate(YEAR_NAMES, 1):
        print(f"{i}. {YEAR_DISPLAY[year]}")
    year_choice = input("Choice (1-4): ").strip()
    if year_choice:
        try:
            student['year'] = YEAR_NAMES[int(year_choice) - 1]
        except:
            print(RED + "Invalid choice. Year not updated." + RESET)
    
    # Update major
    print("\nSelect new major (or Enter to skip):")
    for i, major in enumerate(MAJORS, 1):
        print(f"{i}. {major}")
    major_choice = input("Choice (1-2): ").strip()
    if major_choice:
        try:
            student['major'] = MAJORS[int(major_choice) - 1]
        except:
            print(RED + "Invalid choice. Major not updated." + RESET)
    
    save_data(students)
    print(GREEN + "✓ Student updated successfully!" + RESET)

# ========== DELETE STUDENT ==========
def delete_student(students):
    """Delete a student from the system"""
    sid = input("Enter Student ID to delete: ").strip()
    index, student = find_student(students, sid)
    
    if student is None:
        print(RED + "Student not found!" + RESET)
        return
    
    # Show student info
    print(f"\nStudent Found:")
    print(f"Name: {student.get('name')}")
    print(f"Major: {student.get('major')}")
    
    # Confirm deletion
    confirm = input(f"\nAre you sure you want to delete {student.get('name')}? (y/n): ").strip().lower()
    
    if confirm == 'y':
        # Remove student
        removed = students.pop(index)
        save_data(students)
        print(GREEN + f"✓ Student {removed.get('name')} deleted successfully!" + RESET)
    else:
        print(YELLOW + "Deletion cancelled." + RESET)

# ========== MAIN ==========
def main():
    if not login():
        return
    
    students = load_data()
    
    while True:
        show_menu()
        choice = input("\n Option (1-4): ").strip()
        if choice == "1":
            Student_Management_System(students)
        elif choice == "2":
            add_search_menu(students)
        elif choice == "3":
            update_delete_menu(students)
        elif choice == "4":
            print(GREEN + "Goodbye! 👋" + RESET)
            break
        else:
            print(RED + "Invalid option." + RESET)
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
