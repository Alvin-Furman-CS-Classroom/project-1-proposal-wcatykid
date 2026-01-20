# Timeline Verification Checklist

## Current Timeline Analysis

Your current timeline shows:

| Module | Required Topic(s) | Topic Taught | Checkpoint Due |
|--------|------------------|--------------|----------------|
| 1 | Search (A*, Beam Search) | Week 1-2 | Checkpoint 1 |
| 2 | NLP (Sentiment Analysis) | Week 4-6 | Checkpoint 2 |
| 3 | Propositional Logic | Week 2-4 | Checkpoint 3 |
| 4 | Knowledge Representation, Constraint Satisfaction | Week 5-7 | Checkpoint 4 |
| 5 | Explainable AI, Knowledge Representation | Week 8-10 | Checkpoint 5 |

## Critical Verification Points

### 1. Check Against Course Schedule URLs

Verify these URLs from AGENTS.md:
- **Course Topics**: https://csc-343.path.app/resources/course.topics.md
- **Course Schedule**: https://csc-343.path.app/resources/course.schedule.md

### 2. Potential Issues to Check

#### Issue #1: Module 3 (Propositional Logic)
- **Taught**: Week 2-4
- **Due**: Checkpoint 3
- **Verify**: Is Checkpoint 3 AFTER Week 4 ends? 
  - ✅ If YES: OK (topic is taught before checkpoint)
  - ❌ If NO: PROBLEM (can't implement before it's taught)

#### Issue #2: Module Dependencies vs. Teaching Order
- **Module 3** depends on **Module 2** output, but:
  - Module 3 topic (Logic) taught: Week 2-4
  - Module 2 topic (NLP) taught: Week 4-6
- **Verify**: 
  - When is Checkpoint 2 (Module 2 due)?
  - When is Checkpoint 3 (Module 3 due)?
  - Ensure Checkpoint 2 comes before Checkpoint 3 (dependency order)
  - Ensure Module 2's NLP topic is taught before you need to use its output

#### Issue #3: Knowledge Representation Timing
- Module 4 uses Knowledge Representation (taught Week 5-7)
- Module 5 also uses Knowledge Representation (taught Week 8-10)
- **Verify**: Are there two separate KR topics, or is Module 5's "Knowledge Representation" a reuse/appplication of the topic from Module 4?

### 3. Required Checks

For each module, verify:
- [ ] **Topic Coverage**: Is the topic actually taught in the weeks listed?
- [ ] **Checkpoint Timing**: Is the checkpoint due date AFTER the topic is fully taught?
- [ ] **Dependency Timing**: If Module X depends on Module Y, does Module Y's checkpoint come before Module X starts?

### 4. Suggested Verification Table

Create this table from the actual course schedule:

| Module | Topic | Actual Teaching Weeks | Checkpoint Date | Topic Complete Before Checkpoint? | OK? |
|--------|-------|----------------------|-----------------|----------------------------------|-----|
| 1 | Search | ___ | ___ | ✅/❌ | ___ |
| 2 | NLP | ___ | ___ | ✅/❌ | ___ |
| 3 | Propositional Logic | ___ | ___ | ✅/❌ | ___ |
| 4 | Knowledge Representation | ___ | ___ | ✅/❌ | ___ |
| 5 | Explainable AI | ___ | ___ | ✅/❌ | ___ |

## Common Issues to Watch For

1. **Teaching after checkpoint**: If a topic is taught in Week X but checkpoint is Week X-1, you can't implement it
2. **Dependency timing**: Module dependencies must allow time for implementation
3. **Overlap issues**: If two modules need the same topic taught at different times, clarify whether it's taught multiple times or applied multiple times

## After Verification

Once you've checked the actual course schedule:
1. Update the "Topic Covered By" column with verified weeks
2. Ensure all checkpoints come AFTER topics are taught
3. Confirm dependency order is feasible (Module 1 → 2 → 3 → 4 → 5)
