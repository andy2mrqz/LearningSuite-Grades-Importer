"""This module creates a CSV file suitable for import to Learning Suite.
The goal is to make grading easier by allowing a quick place to enter grades
for multiple students across multiple assignments.  Before, going to the scores
section and scrolling around looking for the student and assignment was a
little tedious.  So why not make this needlessly complex to save a few seconds?

Example:
    $ python grader.py

    After going through the program, go to Learning Suite > Grades > Import
    and import the CSV file that was created.  If you enter the assignment
    names exactly as they are represented on Learning Suite, it will
    intelligently match the columns in the CSV to the actual assignment.
    Otherwise, you can simply choose which assignment you want to link a
    column to.  Learning Suite shows a preview before you submit and any
    changes are made.

Author:
    Andrew Marquez - andy2mgcc@gmail.com
"""
import os
import sys
import csv

# Global
cwd = sys.path[0]

def get_section():
    """Pick which section you are grading"""
    section = ""
    # Hard coded section numbers. Change to suit your needs
    while section not in ("1", "2", "q"):
        print("Which section are you grading?  Enter 1 or 2 (q to exit)")
        section = input("> ")
        print()

    return section

def create_file(s):
    """Name the output file.  Provides a default"""
    # Ask for valid filename and require .csv format
    extension = ""
    while extension != ".csv":
        print(f"Name the output file.  Default: sec{s}-grades.csv (Enter)")
        filename = input("> ") or f"sec{s}-grades.csv"""
        print()
        _, extension = os.path.splitext(filename)

    # Create the file
    try:
        open(os.path.join(cwd, filename), "w+")
    except:
        print("There has been an error.  Try again.")
        print()
        create_file(s)

    return filename

def get_assignments():
    """Enter comma delimeted assignments to be graded"""
    print("Enter assignment names separated by commas")
    assignments = input("> ")
    print()

    # Return list of assignments and strip leading/trailing whitespace
    return [a.strip(" ") for a in assignments.split(",")]

def create_headers(csvfile, assignments):
    """Create the CSV headers for importing"""
    header = ["Net ID"] # Headers start with Net ID, then the assignments
 
    header.extend(assignments)

    # Write the headers
    w = csv.writer(open(csvfile, "w+", newline=""), delimiter=",")
    w.writerow(header)

def write_student_grades(csvfile, net_id, grades):
    """Write the student's net_id and grades to CSV file
    """
    row = [net_id] # Headers start with Net ID, then the grades

    row.extend(grades)

    # Write the grades
    w = csv.writer(open(csvfile, "a", newline=""), delimiter=",")
    w.writerow(row)

def get_net_ids(name, section):
    """Given part or all of a student name and section, look up
    their net ID from a file located at relative location students/sec#.csv
    """
    # Open file for reading
    student_file = os.path.join(cwd, f"students/sec{section}.csv")
    student_list = csv.reader(open(student_file, "r"), delimiter=",")

    # Clean name into list of words w/o punctuation to make searching better
    # Originally just the provided name
    name_parts = "".join(name.split(",")).lower().split(" ")

    options = []
    for student in student_list:
        # Clean student to have no punctuation to make matching better
        # Originally just student[0]
        student_np = "".join(student[0].split(",")).lower()
        # Check if all the search criteria are somewhere in the name
        combined = [part for part in name_parts if part in student_np]
        if name_parts == combined:
            options.append(student)

    return options

def get_candidate(section):
    """Get the student to grade based on search criteria.  If more
    than one student match, allow selection from list
    """
    print("Enter a student's name to grade (q to finish)")
    student_name = input("> ")
    print()
    if student_name == "q":
        return "q"
    else:
        prospectives = get_net_ids(student_name, section)
        if prospectives:
            if len(prospectives) == 1:
                return prospectives[0]
            else:
                print("Select the student to grade")
                for idx, student  in enumerate(prospectives):
                    print(f"{idx+1}: {student[0]}")
                print(f"{len(prospectives)+1}: None of the above")
                print()
                selection = int(input("> "))
                print()
                # If they select "None of the above"
                if selection == len(prospectives) + 1:
                    return
                return prospectives[selection - 1]
        else:
            print("No students found by that name")
            print()
            return None
    
def grade(csvfile, section, assignments):
    """Enter students to grade and enter the grades for each assignment"""
    done = False
    while not done:
        student = get_candidate(section)
        if student == "q":
            done = True
        elif student is None:
            continue
        else:
            name, net_id = student # Unpack values from the list
            grades = [] # Corresponds to the assignments list
            print(f"You chose {name}")
            print("Continue? (Y/n)")
            if input("> ") == "n":
                print()
                continue

            print()
            print(f"You will be grading {', '.join(assignments)}")
            print()
            for assignment in assignments:
                print(f"Enter {name}'s grade for {assignment}")
                grade = input("> ")
                print()
                grades.append(grade)

            # Write student net_id and grades to file
            write_student_grades(csvfile, net_id, grades)

if __name__ == "__main__":
    section = get_section()
    if section != "q":
        csvfile = create_file(section)
        csvfile = os.path.join(cwd, csvfile)
        assignments = get_assignments()
        create_headers(csvfile, assignments)
        grade(csvfile, section, assignments)
        print()
        print("Great, you've made it this far!  Now you can find the file")
        print("you created and import it to LS")
        print()
        input("Goodbye\n")
    else:
        print("Goodbye")
