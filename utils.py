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

def generate_report_with_retry(image, prompt, max_retries=5, base_delay=2, model_name='gemini-1.5-flash'):
    """Generate report with retry mechanism for rate limiting"""
    # Convert image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # List of fallback models in order of preference
    fallback_models = [
        model_name,
        'gemini-1.5-flash',
        'gemini-pro-vision',
        'gemini-1.0-pro-vision'
    ]
    
    model = None
    for model_name in fallback_models:
        try:
            model = genai.GenerativeModel(model_name)
            st.info(f"Using model: {model_name}")
            break
        except Exception as e:
            st.warning(f"Failed to create model {model_name}: {str(e)}")
            continue
    
    if model is None:
        st.error("Failed to create any Gemini model. Please check your API key and network connection.")
        return None
    
    for attempt in range(max_retries + 1):
        try:
            # Generate content with the image and prompt
            response = model.generate_content([
                prompt,
                {'mime_type': 'image/png', 'data': img_byte_arr}
            ])
            
            # Return the response text if successful
            return response.text
            
        except Exception as e:
            # Check if it's a rate limit error
            error_message = str(e).lower()
            if "quota exceeded" in error_message or "429" in error_message:
                if attempt < max_retries:
                    # Calculate delay with exponential backoff and jitter
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 2)
                    st.warning(f"Rate limit exceeded. Retrying in {delay:.1f} seconds... (Attempt {attempt + 1}/{max_retries + 1})")
                    time.sleep(delay)
                    continue
                else:
                    st.error(f"Rate limit exceeded after {max_retries + 1} attempts. Please try again later or consider upgrading your API plan.")
                    st.info("💡 Tips to reduce rate limit issues:\n1. Try using the application during off-peak hours (early morning or late night)\n2. Consider upgrading to a paid Gemini API plan for higher quotas\n3. Reduce the frequency of requests")
                    return None
            elif "internal" in error_message and "error" in error_message:
                # Handle internal errors by retrying with a different model
                if attempt < max_retries:
                    st.warning(f"Internal error occurred. Trying with a different model... (Attempt {attempt + 1}/{max_retries + 1})")
                    # Try next fallback model
                    next_model_index = fallback_models.index(model.model_name) + 1 if model.model_name in fallback_models else 0
                    if next_model_index < len(fallback_models):
                        try:
                            model = genai.GenerativeModel(fallback_models[next_model_index])
                            st.info(f"Switching to model: {fallback_models[next_model_index]}")
                        except:
                            pass
                    time.sleep(base_delay * (attempt + 1))
                    continue
                else:
                    st.error(f"Internal error after {max_retries + 1} attempts. Please try again later.")
                    return None
            else:
                # For other errors, don't retry
                st.error(f"Error generating report: {str(e)}")
                return None
    
    return None

def generate_text_report_with_retry(prompt, max_retries=5, base_delay=2, model_name='gemini-1.5-flash'):
    """Generate text-based report with retry mechanism for rate limiting"""
    # List of fallback models in order of preference
    fallback_models = [
        model_name,
        'gemini-1.5-flash',
        'gemini-pro',
        'gemini-1.0-pro'
    ]
    
    model = None
    for model_name in fallback_models:
        try:
            model = genai.GenerativeModel(model_name)
            st.info(f"Using model: {model_name}")
            break
        except Exception as e:
            st.warning(f"Failed to create model {model_name}: {str(e)}")
            continue
    
    if model is None:
        st.error("Failed to create any Gemini model. Please check your API key and network connection.")
        return None
    
    for attempt in range(max_retries + 1):
        try:
            # Generate content with the prompt
            response = model.generate_content(prompt)
            
            # Return the response text if successful
            return response.text
            
        except Exception as e:
            # Check if it's a rate limit error
            error_message = str(e).lower()
            if "quota exceeded" in error_message or "429" in error_message:
                if attempt < max_retries:
                    # Calculate delay with exponential backoff and jitter
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 2)
                    st.warning(f"Rate limit exceeded. Retrying in {delay:.1f} seconds... (Attempt {attempt + 1}/{max_retries + 1})")
                    time.sleep(delay)
                    continue
                else:
                    st.error(f"Rate limit exceeded after {max_retries + 1} attempts. Please try again later or consider upgrading your API plan.")
                    st.info("💡 Tips to reduce rate limit issues:\n1. Try using the application during off-peak hours (early morning or late night)\n2. Consider upgrading to a paid Gemini API plan for higher quotas\n3. Reduce the frequency of requests")
                    return None
            elif "internal" in error_message and "error" in error_message:
                # Handle internal errors by retrying with a different model
                if attempt < max_retries:
                    st.warning(f"Internal error occurred. Trying with a different model... (Attempt {attempt + 1}/{max_retries + 1})")
                    # Try next fallback model
                    next_model_index = fallback_models.index(model.model_name) + 1 if model.model_name in fallback_models else 0
                    if next_model_index < len(fallback_models):
                        try:
                            model = genai.GenerativeModel(fallback_models[next_model_index])
                            st.info(f"Switching to model: {fallback_models[next_model_index]}")
                        except:
                            pass
                    time.sleep(base_delay * (attempt + 1))
                    continue
                else:
                    st.error(f"Internal error after {max_retries + 1} attempts. Please try again later.")
                    return None
            else:
                # For other errors, don't retry
                st.error(f"Error generating report: {str(e)}")
                return None
    
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