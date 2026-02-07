import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame, PageTemplate, BaseDocTemplate, FrameBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from app.schemas.resume import Resume
from typing import List, Dict
import os

class SimranStylePDFGenerator:
    def __init__(self):
        # Color scheme matching the image
        self.primary_blue = HexColor('#4A90E2')  # Main blue color
        self.dark_blue = HexColor('#2C5282')    # Darker blue for text
        self.light_gray = HexColor('#F7F9FC')   # Light background
        self.dark_gray = HexColor('#4A5568')    # Dark text
        self.medium_gray = HexColor('#718096')  # Medium gray for details
        
        # Layout dimensions
        self.page_width = letter[0]
        self.page_height = letter[1]
        self.sidebar_width = 2.5 * inch
        self.main_content_width = self.page_width - self.sidebar_width - 0.5 * inch
        
    def generate_resume_pdf(self, resume: Resume) -> bytes:
        """Generate PDF matching Simran's resume style"""
        buffer = io.BytesIO()
        
        # Create custom document with frames
        doc = BaseDocTemplate(
            buffer,
            pagesize=letter,
            topMargin=0,
            bottomMargin=0,
            leftMargin=0,
            rightMargin=0
        )
        
        # Define frames for two-column layout
        sidebar_frame = Frame(
            0, 0,
            self.sidebar_width, self.page_height,
            leftPadding=20, rightPadding=10,
            topPadding=30, bottomPadding=30,
            id='sidebar'
        )
        
        main_frame = Frame(
            self.sidebar_width + 0.25 * inch, 0,
            self.main_content_width, self.page_height,
            leftPadding=20, rightPadding=20,
            topPadding=30, bottomPadding=30,
            id='main'
        )
        
        # Create page template
        page_template = PageTemplate(
            id='resume_template',
            frames=[sidebar_frame, main_frame],
            onPage=self._draw_background
        )
        
        doc.addPageTemplates([page_template])
        
        # Create styles
        styles = self._create_styles()
        
        # Build content
        story = []
        
        # Sidebar content
        story.extend(self._build_sidebar_content(resume, styles))
        
        # Main content
        story.extend(self._build_main_content(resume, styles))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def _draw_background(self, canvas, doc):
        """Draw the blue sidebar background"""
        canvas.saveState()
        
        # Draw blue sidebar
        canvas.setFillColor(self.primary_blue)
        canvas.rect(0, 0, self.sidebar_width, self.page_height, fill=1)
        
        # Draw light background for main content
        canvas.setFillColor(self.light_gray)
        canvas.rect(self.sidebar_width, 0, self.main_content_width + 0.5 * inch, self.page_height, fill=1)
        
        canvas.restoreState()
    
    def _create_styles(self) -> Dict:
        """Create custom styles matching the design"""
        base_styles = getSampleStyleSheet()
        
        styles = {
            # Sidebar styles (white text on blue)
            'sidebar_name': ParagraphStyle(
                'SidebarName',
                parent=base_styles['Normal'],
                fontSize=28,
                fontName='Helvetica-Bold',
                textColor=colors.white,
                alignment=TA_LEFT,
                spaceAfter=10,
                leading=32
            ),
            
            'sidebar_section_header': ParagraphStyle(
                'SidebarSectionHeader',
                parent=base_styles['Normal'],
                fontSize=16,
                fontName='Helvetica-Bold',
                textColor=colors.white,
                alignment=TA_LEFT,
                spaceBefore=25,
                spaceAfter=12,
                borderWidth=0,
                borderPadding=0
            ),
            
            'sidebar_contact': ParagraphStyle(
                'SidebarContact',
                parent=base_styles['Normal'],
                fontSize=10,
                fontName='Helvetica',
                textColor=colors.white,
                alignment=TA_LEFT,
                spaceAfter=8,
                leftIndent=15
            ),
            
            'sidebar_skill': ParagraphStyle(
                'SidebarSkill',
                parent=base_styles['Normal'],
                fontSize=11,
                fontName='Helvetica',
                textColor=colors.white,
                alignment=TA_LEFT,
                spaceAfter=6,
                leftIndent=15,
                bulletIndent=10
            ),
            
            # Main content styles
            'main_section_header': ParagraphStyle(
                'MainSectionHeader',
                parent=base_styles['Normal'],
                fontSize=18,
                fontName='Helvetica-Bold',
                textColor=self.primary_blue,
                alignment=TA_LEFT,
                spaceBefore=25,
                spaceAfter=15,
                borderWidth=2,
                borderColor=self.primary_blue,
                borderPadding=8
            ),
            
            'main_content': ParagraphStyle(
                'MainContent',
                parent=base_styles['Normal'],
                fontSize=11,
                fontName='Helvetica',
                textColor=self.dark_gray,
                alignment=TA_LEFT,
                spaceAfter=8,
                leading=14
            ),
            
            'job_title': ParagraphStyle(
                'JobTitle',
                parent=base_styles['Normal'],
                fontSize=14,
                fontName='Helvetica-Bold',
                textColor=self.dark_gray,
                alignment=TA_LEFT,
                spaceAfter=4
            ),
            
            'job_company': ParagraphStyle(
                'JobCompany',
                parent=base_styles['Normal'],
                fontSize=12,
                fontName='Helvetica',
                textColor=self.dark_gray,
                alignment=TA_LEFT,
                spaceAfter=2
            ),
            
            'job_location': ParagraphStyle(
                'JobLocation',
                parent=base_styles['Normal'],
                fontSize=10,
                fontName='Helvetica-Oblique',
                textColor=self.medium_gray,
                alignment=TA_LEFT,
                spaceAfter=8
            ),
            
            'bullet_point': ParagraphStyle(
                'BulletPoint',
                parent=base_styles['Normal'],
                fontSize=10,
                fontName='Helvetica',
                textColor=self.dark_gray,
                alignment=TA_LEFT,
                spaceAfter=4,
                leftIndent=15,
                bulletIndent=10
            ),
            
            'education_degree': ParagraphStyle(
                'EducationDegree',
                parent=base_styles['Normal'],
                fontSize=12,
                fontName='Helvetica-Bold',
                textColor=self.dark_gray,
                alignment=TA_LEFT,
                spaceAfter=2
            ),
            
            'education_details': ParagraphStyle(
                'EducationDetails',
                parent=base_styles['Normal'],
                fontSize=11,
                fontName='Helvetica',
                textColor=self.dark_gray,
                alignment=TA_LEFT,
                spaceAfter=4
            )
        }
        
        return styles
    
    def _build_sidebar_content(self, resume: Resume, styles: Dict) -> List:
        """Build sidebar content (left column)"""
        content = []
        
        # Name
        content.append(Paragraph(resume.name, styles['sidebar_name']))
        content.append(Spacer(1, 20))
        
        # Contact Information (with icons)
        if resume.phone or resume.email or resume.location:
            content.append(Paragraph("📞 Contact", styles['sidebar_section_header']))
            
            if resume.phone:
                content.append(Paragraph(f"📱 {resume.phone}", styles['sidebar_contact']))
            if resume.email:
                content.append(Paragraph(f"✉️ {resume.email}", styles['sidebar_contact']))
            if resume.location:
                content.append(Paragraph(f"📍 {resume.location}", styles['sidebar_contact']))
        
        # Skills Section
        if resume.skills:
            content.append(Paragraph("📊 Skills", styles['sidebar_section_header']))
            
            for skill in resume.skills:
                content.append(Paragraph(f"• {skill}", styles['sidebar_skill']))
        
        return content
    
    def _build_main_content(self, resume: Resume, styles: Dict) -> List:
        """Build main content (right column)"""
        content = []
        
        # Add frame break to move to main content area
        content.append(FrameBreak())
        
        # Professional Summary (if exists)
        if resume.summary:
            content.append(Paragraph(resume.summary, styles['main_content']))
            content.append(Spacer(1, 20))
        
        # Education Section
        if resume.education:
            content.append(Paragraph("🎓 Education", styles['main_section_header']))
            
            for edu in resume.education:
                if edu.school:
                    content.append(Paragraph(edu.school, styles['job_title']))
                
                degree_text = ""
                if edu.degree:
                    degree_text = edu.degree
                if edu.gpa:
                    degree_text += f", CGPA: {edu.gpa}"
                
                if degree_text:
                    content.append(Paragraph(degree_text, styles['education_details']))
                
                if hasattr(edu, 'location') and edu.location:
                    content.append(Paragraph(edu.location, styles['job_location']))
                
                if edu.year:
                    content.append(Paragraph(edu.year, styles['education_details']))
                
                content.append(Spacer(1, 15))
        
        # Experience Section
        if resume.experience:
            content.append(Paragraph("💼 Experience", styles['main_section_header']))
            
            for exp in resume.experience:
                if exp.company:
                    content.append(Paragraph(exp.company, styles['job_title']))
                
                if exp.title:
                    content.append(Paragraph(exp.title, styles['job_company']))
                
                if exp.location:
                    content.append(Paragraph(exp.location, styles['job_location']))
                
                # Bullet points
                for bullet in exp.bullets:
                    content.append(Paragraph(f"• {bullet}", styles['bullet_point']))
                
                content.append(Spacer(1, 15))
        
        # Awards Section (if any achievements)
        awards = [
            "Selected in Top 10 teams in Innoquest3.0",
            "In Top 1000 teams in Vibe hack 2.0", 
            "In Top 5000 teams in Build with India Hackathon"
        ]
        
        if awards:
            content.append(Paragraph("🏆 Awards", styles['main_section_header']))
            
            for award in awards:
                content.append(Paragraph(f"• {award}", styles['bullet_point']))
            
            content.append(Spacer(1, 15))
        
        # Certifications Section
        if resume.certifications:
            content.append(Paragraph("🎖️ Certifications", styles['main_section_header']))
            
            for cert in resume.certifications:
                content.append(Paragraph(f"• {cert}", styles['bullet_point']))
        
        return content

# Service integration
class SimranStylePDFService:
    def __init__(self):
        self.generator = SimranStylePDFGenerator()
    
    async def generate_simran_style_pdf(self, resume: Resume) -> bytes:
        """Generate PDF in Simran's exact style"""
        return self.generator.generate_resume_pdf(resume)

# Singleton instance
simran_pdf_service = SimranStylePDFService()

