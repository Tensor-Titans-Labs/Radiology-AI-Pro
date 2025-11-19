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

def generate_report_with_retry(image, prompt, max_retries=3, base_delay=1):
    """Generate report with retry mechanism for rate limiting"""
    # Convert image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Create the model
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    
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
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    st.warning(f"Rate limit exceeded. Retrying in {delay:.1f} seconds... (Attempt {attempt + 1}/{max_retries + 1})")
                    time.sleep(delay)
                    continue
                else:
                    st.error(f"Rate limit exceeded after {max_retries + 1} attempts. Please try again later or consider upgrading your API plan.")
                    return None
            else:
                # For other errors, don't retry
                st.error(f"Error generating report: {str(e)}")
                return None
    
    return None

def generate_text_report_with_retry(prompt, max_retries=3, base_delay=1):
    """Generate text-based report with retry mechanism for rate limiting"""
    # Create the model
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    
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
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    st.warning(f"Rate limit exceeded. Retrying in {delay:.1f} seconds... (Attempt {attempt + 1}/{max_retries + 1})")
                    time.sleep(delay)
                    continue
                else:
                    st.error(f"Rate limit exceeded after {max_retries + 1} attempts. Please try again later or consider upgrading your API plan.")
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