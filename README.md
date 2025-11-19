# MedInsight AI - RadiologyAI Pro

AI-Powered Diagnostic Image Analysis Platform

## Project Structure

```
medinsight_ai/
│
├── main.py                 # Main application entry point
├── requirements.txt        # Project dependencies
├── gemini_api.py           # API key configuration
├── utils.py                # Utility functions
│
├── home/                   # Home page module
│   └── home.py
│
├── image_classification/   # Image classification module
│   └── classifier.py
│
├── xray/                   # X-ray report generation module
│   └── xray_report.py
│
├── ct_scan/                # CT scan report generation module
│   └── ct_report.py
│
├── mri/                    # MRI report generation module
│   └── mri_report.py
│
├── ultrasound/             # Ultrasound report generation module
│   └── ultrasound_report.py
│
├── hospital_recommendation/ # Hospital recommendation system for Gulbarga
│   └── hospital_finder.py
│
└── README.md              # This file
```

## Features

1. **Home Page** - Overview and introduction to the platform
2. **Image Classification** - Automatically classify medical images
3. **X-ray Report Generation** - Generate diagnostic reports from X-ray images
4. **CT Scan Report Generation** - Generate clinical reports from CT scans
5. **MRI Scan Report Generation** - Generate interpretation reports from MRI scans
6. **Ultrasound Report Generation** - Generate diagnostic summaries from ultrasound images
7. **Hospital Recommendation System** - Recommend hospitals in Gulbarga based on medical reports

## Installation

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   streamlit run main.py
   ```

## Modules

Each feature is implemented as a separate module to maintain clean code organization and separation of concerns:

- **home/home.py** - Contains the home page implementation
- **image_classification/classifier.py** - Handles image classification functionality
- **xray/xray_report.py** - Manages X-ray report generation
- **ct_scan/ct_report.py** - Manages CT scan report generation
- **mri/mri_report.py** - Manages MRI report generation
- **ultrasound/ultrasound_report.py** - Manages ultrasound report generation
- **hospital_recommendation/hospital_finder.py** - Implements the hospital recommendation system
- **utils.py** - Common utility functions used across modules
- **gemini_api.py** - API key configuration for Google Gemini

## API Key Configuration

The application uses Google Gemini API for AI-powered analysis. The API key is configured in `gemini_api.py`. For security, it's recommended to set the `GEMINI_API_KEY` environment variable instead of hardcoding it.