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

## Development notes

I'll document useful lessons, bugs and design decisions as the project develops and grows. Setup instructions and usage examples will be added once there is a working version.

### 21/09/2026
I implemented the first useful piece of application logic: finding opportunities with deadlines inside a supplied date range.

I initially considered sorting the entire opportunity list and then searching for valid deadlines, but after thinking about it for a moment, I instead decided to filter first and then sort that new list, because if there are `n` total opportunities and only `k` valid ones, this scans all `n` opportunities but only sorts the smaller set of `k` results. It also leaves the original list unchanged.

Deadline may not be set for an opportunity so I made sure to check against `None` before comparison to exclude such cases.

I moved all of this logic into a function named `upcoming_opportunities()` which filters and sorts the data before returning a new list, and printing remains outside the function, keeping the application logic separate from displaying the data.