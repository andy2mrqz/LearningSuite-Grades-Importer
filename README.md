# LearningSuite-Grades-Importer
Allows professors and TAs to easily grade assignments and import the grades to Learning Suite.

This module creates a CSV file of student grades suitable for import to Learning Suite.
The goal is to make grading easier by allowing a quick place to enter grades
for multiple students across multiple assignments.  Before, going to the scores
section and scrolling around looking for the student and assignment was a
little tedious.

## Kinda Quick Setup
1. `git clone https://github.com/andy2mrqz/LearningSuite-Grades-Importer.git`
2. The students folder contains example CSV files of students and their Net IDs.  Go to
`Learning Suite > YourCourse 101 > Users > Enrolled Students > Show` to see an HTML table of student information.
You can highlight the whole table and copy it into a spreadsheet program, delete everything besides the first
two rows (Name and Net ID), and download as a CSV. The program currently looks for students by section in files
named like sec1.csv, sec2.csv ... sec100.csv. Place your CSV file in the students folder in this format, or modify
the `get_net_ids` function to change how you search for students and their Net IDs.
3. `$ python grader.py`
4. After going through the program, go to `Learning Suite > Grades > Import`
and import the CSV file that was created.  If you enter the assignment
names exactly as they are represented on Learning Suite, it will
intelligently match the columns in the CSV to the actual assignment.
Otherwise, you can simply choose which assignment you want to link a
column to.  Learning Suite shows a preview before you submit and any
changes are made.
