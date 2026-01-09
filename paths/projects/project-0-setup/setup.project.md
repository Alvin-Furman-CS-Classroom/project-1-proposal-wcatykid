---
outcomes:
  - The student will be setup with github Classroom (using this project) and open their repository in an editor of choice.
  - The student will be able to make changes to their repository and commit them to the remote repository.
  - The student will understand options available for AI agent tools and how to use them.
  - The student will make a plan for a simple program with the agent
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

You will have the opportunity to use and try many different AI agents in this course. This is a very active field and agents are constantly being updated and improved.

For starters, let's try using Claude Code, Cursor, or GitHub Copilot to help you setup your project. These all have their pros and cons but are solid choices for this course.

- [Claude Code](https://code.claude.com/): This is a TUI (Terminal User Interface) based agent that can work along side with you no matter what editor you are using. Claude Code and Opus 4.5 in particular is a very powerful combination.
- [Cursor](https://cursor.com/): This is a full-blown IDE (VS Code fork) with the AI agent built into the editor itself. Its the most popular choice by current industry standards but is also the most expensive.
- [GitHub Copilot](https://github.com/features/copilot): This is built right into VSCode and is cheaper than Cursor or Claude Code.
- [Opencode](https://opencode.ai/): This is another TUI-based agent that can work with any model including some quite powerful free models from time-to-time.
- [Antigravity (Google)](https://antigravity.google/): Google's VSCode fork with their Gemini 3 model very powerful and mostly free (for now).

All of these agents are free to start but scale differently based on how much you use them. Typically, you can expect to pay $20/month for a good agent with moderate usage

---

To try it out, start up your agent of choice and say something like `I want to setup my project`.

Whatch what the agent does. It will search the repository for relevant files likely prompt you for a task to complete.

### 5. Build something with your agent

AI Agents work best when they know what you're trying to do. You can help them understand by:

- Clearly explaining your goal
- Providing examples or rough notes/ideas
- Pointing it at relevent files or documentation in your repository

For example, there are multiple tasks in the `/tasks` folder. You can point your agent to these tasks and it should guide you through the process of completing them (or complete them for you if it is an eager model).

Let's try and point it at task one... you can do this by pasting in the path to the task file in the agent's chat window, saying something like "I want to complete task one" or `@` mentioning the file (most agents let you do this). Once you've done this, the agent should guide you through the process of completing the task.

### 6. Customize your agent

We can change the way our agents behave simply by changing the `AGENTS.md` file.
