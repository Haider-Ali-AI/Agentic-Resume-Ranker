# 🤖 Agentic Resume Ranking System

## Overview

This project implements an automated, end-to-end system to rank candidate resumes based on their match percentage against a given job description (JD). [cite_start]The core mechanism uses a **Greedy Keyword Matching Algorithm** combined with n8n automation to handle input, processing, and output[cite: 1, 10].

[cite_start]The system functions as a lightweight AI tool for recruitment, automating the initial, time-consuming screening process[cite: 8].

---

## ✨ Features and Core Logic

### Core Functionality
* [cite_start]**Input Handling:** The system accepts a job description and multiple candidate resumes (PDF/TXT)[cite: 13, 14].
* [cite_start]**Greedy Scoring:** Resumes are scored based on the ratio of JD keywords found in the resume[cite: 18].
* **Algorithm Formula:** The score is calculated as:
    $$\text{Score} = \frac{\text{Matched Keywords}}{\text{Total JD Keywords}} \times 100$$
* [cite_start]**Ranking & Reporting:** The system returns a ranked list and automatically stores results in a spreadsheet/database while emailing the Top 3 candidates and their match percentages to HR[cite: 20, 21].

### Key Technologies
| Component | Tool / Requirement | Role in Project |
| :--- | :--- | :--- |
| **Automation** | **n8n** | [cite_start]Orchestrates the entire workflow, manages input, routing, sorting, and integrations[cite: 6, 27]. |
| **Backend Logic** | **JavaScript** (Native Function) | [cite_start]Implements the **Greedy Algorithm**, tokenization, and cleaning logic[cite: 24, 26]. |
| **File Parsing** | **PyPDF2** (integrated via custom code) | Used to reliably parse text content from PDF resume files. |
| **Reporting** | **Google Sheets** (or Notion) and **SMTP Email** | [cite_start]Stores the full list and handles the Top 3 candidate notification[cite: 28]. |

---

## 🛠️ Setup and Execution

### Prerequisites
1.  **n8n:** Installed and running locally.
2.  **Python Libraries:** If using the original Python node, ensure `PyPDF2` and `nltk` are installed (`pip install PyPDF2 nltk`).
3.  **Credentials:** Google Sheets Service Account/App Password and SMTP App Password are required for output nodes.

### Workflow Steps (Node by Node)
1.  **Input:** The workflow starts manually (`Start` node) and reads files from disk (`Read/Write Files from Disk`).
2.  **Preparation:** A `Function` node injects the JD text.
3.  [cite_start]**Processing:** A `Split Out` node separates the files, and the **JavaScript Scoring Logic** tokenizes the text and calculates the score[cite: 5].
4.  [cite_start]**Ranking:** The `Sort` node ranks all items by the calculated `score`[cite: 20].
5.  [cite_start]**Output:** A final `Function` node filters the top 3 and routes the data to the storage (`Append or update row in sheet`) and notification (`Send email`) paths[cite: 21, 28].

### How to Run:
1.  Import the **`n8n_workflow.json`** file into your n8n workspace.
2.  Configure the Google Sheets and Email credentials.
3.  Place PDF/TXT resumes in the path specified in the `Read/Write Files from Disk` node.
4.  Click the **`Execute Workflow`** button on the **Start** node.

---

## 🏆 Evaluation Summary

| Criteria | Fulfillment |
| :--- | :--- |
| Accurate Greedy Matching Algorithm | [cite_start]Implemented the score formula using JavaScript logic[cite: 4, 18]. |
| Resume parsing + Pre-processing | [cite_start]Implemented text cleaning and tokenization (e.g., removing stop words)[cite: 5]. |
| Integration with n8n (End-to-End) | [cite_start]Full, working pipeline from file reading to final email delivery[cite: 6, 27]. |
| Clean Ranking Output (Sorted) | [cite_start]Output is correctly sorted and filtered to display the Top 3[cite: 20, 21]. |