# Long-Term Agentic Memory

A lightweight **memory system for AI agents** that extracts and stores **stable factual information** from user conversations.

This project focuses on building **persistent memory for AI agents** so they can remember important information across interactions instead of forgetting everything after one message.

The system analyzes messages and stores information in **three structured memory types**:

- Singular Memory
- Multi-value Memory
- Structured Memory

The goal is to simulate **long-term memory similar to human memory** inside AI systems.

---

# Concept

Most AI agents only have **short-term context** (current conversation).  
This project allows an agent to:

- Extract important information
- Ignore temporary or emotional statements
- Store long-term facts
- Reuse them in future interactions

This makes the agent **more personalized and intelligent over time**.

---

# Memory Types

## 1. Singular Memory

Stores **single value facts** that should always keep the latest value.

Example:

```json
"singular": {
  "name": "Sanwal",
  "city": "Rawalpindi"
}
```

If a new value appears, it **overwrites the old one**.

Example:

User:
```
My city is Lahore
```

Memory becomes:

```json
"city": "Lahore"
```

---

## 2. Multi Memory

Stores **multiple values** related to the same category.

Example:

```json
"multi": {
  "skills": ["Python", "JavaScript"],
  "interests": ["AI", "Machine Learning"]
}
```

Rules:

- New values are **appended**
- **Duplicates are ignored**

Example:

User:
```
I also know C++
```

Memory becomes:

```json
"skills": ["Python", "JavaScript", "C++"]
```

---

## 3. Structured Memory

Stores **nested structured information** like education or work experience.

Example:

```json
"structured": {
  "education": {
    "field": "Computer Science",
    "level": "Intermediate"
  }
}
```

This allows storing **complex user profiles**.

---

# System Instruction

The AI agent follows a strict instruction to extract only **stable factual information**.

```python
system_instruction = """
Extract stable factual information from the message.
Ignore temporary and emotional information.

Return ONLY valid JSON in this format:

{
 "singular": { },
 "multi": {},
 "structured": {}
}

Rules:
- singular: one-value facts (overwrite)
- multi: multi-value facts (append, no duplicates)
- structured: nested objects (education, work)
"""
```

---

# Example Input

User message:

```
Hi, my name is Sanwal. I live in Rawalpindi.
I am learning Python and JavaScript.
```

---

# Example Output

```json
{
  "singular": {
    "name": "Sanwal",
    "city": "Rawalpindi"
  },
  "multi": {
    "skills": ["Python", "JavaScript"]
  },
  "structured": {}
}
```

---

# Why This Project

This system helps build:

- Personal AI Assistants
- Autonomous AI Agents
- AI Operating Systems
- Long-term personalized chatbots

It is an important building block for **Agentic AI systems**.

---

# Future Improvements

- Memory retrieval system
- Vector search integration
- User profile building
- Multi-agent shared memory
- Memory scoring and decay
- Database persistence

---

# Author

**Sanwal Sharafat**

AI Agent Developer focused on building **AI Agents and Personal AI Operating Systems**.

GitHub:  
https://github.com/SanwalSharafat