# Contribution Guide

Welcome to the **Remedial Class Management** project! We are very excited that you are interested in contributing. As a Hacktoberfest-friendly repository, we encourage contributions from all skill levels.

By following this guide, you help us maintain code quality and keep the project workflow smooth.

## Code Style

Since this project is primarily built using **Python** and **Streamlit**, all code contributions must adhere to the **PEP 8 style guide**, which is the official standard for Python.

### 1. Naming Conventions

Please use the following conventions:

| Element                         | PEP 8 Naming Style                                               | Example                                 |
| :------------------------------ | :--------------------------------------------------------------- | :-------------------------------------- |
| **Variables/Functions/Methods** | **`snake_case`** (all lowercase, words separated by underscores) | `calculate_average`, `get_student_list` |
| **Classes/Components**          | **`PascalCase`**                                                 | `StudentModel`, `DatabaseConnector`     |
| **Global Constants**            | `UPPER_SNAKE_CASE`                                               | `MAX_SCORE_LIMIT`                       |
| **Modules/Files**               | Short, all lowercase with underscores                            | `db_ops.py`, `app.py`                   |

### 2. Formatting

- **Indentation**: Use **4 spaces** for indentation. **Tabs are strictly prohibited.**
- **Line Length**: Limit all lines of code to a maximum of **79 characters**.
- **Imports**: Imports should generally be on separate lines and grouped (standard library, third-party, local imports) as recommended by PEP 8.
- **Type Hinting**: Please use Python type hints (`def func(arg: str) -> bool:`) for new functions and methods where appropriate.

### 3. Comments and Documentation

- Use docstrings (triple quotes `"""..."""`) for documenting modules, classes, and functions.
- Provide comments sparingly for complex logic.
- Delete any unnecessary _commented-out code_ before submitting a PR.

---

## Branching Strategy (Git Workflow)

We use a straightforward, feature-focused workflow:

1.  **`main`**: The primary branch that should always be stable and reflect the latest usable version. **Do not commit directly to `main`**.
2.  **Feature or Fix Branches**:
    - Every contribution (new feature, bug fix, or documentation update) must be done on a new branch.
    - Create your branch off of `main` (or `develop` if it exists).
    - **Branch Naming Convention**: Use a clear prefix:
      - `feat/new-feature-name` (For adding new features)
      - `fix/description-of-fix` (For bug fixes)
      - `docs/update-readme` (For documentation changes)
      - `chore/dependency-updates` (For routine maintenance)

---

## Pull Request (PR) Process

Follow these steps to ensure your contribution is integrated smoothly:

### 1. Fork and Clone the Repository

- **Fork** the **`R-Anurag/RemedialClassManagement`** repository to your personal GitHub account.
- **Clone** your forked repository to your local machine.
  ```bash
  git clone [https://github.com/your-username/RemedialClassManagement.git]
  cd RemedialClassManagement
  ```

### 2. Create a New Branch

- Always start from the latest `main`.
  ```bash
  git checkout main
  git pull origin main
  git checkout -b feature/your-branch-name
  ```

### 3. Commit Changes

- Implement your desired changes.
- Create a **commit** with a clear, informative message. The commit message should explain _what_ you changed, not just _how_ you changed it.

  **Good Commit Message Example (Conventional Commit Style):**

  ```
  feat: implement student score validation function

  Adds validation logic to ensure the entered score is within the 0-100 range.
  ```

**General Format:** `<type>(<scope>): <short description>`

| Type           | Purpose                                                            | Example                                                |
| :------------- | :----------------------------------------------------------------- | :----------------------------------------------------- |
| **`feat`**     | A new feature.                                                     | `feat(chart): implement candlestick chart view`        |
| **`fix`**      | A bug fix.                                                         | `fix(layout): fix sidebar collapse issue on mobile`    |
| **`docs`**     | Documentation changes only.                                        | `docs: update CONTRIBUTING.md`                         |
| **`refactor`** | Code restructuring that doesn't fix a bug or add a feature.        | `refactor(auth): rename login service to auth service` |
| **`test`**     | Adding or correcting tests.                                        | `test: add unit test for StockCard component`          |
| **`chore`**    | Changes to the build process, package manager, or auxiliary tools. | `chore: update webpack configuration`                  |

---

### 4. Push and Create a PR

- **Push** your new branch to GitHub.
  ```bash
  git push origin fix/resolve-login-issue
  ```
- Go to your repository page on GitHub and click **"Compare & pull request"** to open a new PR.
- Ensure the PR target is the **`main`** branch of the upstream repository (`R-Anurag/RemedialClassManagement`).

### PR Checklist

Before hitting "Create pull request", please check the following points:

- [ ] The PR title is concise and the description details the changes.
- [ ] The code changes have been tested locally and function correctly.
- [ ] The new code adheres to the project's **Code Style**.
- [ ] No unnecessary or commented-out code is left.
- [ ] You have resolved any merge conflicts (if applicable).

Thank you very much for your contribution! We will review your PR as soon as possible.
