# CS 450 AI Teaching Assistant — Presentation Talking Points

Extra talking points to expand on each bullet during the presentation. Use these as a speaker guide; each sub-bullet is one line you can say aloud.

---

## Slide 1 — Introduction

- **Project Goal: Create an AI teaching assistant for CS 450 that can explain course concepts and answer student questions in real time**
  - Think of it as a tutor that is available 24/7, not just during office hours.
  - It is scoped specifically to CS 450 material, so answers stay on-topic for the course.

- **Topic: Tailoring a LLM to perform a specific task**
  - We did not retrain the model from scratch — we shaped its behavior with prompt engineering and grounded it in course material with RAG.
  - This shows how a general-purpose LLM can be adapted to a niche domain without fine-tuning.

- **Importance: Provides a tool to help students understand course topics that can be used at any time**
  - Students often get stuck reviewing slides late at night when no instructor is available.
  - A focused tutor is less distracting than a general chatbot because it stays inside the course's scope.

---

## Slide 2 — Data

- **Source: CS 450 slides**
  - These are the official lecture decks, so the assistant is grounded in exactly what students are tested on.
  - Topics span the full AI curriculum: Foundations of AI, Search, Constraint Satisfaction, Learning, Neural Networks, Deep Learning, Logical Agents, Uncertainty, and Natural Language Models.
  - Nine decks total covering the whole semester.

- **Format: PDF files**
  - PDFs are convenient but mix text, images, and formatting noise, which made extraction non-trivial.
  - We had to pull out the raw text before we could feed anything to the model.

---

## Slide 3 — Data Preprocessing and Storage

- **Extracted text data from slides**
  - Used PyPDF to read each PDF page by page.
  - Slide decks are visual, so the extracted text is often short and fragmented.

- **Each slide = separate document**
  - Treating slides as individual documents keeps retrieval focused on a single concept at a time.
  - We further chunked text with a recursive splitter (400 characters, 150 overlap) so longer slides still retrieve cleanly.

- **Text → vector embeddings**
  - Embeddings turn text into numerical vectors that capture meaning, so similar ideas end up close together.
  - This is what lets the system find relevant slides even when the student's wording is different.

- **Data stored using ChromaDB**
  - ChromaDB is a lightweight vector database that runs locally — no cloud setup required.
  - We use a persistent client so the embeddings only need to be generated once.

- **Vector database stores AI's "memory"**
  - It is the assistant's reference library that it consults before answering.
  - Without it, the LLM would only know general AI knowledge, not the specifics of CS 450.

---

## Slide 4 — AI Techniques

- **LLMs: GPT-4.1-mini, Qwen2.5 3B**
  - GPT-4.1-mini is hosted, fast, and high-quality — good for the best answers.
  - Qwen2.5 3B runs locally through Ollama — free, private, and a useful comparison point.

- **Prompt Engineering: Define roles and guidelines**
  - The system prompt tells the model it is a CS 450 teaching assistant and how to behave.
  - We explicitly ask for clear explanations, examples, and to admit uncertainty rather than guess.

- **RAG: Provide external data to LLM to answer questions**
  - RAG stands for Retrieval-Augmented Generation: retrieve relevant text first, then generate an answer.
  - This keeps responses grounded in course material instead of relying solely on the model's training data.

---

## Slide 5 — System Workflow

- **User asks a question**
  - The student types a natural-language question into the chat interface.

- **Retrieve most relevant context from slides**
  - The question is embedded and compared against the ChromaDB collection.
  - The top matching slide chunks are pulled out as context.

- **Send LLM prompt-engineered template**
  - The template combines the role definition, response guidelines, retrieved context, and the user question.
  - This is where prompt engineering and RAG come together.

- **Generate response**
  - The LLM produces an answer that should be grounded in the retrieved slides.
  - The whole pipeline runs in seconds end-to-end.

---

## Slide 6 — Evaluation of Testing

- **Positives — Detailed and thorough responses**
  - The assistant generally explains concepts in depth instead of giving one-liners.

- **Positives — Provides relevant examples**
  - For instance, it can explain A* search with an analogy or walk through a constraint satisfaction problem step-by-step.

- **Positives — Minimal delay**
  - Even with retrieval added, response time stays usable for an interactive chat.

- **Negatives — Not concise**
  - Without fine-tuning, the model often over-explains, which can overwhelm a student.

- **Negatives — Off topic at times**
  - When retrieval misses, the model falls back on general AI knowledge and drifts away from CS 450 specifics.

- **Negatives — Context from slides not used effectively / low similarity scores**
  - Slides are visual and bullet-heavy, so the extracted text is sparse and embeddings score poorly against full-sentence questions.
  - When similarity is low, the retrieved context is not useful and the model essentially ignores it.

---

## Slide 7 — Challenges

- **What worked: Prompt engineering**
  - A well-written system prompt was the single biggest lever for shaping behavior.
  - It controls tone, format, and what the assistant should refuse to answer.

- **What worked: LLMs (GPT-4.1-mini, Qwen2.5 3B)**
  - Both models handled the role well; GPT was sharper, Qwen showed it is feasible to run locally.

- **Challenges: RAG (generating responses from context)**
  - Getting the model to actually use retrieved context, instead of leaning on its own knowledge, was harder than expected.

- **Challenges: Limited slides content**
  - Slide PDFs contain mostly bullets, not prose, so there is not much text to retrieve from.

- **Challenges: Formatting and shortening responses**
  - Even with explicit instructions, the model resists being concise without fine-tuning.

---

## Slide 8 — Conclusion and Future Improvements

- **Summary: Built an AI teaching assistant to explain course concepts**
  - End-to-end working pipeline from PDFs to chat interface, scoped to CS 450.

- **Summary: Used LLMs, prompt engineering, and RAG**
  - These three techniques together let us tailor a general LLM to a specific course without retraining.

- **Improvement: Clean data from slides**
  - Strip headers, page numbers, and layout noise so embeddings represent actual content.

- **Improvement: Add more data (assignment solutions, exam outlines, etc.)**
  - More prose-heavy sources would give RAG much better context to retrieve from.

- **Improvement: Fine-tune responses**
  - Fine-tuning on example Q&A pairs would help the model match a concise teaching-assistant style.
