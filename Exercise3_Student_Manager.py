
from tkinter import *
from tkinter import messagebox, simpledialog
import os

# -------------------------------
# Student class holds all student information and logic
# -------------------------------
class Student:
    def __init__(self, code, name, marks, exam):
        self.code = code                      # Student code (unique identifier, stored as string)
        self.name = name                      # Student name (string)
        self.marks = list(map(int, marks))    # Convert 3 coursework marks from strings to integers
        self.exam = int(exam)                 # Convert exam mark from string to integer
        self.coursework_total = sum(self.marks)   # Total of 3 coursework marks (out of 60)
        self.total = self.coursework_total + self.exam   # Combined total mark (coursework + exam)
        self.percent = round((self.total / 160) * 100, 2) # Calculate overall percentage (160 is the max total)
        self.grade = self.get_grade()         # Determine letter grade based on percentage

    # Determine grade based on percentage range
    def get_grade(self):
        p = self.percent
        if p >= 70: return 'A'
        elif p >= 60: return 'B'
        elif p >= 50: return 'C'
        elif p >= 40: return 'D'
        else: return 'F'

    # Return a formatted summary string for displaying in the text area
    def get_summary(self):
        return (f"Name: {self.name}\n"
                f"Number: {self.code}\n"
                f"Coursework Total: {self.coursework_total}\n"
                f"Exam Mark: {self.exam}\n"
                f"Overall Percentage: {self.percent:.2f}%\n"
                f"Grade: {self.grade}\n")

# -------------------------------
# Functions for loading and saving students from/to file
# -------------------------------
def load_students(fn):
    """Load students from a file and return a list of Student objects"""
    students = []  # Empty list to hold all Student objects
    try:
        if os.path.exists(fn):  # Only read if the file exists
            with open(fn) as f:
                n = int(f.readline())  # First line = number of students
                for line in f:
                    # Split each line into parts (code, name, 3 marks, exam)
                    items = line.strip().split(',')
                    if len(items) == 6:  # Make sure line has all fields
                        code, name, m1, m2, m3, exam = items
                        # Create a new Student object and add to list
                        students.append(Student(code, name, [m1, m2, m3], exam))
    except Exception as e:
        # If reading fails, show an error message
        messagebox.showerror("Error", f"Error loading file: {e}")
    return students

def save_students(fn, students):
    """Save the list of Student objects to a file"""
    # Make sure the directory exists before writing file
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    try:
        with open(fn, 'w') as f:
            # First line = number of students
            f.write(str(len(students)) + "\n")
            # Write each student's details in one line (CSV format)
            for s in students:
                f.write(f"{s.code},{s.name},{s.marks[0]},{s.marks[1]},{s.marks[2]},{s.exam}\n")
    except Exception as e:
        # Show error message if saving fails
        messagebox.showerror("Error", f"Error saving file: {e}")

