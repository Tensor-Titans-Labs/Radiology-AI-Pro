# 🏥 MedInsight AI - RadiologyAI Pro

**Advanced Multi-Modal Medical Imaging Analysis & Hospital Recommendation System**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-ff4b4b)
![Gemini AI](https://img.shields.io/badge/AI-Gemini%202.0%20Flash-4285f4)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

## 📋 Overview

**MedInsight AI** is a comprehensive, AI-powered medical diagnostic assistant designed to bridge the gap between complex medical imaging and accessible healthcare insights. Leveraging Google's state-of-the-art **Gemini 2.0 Flash-Lite** model, it provides real-time analysis of X-rays, CT Scans, MRIs, and Ultrasounds, generating professional reports and offering localized hospital recommendations.

This project serves as a powerful prototype for the future of digital health, acting as an intelligent "second opinion" tool for patients and a preliminary diagnostic aid for healthcare professionals.

---

## ✨ Key Unique Features

MedInsight AI stands out due to its unified approach and resilient architecture:

1.  **Comprehensive Multi-Modal Analysis**: A single platform for analyzing **X-rays, CT Scans, MRIs, and Ultrasounds**, unlike many single-purpose tools.
2.  **Resilient AI Architecture**: Features a custom-engineered **Smart Fallback Mechanism** that intelligently switches between Gemini models (2.0 Flash, 1.5 Pro, etc.) to handle rate limits and ensure high availability.
3.  **Localized Hospital Recommendations**: Bridges the gap to care by analyzing medical conditions and recommending suitable hospitals in the **Gulbarga region** (customizable).
4.  **Automated Professional Reporting**: Instantly generates downloadable, professionally formatted **PDF Medical Reports** for record-keeping.
5.  **Real-Time Diagnostic Support**: Provides immediate, detailed textual analysis to demystify complex medical scans.
6.  **Intelligent Image Classification**: Automatically validates uploaded images to ensure the correct diagnostic model is applied.
7.  **Cost-Optimized Performance**: Prioritizes efficient "Flash" models for rapid inference, falling back to "Pro" models only when necessary.

---

## 🛠️ Tech Stack

*   **Frontend/Framework**: [Streamlit](https://streamlit.io/) (Python)
*   **Artificial Intelligence**: Google [Gemini API](https://ai.google.dev/) (Models: `gemini-2.0-flash-lite`, `gemini-1.5-flash`, `gemini-1.5-pro`)
*   **Image Processing**: [Pillow (PIL)](https://python-pillow.org/)
*   **Report Generation**: [ReportLab](https://www.reportlab.com/)
*   **Language**: Python 3.x

---

## 🚀 Installation & Setup

Follow these steps to set up the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/medinsight-ai.git
cd medinsight-ai
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
1.  Get your API key from [Google AI Studio](https://aistudio.google.com/).
2.  Open `gemini_api.py` or set it as an environment variable.
    *   *Option A (Environment Variable - Recommended):*
        ```bash
        export GEMINI_API_KEY="your_api_key_here"
        # Or on Windows PowerShell:
        $env:GEMINI_API_KEY="your_api_key_here"
        ```
    *   *Option B (Direct Edit - For testing only):*
        Edit `gemini_api.py` and replace the default key.

### 5. Run the Application
```bash
streamlit run main.py
```
The app will open in your browser at `http://localhost:8501`.

---

## 📖 Usage Guide

1.  **Home**: Overview of the platform and quick access to features.
2.  **Hospital Finder**: Describe your symptoms or condition to get AI-curated hospital recommendations.
3.  **Image Classification**: Upload any medical image to identify if it's an X-ray, MRI, CT, or Ultrasound.
4.  **Analysis Modules (X-Ray, CT, MRI, Ultrasound)**:
    *   Upload your medical scan (PNG, JPG, JPEG).
    *   Click **"Generate Report"**.
    *   View the detailed AI analysis.
    *   Download the findings as a **PDF Report**.

---

## ⚠️ Current Limitations

As a prototype, please be aware of the following:

*   **Dependency on Cloud API**: Requires an active internet connection and relies on Google's Gemini API availability.
*   **Not for Clinical Diagnosis**: This tool is for **educational and informational purposes only**. It has not undergone clinical trials or FDA approval. **Always consult a certified medical professional for diagnosis.**
*   **Static Hospital Data**: The hospital recommendation database is currently limited to specific regions and is not real-time.
*   **Data Persistence**: The application is stateless; user data and reports are not saved after the session ends.

---

## 🔮 Future Scope

*   Integration with real-time hospital databases and appointment booking systems.
*   Implementation of secure user authentication and cloud database storage.
*   Fine-tuning models on specific medical datasets for higher accuracy.
*   Mobile application development.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Acknowledgements

*   **Google DeepMind** for the Gemini API.
*   **Streamlit** for the amazing rapid application development framework.