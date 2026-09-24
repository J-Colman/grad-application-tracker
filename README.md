# Graduate Application Tracker

A Python CLI for tracking graduate job opportunities, application deadlines, and progress.

I'm building this to organise my graduate job search while strengthening my Python, testing, Git and database skills.

## Current Status

The repository is set up with a few chosen tools and libraries prior to starting implementation:

- uv - Managing the project's environment and dependencies.
- Click - Handling command line user interaction.
- Ruff - Linting and formatting Python code.
- pytest - Running automated tests.

## Planned v1

- Add and list job opportunities.
- Show upcoming application deadlines.
- Track application statuses, such as saved, applied, and interviewed.
- Save records between sessions.

This first version will run locally in the terminal and store data in a JSON file. Later I plan to introduce PostgreSQL, an HTTP API and a TypeScript interface.

## Setup Instructions

Requires Python 3.14.5 and uv

Clone the repository then run these commands from it's root directory:

```bash
uv sync
uv run python -m grad_application_tracker.main
```

## Development Notes

I'll document useful lessons, bugs and design decisions as the project develops and grows. 

---

### 21/09/2026
I implemented the first useful piece of application logic: finding opportunities with deadlines inside a supplied date range.

Deadline may not be set for an opportunity so I made sure to check against `None` before comparison to exclude such cases.

I moved all of this logic into a function named `upcoming_opportunities()` which filters and sorts the data before returning a new list, and printing remains outside the function, keeping the application logic separate from displaying the data.

---

### 22/09/2026
I felt this was a good place to briefly stop and add some initial tests to the application, so I built a test file that ran nine tests on `main.py` to verify the robustness of its logic.

I also added a continuous integration workflow to the Github repo so these tests are automated and run on push.

I created the two data transformation functions to translate opportunities from an object to a dictionary and vice versa so I can pass data into and read data from JSON files. Naturally I built those two functions next, `save_opportunities` and `load_opportunities` implementing exactly the planned logic of saving opportunities to a JSON file.

---

### 23/09/2026

I refactored the main function logic to reflect and test the new abilities of the program.

Upon refactoring main, I realised an issue with the atomic save I had implemented. The `save_opportunities` function would first create the temporary file before even attempting to convert the opportunities to dictionaries, meaning that if for some reason there was an issue the second step, the `try/finally` blocks would never run and the temporary file would never be deleted. It was simply fixed by swapping the logic around so we attempted to convert the data first.

I added some new tests to ensure saving and loading data was working as expected.

---

### 24/09/2026