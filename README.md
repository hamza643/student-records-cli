# Student Records CLI

A small command-line app to manage student records. Everything is saved in a JSON file so our data will still there the next time when we run it.

## How to run

You need Python and Git. On Windows PowerShell:

```powershell
git clone <https://github.com/hamza643/student-records-cli>
cd student-records-cli
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python main.py
```


## What it does

- Add a student (name, email, age, any number of subject grades)
- List students in a table, sorted by name
- Search by partial name or exact email
- Update a student's email, age, or one grade
- Delete a student by id, with a confirmation
- Show statistics: total students, average per subject, highest and lowest student, and how many fall in each grade band (A, B, C, F)
- Export the statistics to `report.txt` with a timestamp

Bad input (wrong email, age outside 5-25, grade outside 0-100, letters instead of numbers) gets rejected and the app asks again. Ids are never reused, even after a delete.

## Files

- `models.py`: the Student class and validation
- `storage.py`: all reading and writing of files
- `stats.py`: averages, grade bands, report text
- `main.py`: the menu (the only file that uses `input()` and `print()`)

## Things to know

- I built this on Python 3.9, not 3.12, I haven't tested it on 3.12.

- Everything is loaded into memory and rewritten on every change. That's fine for a school data , but it would be slow with 100,000 students.

- If students.json is corrupt, it is renamed to students.json.bak and the app starts empty, so no data is lost.