# Simple Online Judge

A minimal, self-hosted online judge for teaching Python. Students log in, solve
coding questions organized in sections, and see instant feedback + scoreboard.
Admins manage users, sections, questions, resources, and shared files entirely
from the web UI.


## Quick start

```bash
git clone https://github.com/cahidenes/simple-online-judge.git
cd simple-online-judge
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
sh run.sh
# open http://localhost:8080
```

> **WARNING: change the admin password after install.**
>
> Default login is `admin` / `admin`. Go to `Users > Edit` on `admin`
> and set a new password first thing.

## What students see

Students log in and see:

- `Home`: list of sections with progress (`done / total`).
- Click a section, then a question. They write Python code and press Submit.
- They get instant result: Correct / Wrong / Partial, with error or expected output.
- `Resources`: lecture notes.
- `Scoreboard`: who solved what, total points.

Students cannot see admin menus. Hidden/inactive sections are invisible to them.

## Admin use

Log in as `admin`. You will see extra menus on top:
`Edit Resources, Questions, Users, Sections, Files`.

### Users

- `Users` lists all users.
- `Add User`: enter Username, Password, Name. Tick `Visible` if they should appear on scoreboard. Untick for test accounts.
- `Edit`: change password, name, or rename user. This is also where you change the admin password.

### Sections

Sections are groups of questions, e.g. Week 1, Week 2.

- `Sections` lists all sections. `Add Section` makes a `New Section`, then rename it and press `Save`.
- You can drag rows to reorder.
- You cannot delete a section that still has questions. Move/delete questions first.
- Three checkboxes per section:
  - `Visible`: if off, students cannot see it at all. Use to hide drafts.
  - `Active`: if off, students see it but cannot open/submit. Use to close an old week.
  - `Points`: if off, questions give only 0.1 participation points. Use for practice material.
- Typical flow: keep new week `Visible off` while preparing, turn all three on when class starts, turn `Active` off when week ends.

### Questions

- `Questions` lists all questions grouped by section. Use search or tag pills to filter. Drag a question to reorder or move it to another section.
- `Add Question` creates one. Click a title on a question page as admin to edit it.
- Main fields: `Title`, `Question body`, `Points`, `Tags`, `Section`.
- `Question body` is **HTML**. Write plain text or simple HTML like `<b>`, `<ul><li>`, `<pre>`, `<img src="/files/...">`. What you type is what students see.
- `Pre / Tmp / Post solution`: code wrapped around student code when run. `Tmp` is the starter code students see. Often you can leave them empty.
- `Env Files`: file names from `Files` page, comma separated. They are copied next to student code when it runs. Use for CSV/data files.
- `Points`: Points of the questions. students will get this amout of point when it is fully solved.
- Question check types (`Judge Type`):
  - `testcaseonly`: fixed input/output pairs. Tick `show` to show the case to students, untick to keep it hidden.
  - `solution`: you give a reference `Solution` + a `Generator` that prints random inputs. Server tests student code on 100 random inputs against your solution.
  - `checker`: you write a `Checker` script for flexible grading. Empty output = full points, or output `0.5|message` for partial points.
  - `outputonly`: student code must print one fixed output. No `input()` allowed.
  - `guessinput`: students see code + output and must guess the input.
  - `codegolf`: like outputonly, but shorter code = more points. Set score formula with `c` = character count, e.g. `max(0, 1 - c/100)`.
  - `manual`: no auto check. Submission waits, admin grades it from the scoreboard (click purple cell, then judge).

### Resources

- `Edit Resources > Add Resource`: enter `Title` + text + `Save`. Drag to reorder.
- Text is **Markdown**. Use `## heading`, `- list`, `**bold**`, links, etc.
- Special blocks become runnable code for students:

  ````markdown
  ```
  print("hello")
  ```
  ````

  Code with input (separate with `---`):

  ````markdown
  ```
  print(input())
  ---
  hello
  ```
  ````

- Lines starting with `| ` become highlighted boxes:
  `| Read this carefully.`

## Security note

Credentials are stored in plain text and login uses plain cookies. There is no encryption.

Student code runs on your server. The `import`/`open` blocking is only a simple check — a clever student can bypass it and take over the server. Only give accounts to people you trust, and run this on a separate machine/VM with nothing valuable on it.
