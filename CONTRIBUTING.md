# Contribution Guide

Welcome to the **Remedial Class Management** project! We are very excited that you are interested in contributing. As a Hacktoberfest-friendly repository, we encourage contributions from all skill levels.

By following this guide, you help us maintain code quality and keep the project workflow smooth.

## Code of Conduct

We are committed to creating an open, welcoming, and inclusive environment. All contributors are expected to adhere to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/){:target="\_blank"}.

---

## Code Style

Consistency is key. While this project welcomes contributions in various languages and frameworks, please ensure you follow these basic conventions for the language you are using:

### 1. Naming Conventions

| Element                         | Recommended Naming Style                       | Example                           |
| :------------------------------ | :--------------------------------------------- | :-------------------------------- |
| **Variables/Functions/Methods** | `camelCase` (e.g., JavaScript, Python)         | `calculateAverage`, `studentList` |
| **Classes/Components**          | `PascalCase` (e.g., Java, C#, React Component) | `StudentModel`, `RemedialForm`    |
| **Global Constants**            | `UPPER_SNAKE_CASE`                             | `MAX_SCORE_LIMIT`                 |

### 2. Formatting

- **Indentation**: Use **4 spaces** for indentation (avoid using tabs).
- **Spacing**: Use adequate spacing around operators, after commas, and inside code blocks for optimal readability.
- **New Files**: If you are adding a new file, ensure it has the correct extension and its name clearly reflects its content (e.g., `remedial_service.py`, `Student.java`).

### 3. Comments

- Provide comments sparingly, mainly for public functions, complex business logic, or ambiguous code sections.
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
  git clone [https://github.com/YOUR_USERNAME/RemedialClassManagement.git](https://github.com/YOUR_USERNAME/RemedialClassManagement.git)
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

### 4. Push and Create a PR

- **Push** your new branch to GitHub.
  ```bash
  git push origin feature/your-branch-name
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
