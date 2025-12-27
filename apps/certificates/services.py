"""
Service for PDF certificate generation using ReportLab.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from django.core.files.base import ContentFile
from django.conf import settings
import io
from datetime import datetime


def generate_certificate_pdf(certificate):
    """
    Generate a PDF certificate for course completion.
    
    Args:
        certificate: Certificate model instance
    
    Returns:
        ContentFile: PDF file content
    """
    buffer = io.BytesIO()
    
    # Create PDF
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Set colors
    primary_color = colors.HexColor('#1e40af')  # Blue
    gold_color = colors.HexColor('#d97706')  # Gold
    
    # Draw border
    p.setStrokeColor(primary_color)
    p.setLineWidth(3)
    p.rect(30, 30, width - 60, height - 60)
    
    # Inner decorative border
    p.setStrokeColor(gold_color)
    p.setLineWidth(1)
    p.rect(40, 40, width - 80, height - 80)
    
    # Title
    p.setFont("Helvetica-Bold", 48)
    p.setFillColor(primary_color)
    p.drawCentredString(width / 2, height - 120, "CERTIFICATE")
    
    p.setFont("Helvetica", 24)
    p.setFillColor(colors.black)
    p.drawCentredString(width / 2, height - 160, "OF COMPLETION")
    
    # Decorative line
    p.setStrokeColor(gold_color)
    p.setLineWidth(2)
    p.line(150, height - 180, width - 150, height - 180)
    
    # "This is to certify that"
    p.setFont("Helvetica", 14)
    p.setFillColor(colors.grey)
    p.drawCentredString(width / 2, height - 230, "This is to certify that")
    
    # Student name
    p.setFont("Helvetica-Bold", 32)
    p.setFillColor(primary_color)
    p.drawCentredString(width / 2, height - 280, certificate.student_name)
    
    # Underline for name
    name_width = p.stringWidth(certificate.student_name, "Helvetica-Bold", 32)
    p.setStrokeColor(gold_color)
    p.setLineWidth(1)
    p.line(
        (width - name_width) / 2,
        height - 290,
        (width + name_width) / 2,
        height - 290
    )
    
    # "has successfully completed"
    p.setFont("Helvetica", 14)
    p.setFillColor(colors.grey)
    p.drawCentredString(width / 2, height - 330, "has successfully completed the course")
    
    # Course name
    p.setFont("Helvetica-Bold", 24)
    p.setFillColor(colors.black)
    
    # Handle long course names
    course_name = certificate.course_name
    if len(course_name) > 50:
        # Split into two lines
        words = course_name.split()
        line1 = ""
        line2 = ""
        for word in words:
            if len(line1 + word) < 50:
                line1 += word + " "
            else:
                line2 += word + " "
        p.drawCentredString(width / 2, height - 380, line1.strip())
        p.drawCentredString(width / 2, height - 410, line2.strip())
        y_offset = 410
    else:
        p.drawCentredString(width / 2, height - 380, course_name)
        y_offset = 380
    
    # Date
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.grey)
    completion_date = certificate.completion_date.strftime("%B %d, %Y")
    p.drawCentredString(width / 2, height - y_offset - 60, f"Completed on {completion_date}")
    
    # Certificate ID
    p.setFont("Helvetica", 10)
    p.drawCentredString(width / 2, height - y_offset - 90, f"Certificate ID: {certificate.certificate_id}")
    
    # Instructor signature section
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.black)
    p.drawCentredString(width / 2, 150, certificate.instructor_name)
    
    p.setStrokeColor(colors.black)
    p.setLineWidth(1)
    p.line(width / 2 - 100, 145, width / 2 + 100, 145)
    
    p.setFont("Helvetica", 10)
    p.setFillColor(colors.grey)
    p.drawCentredString(width / 2, 130, "Course Instructor")
    
    # Footer
    p.setFont("Helvetica", 8)
    p.drawCentredString(width / 2, 80, "E-Learning Platform")
    p.drawCentredString(width / 2, 65, f"Verify at: {settings.FRONTEND_URL}/certificates/verify/{certificate.id}/")
    
    # Save PDF
    p.showPage()
    p.save()
    
    # Get PDF content
    buffer.seek(0)
    return ContentFile(buffer.getvalue(), name=f'certificate_{certificate.certificate_id}.pdf')
