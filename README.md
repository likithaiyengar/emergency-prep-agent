\# Emergency Preparedness Guide for Students

An AI-powered agentic application that helps students prepare for natural disasters.



\## Project Domain

Safety and Disaster Readiness



\## Features

\- AI chat assistant powered by Groq (LLaMA 3.3)

\- Memory: Stores every conversation in SQLite database

\- Reflection: Agent reviews conversation every 6 messages and identifies gaps

\- Replanning: Updates advice based on student's location and housing type

\- Quick action buttons for Fire, Flood, Earthquake, Cyclone

\- Personalized emergency numbers by city

\- Student profile saved automatically



\## Agentic Components

\- Memory Estate: SQLite stores all conversations and student profiles

\- Reflection: Agent reflects on gaps in preparedness every 6 messages

\- Replanning: Agent updates plan when new information is provided



\## Tech Stack

\- Python 3.12

\- Streamlit (UI)

\- Groq API with LLaMA 3.3 (LLM)

\- SQLite (Memory/Database)

\- python-dotenv



\## Setup Instructions

1\. Clone the repository

2\. Create virtual environment: python -m venv venv

3\. Activate: venv\\Scripts\\activate

4\. Install dependencies: pip install streamlit groq python-dotenv

5\. Create .env file and add your Groq API key: OPENAI\_API\_KEY=your\_key\_here

6\. Run: streamlit run app.py



\## Project Structure

\- app.py: Streamlit UI

\- agent.py: Core agent logic with tools, reflection, replanning

\- memory.py: SQLite memory layer

\- .env: API keys



\## Sample Queries

\- "I live in a hostel in Bangalore, how do I prepare for floods?"

\- "Give me an earthquake safety checklist"

\- "What are emergency numbers in Chennai?"



\## Author

\Likitha K R

\4MH23CA023

\MAHARAJA INSTITUTE OF TECHNOLOGY MYSURU

