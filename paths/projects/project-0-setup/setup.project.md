---
template_repo: "https://github.com/Alvin-Furman-CS-Classroom/alvin-furman-cs-classroom-csc-343-ai-spring-2026-project-0-setup-csc343-project-0-setup"
outcomes:
  - The student will be set up with GitHub Classroom (using this project) and open their repository in an editor of choice.
  - The student will be able to make changes to their repository and commit them to the remote repository.
  - The student will understand options available for AI agent tools and how to use them.
  - The student will make a plan for a simple program with the agent.
  - The student will build the program with the agent
  - The student will evaluate the agent's performance and provide feedback.
assignment_id: 922182
assignment_url: "https://classroom.github.com/a/bPvk0wQm"
assignment_title: "Project 0: Setup"
---

# Project 0: Setup

This project will help you get set up with the tools you will use in this course as well as introduce you to agent-based development.

Follow the instructions below thoughtfully and in order. Take your time and experiment. The goal is to understand how to use AI agents effectively for our project work that comes after.

---

## Part 1: Get Your Editor Ready

Before you can open your project, you need an AI-powered code editor. We recommend starting with **Cursor**.

### Install Cursor

1. Download [Cursor](https://cursor.com/) and install it
2. Open Cursor and sign in (create an account if needed)
3. [Claim your free year as a student](../../resources/cursor.guide.md#free-year-for-students)

That's it! You're ready to open your project.

> **Pro tip:** You can explore other options like [GitHub Copilot](../../resources/github-copilot.guide.md), [Claude Code](../../resources/claude-code.guide.md), or see the full [Agent Comparison Guide](../../resources/agents-comparison.guide.md) later. For now, Cursor is the easiest way to get started.

---

## Part 2: Get Your Project

### 1. Accept the assignment

Use the link below to accept the assignment. This will ask you to create a GitHub account (or login with an existing one) and link your Furman email to it. Make sure you select your Furman email from the list it shows you.

<a href="https://classroom.github.com/a/bPvk0wQm" className="inline-block px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white no-underline font-semibold rounded-lg shadow-md transition-colors duration-200">Accept the Assignment</a>

If you, for some reason, do not see your Furman email in the list, let the instructor know.

### 2. Open it in Cursor

After you've accepted the assignment, you will see a blue link. This is the URL of your repository. Copy this URL.

In Cursor, go to **File > New Window > Clone Repository** and paste the URL into the "Repository URL" field. Cursor will clone and open the repository for you.

Or, if you prefer the terminal:

```bash
git clone <YOUR_REPO_URL>
cd project-0-setup-<your-username>
```

### 3. Look around before opening your agent

Before you fire up an AI agent, take a moment to explore what's in the repository yourself:

```
README.md           # Brief overview, points here
AGENTS.md           # Instructions for AI agents (read this!)
REFLECTION.md       # You'll fill this out at the end
task1/              # Your code task work goes here
task2/              # Your planning task work goes here
task3/              # Your computing task work goes here
```

> **Pro tip:** Read the `AGENTS.md` file... this is like a plain-language program for making your agent behave in a certain way.

---

## Part 3: Your First Conversation

Open your repository in your editor with your agent active.

### Start simple

Try saying:

> Hello, what can I do here?

**Watch what happens.** Does your agent:

- Read files first, or start talking immediately?
- Ask clarifying questions, or assume what you want?
- If you asked this same question again later in a fresh conversation, would the agent respond exactly the same way?

### Try a few variations

Experiment with different prompts and see how the responses change.

Try these prompts (or your own variations):

> Interview me about my interests and hobbies.

> Tell me a joke.

> What's your favorite programming language?

> Tabs or spaces?

---

## Part 4: Complete the Tasks

There are three tasks, each helping you experience a different way agents can help. Your repository has empty folders for each: task (`task1/`, `task2/`, `task3/`.)

These tasks are designed to help you experiment with different ways agents can help.

- [ ] [Task 1: Coding](tasks/code.task.md)
- [ ] [Task 2: Planning](tasks/planning.task.md)
- [ ] [Task 3: Computing](tasks/computing.task.md)

You can click each task above for detailed instructions. Mark the tasks as complete when you have finished them.

---

## Part 5: Experiment with AGENTS.md

If you don't like how your agent is interacting with you, you can change how it behaves by editing `AGENTS.md`.

### AGENTS.md

1. Open `AGENTS.md` and read through it.
2. Add a line like: `Always explain your reasoning step by step before writing any code.`
3. Start a new conversation and see if the agent follows your instructions.

### Things to try

- "Be concise" vs. "Explain everything in detail"
- "Ask clarifying questions before starting" vs. "Just do what I ask"
- "Focus on teaching me" vs. "Focus on completing the task quickly"
- Fun things like "Talk like a pirate" or a "you are an over-zealous Reddit moderator"

> **Pro tip:** Not all agents respect `AGENTS.md` equally.

---

## Part 6: Commit Your Work

After completing the tasks, save your work by committing and pushing your changes to your repository:

```bash
git add .
git commit -m "Complete Project 0 tasks"
git push
```

You can also do this by going to the Source Control tab in your IDE and clicking the "Commit" button (be sure to type in a commit message like "Complete Project 0 tasks").

> **Pro tip** Your agent is probably better at git than you, you can ask it for help with git commands.

---

## Part 7: Reflect

Fill out `REFLECTION.md` with your honest thoughts. There are brackets to fill in your answers e.g. `[Your answer here]`. Replace each bracketed section with your answer.

After you are finished, commit your reflections and push them to your repository:

```bash
git add REFLECTION.md
git commit -m "Add reflection"
git push
```

---

## What to Submit

Your repository should include:

- [ ] Code file(s) from Task 1
- [ ] Any artifacts from Tasks 2-3 (optional)
- [ ] Completed `REFLECTION.md`

---

## Stuck?

1. **Ask your agent first**: This is good practice, and often works well if you are clear about your question.
2. **Reach out to the instructor**: If you're truly stuck.
