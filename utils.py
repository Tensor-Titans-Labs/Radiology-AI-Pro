import streamlit as st
from PIL import Image
import google.generativeai as genai
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
import tempfile
import time
import random

def process_image(uploaded_file):
    """Process uploaded image file"""
    try:
        image = Image.open(uploaded_file)
        return image
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

def generate_report_with_retry(image, prompt, max_retries=3, base_delay=2, model_name='gemini-2.0-flash-lite'):
    """Generate report with retry mechanism and model fallback"""
    # Convert image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # List of models to try in order
    # Prioritize the requested model, then fall back to efficient/stable models
    models_to_try = [
        model_name,
        'gemini-2.0-flash-lite',
        'gemini-2.5-flash-lite',
        'gemini-flash-latest',
        'gemini-pro-latest'
    ]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_models = [x for x in models_to_try if not (x in seen or seen.add(x))]
    
    last_error = None
    
    for current_model_name in unique_models:
        try:
            # Create model
            model = genai.GenerativeModel(current_model_name)
            # st.info(f"Attempting with model: {current_model_name}")
        except Exception as e:
            # st.warning(f"Skipping model {current_model_name}: {str(e)}")
            continue
            
        # Retry loop for the current model
        for attempt in range(max_retries + 1):
            try:
                # Generate content with the image and prompt
                response = model.generate_content([
                    prompt,
                    {'mime_type': 'image/png', 'data': img_byte_arr}
                ])
                
                # Return the response text if successful
                if response.text:
                    return response.text
                
            except Exception as e:
                last_error = e
                error_message = str(e).lower()
                
                # Handle Rate Limits (429 or Quota Exceeded)
                if "quota exceeded" in error_message or "429" in error_message or "resource exhausted" in error_message:
                    if attempt < max_retries:
                        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                        # st.warning(f"Rate limit on {current_model_name}. Retrying in {delay:.1f}s...")
                        time.sleep(delay)
                        continue
                    else:
                        # st.warning(f"Rate limit persisted for {current_model_name}. Switching model...")
                        break # Break retry loop to try next model
                
                # Handle Internal Errors (500s)
                elif "internal" in error_message or "overloaded" in error_message:
                    if attempt < max_retries:
                        time.sleep(base_delay)
                        continue
                    else:
                        break # Try next model
                
                # Handle Blocked Content or other API errors
                else:
                    st.error(f"Error with {current_model_name}: {str(e)}")
                    break # Try next model immediately for non-transient errors
        
    st.error(f"Failed to generate report after trying multiple models. Last error: {str(last_error)}")
    return None

def generate_text_report_with_retry(prompt, max_retries=3, base_delay=2, model_name='gemini-2.0-flash-lite'):
    """Generate text-based report with retry mechanism and model fallback"""
    
    # List of models to try in order
    models_to_try = [
        model_name,
        'gemini-2.0-flash-lite',
        'gemini-2.5-flash-lite',
        'gemini-flash-latest',
        'gemini-pro-latest'
    ]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_models = [x for x in models_to_try if not (x in seen or seen.add(x))]
    
    last_error = None
    
    for current_model_name in unique_models:
        try:
            model = genai.GenerativeModel(current_model_name)
            # st.info(f"Attempting with model: {current_model_name}")
        except Exception as e:
            continue
            
        for attempt in range(max_retries + 1):
            try:
                response = model.generate_content(prompt)
                if response.text:
                    return response.text
                
            except Exception as e:
                last_error = e
                error_message = str(e).lower()
                
                if "quota exceeded" in error_message or "429" in error_message or "resource exhausted" in error_message:
                    if attempt < max_retries:
                        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                        # st.warning(f"Rate limit on {current_model_name}. Retrying in {delay:.1f}s...")
                        time.sleep(delay)
                        continue
                    else:
                        # st.warning(f"Rate limit persisted for {current_model_name}. Switching model...")
                        break
                elif "internal" in error_message or "overloaded" in error_message:
                    if attempt < max_retries:
                        time.sleep(base_delay)
                        continue
                    else:
                        break
                else:
                    # st.error(f"Error with {current_model_name}: {str(e)}")
                    break
    
    st.error(f"Failed to generate report. Please try again later. Last error: {str(last_error)}")
    return None

def generate_report(image, prompt):
    """Generate report using Gemini API with retry mechanism (backward compatibility)"""
    return generate_report_with_retry(image, prompt)

def create_pdf_report(analysis_text, image=None, report_type="Medical Report", patient_info=None):
    """Create a PDF report with analysis results"""
    try:
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        
        # Create document
        doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=HexColor('#667eea'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph(report_type, title_style))
        story.append(Paragraph("AI-Powered Medical Analysis Report", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Patient Information
        if patient_info:
            story.append(Paragraph("Patient Information", heading_style))
            for key, value in patient_info.items():
                story.append(Paragraph(f"<b>{key}:</b> {value}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Timestamp
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Image (if provided)
        if image:
            # Save image to temporary file
            img_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            image.save(img_temp.name, 'PNG')
            
            # Add image to PDF
            story.append(Paragraph("Medical Image", heading_style))
            img = RLImage(img_temp.name, width=4*inch, height=3*inch)
            story.append(img)
            story.append(Spacer(1, 0.3*inch))
        
        # Analysis
        story.append(Paragraph("AI Analysis Results", heading_style))
        
        # Split text into paragraphs
        paragraphs = analysis_text.split('\n\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para.replace('\n', '<br/>'), styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        doc.build(story)
        
        # Read the PDF content
        with open(temp_file.name, 'rb') as f:
            pdf_data = f.read()
        
        return pdf_data
        
    except Exception as e:
        st.error(f"Error creating PDF report: {str(e)}")
        return None