# -------------------------------
# Main Application Window Class (Tkinter GUI)
# -------------------------------
class StudentManager(Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Manager")                   # Title of main window
        self.configure(bg='#001f4d')                   # Set navy blue background
        self.filename = "resources/studentMarks.txt"   # File path to save student data
        self.students = load_students(self.filename)   # Load student data from file
        self.setup_gui()                               # Create and display GUI components

    # --------------------------------------------
    # GUI layout setup — creates all buttons, labels, and text areas
    # --------------------------------------------
    def setup_gui(self):
        # App title label
        Label(self, text="Student Manager", font=("Arial", 18, "bold"), bg='#001f4d', fg='white').pack(pady=10)

        # Frame for menu buttons (organizes layout neatly)
        btn_frame = Frame(self, bg='#001f4d')
        btn_frame.pack(pady=5)

        # Row 1: main actions - view, sort, and stats
        Button(btn_frame, text="View All Student Records", command=self.view_all, width=20, bg='white', fg='#001f4d').grid(row=0, column=0, padx=4)
        Button(btn_frame, text="Show Highest Score", command=self.show_highest, width=16, bg='white', fg='#001f4d').grid(row=0, column=1, padx=4)
        Button(btn_frame, text="Show Lowest Score", command=self.show_lowest, width=16, bg='white', fg='#001f4d').grid(row=0, column=2, padx=4)
        Button(btn_frame, text="Sort Asc", command=lambda:self.sort_records(True), width=10, bg='white', fg='#001f4d').grid(row=0,column=3,padx=4)
        Button(btn_frame, text="Sort Desc", command=lambda:self.sort_records(False), width=10, bg='white', fg='#001f4d').grid(row=0,column=4,padx=4)

        # Row 2: student management buttons - add, delete, update
        Button(btn_frame, text="Add Student", command=self.add_student_popup, width=13, bg='white', fg='#001f4d').grid(row=1,column=0,pady=5)
        Button(btn_frame, text="Delete Student", command=self.delete_student_popup, width=13, bg='white', fg='#001f4d').grid(row=1,column=1,pady=5)
        Button(btn_frame, text="Update Student", command=self.update_student_popup, width=13, bg='white', fg='#001f4d').grid(row=1,column=2,pady=5)

        # Frame for viewing individual student records
        self.ind_frame = Frame(self, bg='#001f4d')
        self.ind_frame.pack(pady=10)
        Label(self.ind_frame, text="View Individual Student Record:", font=("Arial",12), bg='#001f4d', fg='white').grid(row=0, column=0)

        # Dropdown menu setup for student selection
        self.student_var = StringVar()
        self.update_dropdown()                           # Populate dropdown with student names
        self.student_dropdown.grid(row=0, column=1, padx=8)
        Button(self.ind_frame, text="View Record", command=self.view_individual, width=12, bg='white', fg='#001f4d').grid(row=0, column=2)

        # Text widget for displaying records, summaries, or messages
        self.txt = Text(self, width=60, height=15, font=("Consolas", 10), bg='#001f4d', fg='white', insertbackground='white')
        self.txt.pack(pady=10)

    # --------------------------------------------
    # Update the dropdown list whenever data changes
    # --------------------------------------------
    def update_dropdown(self):
        names = [s.name for s in self.students]  # Extract all student names
        menu = OptionMenu(self.ind_frame, self.student_var, *names)
        self.student_dropdown = menu
        menu.config(width=25, bg='white', fg='#001f4d')
        menu.grid(row=0, column=1, padx=8)

    # --------------------------------------------
    # Display all students and overall average
    # --------------------------------------------
    def view_all(self):
        self.txt.delete(1.0, END)  # Clear previous text
        total_percent = 0
        for s in self.students:
            self.txt.insert(END, s.get_summary() + "\n")  # Add each student’s summary
            total_percent += s.percent
        n = len(self.students)
        avg = total_percent / n if n else 0
        self.txt.insert(END, f"\nNumber of Students: {n}\nAverage Percentage: {avg:.2f}%")

    # --------------------------------------------
    # Display a single student's record based on dropdown selection
    # --------------------------------------------
    def view_individual(self):
        name = self.student_var.get()  # Get selected name from dropdown
        found = [s for s in self.students if s.name == name]
        self.txt.delete(1.0, END)
        if found:
            self.txt.insert(END, found[0].get_summary())
        else:
            self.txt.insert(END, "Student not found.")

    # --------------------------------------------
    # Show the student with the highest score
    # --------------------------------------------
    def show_highest(self):
        if not self.students: return
        top = max(self.students, key=lambda s: s.percent)
        self.txt.delete(1.0, END)
        self.txt.insert(END, top.get_summary())

    # --------------------------------------------
    # Show the student with the lowest score
    # --------------------------------------------
    def show_lowest(self):
        if not self.students: return
        low = min(self.students, key=lambda s: s.percent)
        self.txt.delete(1.0, END)
        self.txt.insert(END, low.get_summary())

    # --------------------------------------------
    # Sort students by their percentage (ascending or descending)
    # --------------------------------------------
    def sort_records(self, ascending=True):
        self.students.sort(key=lambda s: s.percent, reverse=not ascending)
        self.update_dropdown()
        self.view_all()

    # --------------------------------------------
    # Add a new student through a popup form
    # --------------------------------------------
    def add_student_popup(self):
        win = Toplevel(self)
        win.title("Add Student")
        win.configure(bg='#001f4d')
        win.geometry("300x300")

        # Fields for entering student details
        fields = ['Code(1000-9999)', 'Name', 'Mark1(0-20)', 'Mark2(0-20)', 'Mark3(0-20)', 'Exam(0-100)']
        entries = []
        for i, f in enumerate(fields):
            Label(win, text=f, bg='#001f4d', fg='white').grid(row=i, column=0, pady=5, sticky=W)
            ent = Entry(win, bg='white', fg='#001f4d')
            ent.grid(row=i, column=1, pady=5)
            entries.append(ent)

        # Inner function that processes the input when user clicks "Add Student"
        def submit():
            try:
                code = entries[0].get()
                if not code.isdigit() or not (1000 <= int(code) <= 9999):
                    raise ValueError("Student code must be 1000-9999.")
                name = entries[1].get()
                marks = [int(entries[2].get()), int(entries[3].get()), int(entries[4].get())]
                if any(m < 0 or m > 20 for m in marks):
                    raise ValueError("Coursework marks must be 0-20.")
                exam = int(entries[5].get())
                if exam < 0 or exam > 100:
                    raise ValueError("Exam mark must be 0-100.")
                for s in self.students:
                    if s.code == code or s.name.lower() == name.lower():
                        raise ValueError("Duplicate code or name.")
                self.students.append(Student(code, name, marks, exam))
                save_students(self.filename, self.students)
                self.update_dropdown()
                self.view_all()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        Button(win, text="Add Student", command=submit, bg='white', fg='#001f4d').grid(row=len(fields),column=0,columnspan=2,pady=10)

    # --------------------------------------------
    # Delete an existing student record
    # --------------------------------------------
    def delete_student_popup(self):
        win = Toplevel(self)
        win.title("Delete Student")
        win.configure(bg='#001f4d')
        win.geometry("300x120")
        Label(win, text="Enter Name or Code:", bg='#001f4d', fg='white').grid(row=0, column=0, pady=5)
        ent = Entry(win, bg='white', fg='#001f4d')
        ent.grid(row=0, column=1, pady=5)

        def submit():
            val = ent.get().strip()
            idx = -1
            for i, s in enumerate(self.students):
                if s.code == val or s.name.lower() == val.lower():
                    idx = i
                    break
            if idx != -1:
                if messagebox.askyesno("Confirm", f"Delete {self.students[idx].name}?"):
                    del self.students[idx]
                    save_students(self.filename, self.students)
                    self.update_dropdown()
                    self.view_all()
                    win.destroy()
            else:
                messagebox.showerror("Error", "Student not found.")

        Button(win, text="Delete", command=submit, bg='white', fg='#001f4d').grid(row=1, column=0, columnspan=2, pady=10)

    # --------------------------------------------
    # Update an existing student's information
    # --------------------------------------------
    def update_student_popup(self):
        win = Toplevel(self)
        win.title("Update Student")
        win.configure(bg='#001f4d')
        win.geometry("340x320")
        Label(win, text="Enter Name or Code:", bg='#001f4d', fg='white').grid(row=0, column=0, pady=6)
        ent = Entry(win, bg='white', fg='#001f4d')
        ent.grid(row=0, column=1, pady=6)

        # Dropdown field for selecting which part to update
        fields = ['Name', 'Code', 'Mark1', 'Mark2', 'Mark3', 'Exam']
        Label(win, text="Select field to update:", bg='#001f4d', fg='white').grid(row=1, column=0, pady=6)
        field_var = StringVar(win)
        field_var.set(fields[0])
        OptionMenu(win, field_var, *fields).grid(row=1, column=1, pady=6)
        Label(win, text="New Value:", bg='#001f4d', fg='white').grid(row=2, column=0, pady=6)
        new_val_ent = Entry(win, bg='white', fg='#001f4d')
        new_val_ent.grid(row=2, column=1, pady=6)

        def submit():
            val = ent.get().strip()
            idx = -1
            for i, s in enumerate(self.students):
                if s.code == val or s.name.lower() == val.lower():
                    idx = i
                    break
            if idx == -1:
                messagebox.showerror("Error", "Student not found.")
                return
            field = field_var.get()
            new_val = new_val_ent.get().strip()
            s = self.students[idx]
            try:
                if field == 'Name':
                    if any(x.name.lower() == new_val.lower() for x in self.students):
                        raise ValueError("Duplicate name.")
                    s.name = new_val
                elif field == 'Code':
                    if not new_val.isdigit() or not (1000 <= int(new_val) <= 9999):
                        raise ValueError("Code must be 1000-9999.")
                    if any(x.code == new_val for x in self.students):
                        raise ValueError("Duplicate code.")
                    s.code = new_val
                elif field in ['Mark1', 'Mark2', 'Mark3']:
                    idxm = int(field[-1]) - 1
                    mark = int(new_val)
                    if mark < 0 or mark > 20:
                        raise ValueError("Mark must be 0-20.")
                    s.marks[idxm] = mark
                elif field == 'Exam':
                    mark = int(new_val)
                    if mark < 0 or mark > 100:
                        raise ValueError("Exam must be 0-100.")
                    s.exam = mark
                # After updating marks or exam, recalculate totals and grade
                s.coursework_total = sum(s.marks)
                s.total = s.coursework_total + s.exam
                s.percent = round((s.total / 160) * 100, 2)
                s.grade = s.get_grade()
                save_students(self.filename, self.students)
                self.update_dropdown()
                self.view_all()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        Button(win, text="Update", command=submit, bg='white', fg='#001f4d').grid(row=3,column=0,columnspan=2,pady=14)

# -------------------------------
# Run the application when script is executed directly
# -------------------------------
if __name__ == "__main__":
    app = StudentManager()
    app.mainloop()