---
outcomes:
  - The student will be set up with GitHub Classroom (using this project) and open their repository in an editor of choice.
  - The student will be able to make changes to their repository and commit them to the remote repository.
  - The student will understand options available for AI agent tools and how to use them.
  - The student will make a plan for a simple program with the agent.
  - The student will build the program with the agent
  - The student will evaluate the agent's performance and provide feedback.
---

# Project 0: Setup (draft)

## Overview

In this project, you will learn the tools and technologies we will be using throughout the course.

## Github Classroom

We'll be using Github Classroom to manage your project repositories, get feedback on your work, and submit your work.

### 1. Accept the assignment on [Github Classroom]().

Note: Since this is your first assignment, you will be asked to create or link your Github account to your Furman email address. Pick your email address from the list. If for some reason you don't see your email address, let the instructor know.

After you've accepted the assignment, you will be redirected to a page that looks like this:

<!-- TODO: add a screenshot of the Github Classroom assignment page -->

### 2. Clone the repository to your local machine

Click the "Code" button and copy the URL. Open up your terminal and run the following command to clone the repository to your local machine.

```bash
git clone <YOUR_REPO_URL>
```

### 3. Open the repository in your editor of choice

Take a look at the starter code in the repository. It's a simple Python project that you will be building upon.

```bash
- project-0-setup/
  - README.md
  - AGENTS.md
```

### 4. Pick your AI agent

You will use AI coding agents throughout this course. There are many options, but here is a simple path to get started:

**Recommendation:** For the best experience, use [Cursor](https://cursor.com/) or [Claude Code](https://code.claude.com/) with Claude Opus 4.5. This is the most capable setup available right now and costs $20/mo with a Claude Pro subscription.

**Free alternatives:** If cost is a concern, [GitHub Copilot](https://github.com/features/copilot) is [free for students](../../resources/github-copilot.guide.md#free-access-for-students) and works well. [Cursor](https://cursor.com/) also has a [free year for students](../../resources/cursor.guide.md#free-year-for-students) if you qualify.

See the [Agent Comparison Guide](../../resources/agents-comparison.guide.md) to compare all options.

---

To try it out, start up your agent of choice and say something like `I want to setup my project`.

Watch what the agent does. It will search the repository for relevant files likely prompt you for a task to complete.

### 5. Build something with your agent

AI Agents work best when they know what you're trying to do. You can help them understand by:

- Clearly explaining your goal
- Providing examples or rough notes/ideas
- Pointing it at relevant files or documentation in your repository

For example, there are multiple tasks in the `/tasks` folder. You can point your agent to these tasks and it should guide you through the process of completing them (or complete them for you if it is an eager model).

Let's try and point it at task one... you can do this by pasting in the path to the task file in the agent's chat window, saying something like "I want to complete task one" or `@` mentioning the file (most agents let you do this). Once you've done this, the agent should guide you through the process of completing the task.

### 6. Customize your agent

We can change the way our agents behave simply by changing the `AGENTS.md` file.
