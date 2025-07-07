# 🤖 Siliguri Institute of Technology - Campus Assistant

![Demo GIF](https://demo.gif) <!-- Replace with actual link -->

---

## 📘 Overview

The **SIT Campus Assistant** is an AI-powered chatbot designed to provide instant information about **Siliguri Institute of Technology**. It handles queries related to:

- Courses  
- Admissions  
- Placements  
- Facilities  
- Contact details  

Powered by a hybrid system combining a local knowledge base and **Google’s Gemini API** for enhanced understanding and fallback support.

---

## ✨ Key Features

- ✅ **Instant Answers** to college-related questions  
- 🕒 **24/7 Availability** for students and visitors  
- 🧠 **Knowledge Base** with institute-specific content  
- 🌐 **Gemini Fallback** for complex/unseen queries  
- 🌙 **Modern Dark Theme** with responsive layout  
- 💬 **Token Counter** to monitor API usage costs  

---

## 🛠️ Technology Stack

| Layer       | Tool                     |
|-------------|--------------------------|
| Frontend    | Streamlit                |
| AI Model    | Google Gemini API        |
| NLP         | Sentence Transformers    |
| Vector DB   | FAISS                    |
| Caching     | Streamlit Cache          |

---

## 🚀 Setup and Installation

### ✅ Prerequisites

- Python 3.8+
- Gemini API Key

### 🔧 Step-by-Step Guide

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/HabibParvej/ChatBot.git
    cd ChatBot
    ```

2. **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate      # For Linux/Mac
    venv\Scripts\activate         # For Windows
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Secrets:**

    Create a file at `.streamlit/secrets.toml`:
    ```toml
    GEMINI_API_KEY = "your_actual_api_key_here"
    ```

5. **Build the Knowledge Base:**
    ```bash
    python build_vector.py
    ```

6. **Run the Application:**
    ```bash
    streamlit run app.py
    ```

---

## 🎨 Customization

To update or expand college information:

1. Modify the knowledge base file:
    ```
    data/college_knowledge.csv
    ```

2. Rebuild the vector store:
    ```bash
    python build_vector.py
    ```

3. Restart the app:
    ```bash
    streamlit run app.py
    ```

---

## 📁 Project Structure

ChatBot/
├── .streamlit/ # Streamlit configuration
│ └── secrets.toml # API keys
├── data/ # Knowledge base data
│ └── college_knowledge.csv
├── faiss_store/ # Vector database
│ ├── index.faiss
│ └── data.pkl
├── app.py # Main application
├── build_vector.py # Knowledge base builder
├── requirements.txt # Dependencies
└── README.md # Project documentation

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository  
2. Create your branch:  
    ```bash
    git checkout -b feature/your-feature
    ```
3. Commit your changes:  
    ```bash
    git commit -am "Add some feature"
    ```
4. Push the branch:  
    ```bash
    git push origin feature/your-feature
    ```
5. Open a **Pull Request**

## 📧 Contact

- **Habib Parvej** – [habibparvej777@gmail.com](mailto:habibparvej777@gmail.com)  
- **Siliguri Institute of Technology** – [info@sittech.edu.in](mailto:info@sittech.edu.in)  
- **GitHub Profile** – [github.com/HabibParvej](https://github.com/HabibParvej)

