from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from io import BytesIO
from app.models.resume_model import ResumeDB

class PDFService:
    async def generate_pdf(self, resume: ResumeDB, template: str = "tech") -> bytes:
        """
        Generate PDF based on resume data and selected template
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        styles = getSampleStyleSheet()
        story = []
        
        data = resume.parsed_data
        if not data:
            data = {}
            
        # Add Name (Header)
        name = data.get("name", "Name Not Found")
        story.append(Paragraph(name, styles["Title"]))
        
        # Contact Info
        contact_info = []
        if data.get("email"): contact_info.append(data["email"])
        if data.get("phone"): contact_info.append(data["phone"])
        if data.get("location"): contact_info.append(data["location"])
        
        story.append(Paragraph(" | ".join(contact_info), styles["Normal"]))
        story.append(Spacer(1, 12))
        
        # Sections
        sections = ["Summary", "Experience", "Education", "Skills", "Projects"]
        
        for section in sections:
            if section.lower() in data and data[section.lower()]:
                # Section Header
                story.append(Paragraph(section.upper(), styles["Heading2"]))
                
                content = data[section.lower()]
                
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, str):
                             story.append(Paragraph(f"• {item}", styles["Normal"]))
                        elif isinstance(item, dict):
                            # Experience / Education items
                            title = item.get("title") or item.get("degree") or item.get("name")
                            company = item.get("company") or item.get("school")
                            date = item.get("duration") or item.get("year")
                            
                            if title:
                                story.append(Paragraph(f"<b>{title}</b>", styles["Heading3"]))
                            if company:
                                text = company
                                if date:
                                    text += f" | {date}"
                                story.append(Paragraph(text, styles["Normal"]))
                            
                            if "description" in item:
                                story.append(Paragraph(item["description"], styles["Normal"]))
                            if "bullets" in item and isinstance(item["bullets"], list):
                                for bullet in item["bullets"]:
                                    story.append(Paragraph(f"• {bullet}", styles["Normal"]))
                                    
                            story.append(Spacer(1, 6))
                elif isinstance(content, str):
                    story.append(Paragraph(content, styles["Normal"]))
                    
                story.append(Spacer(1, 12))
                
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

pdf_service = PDFService()
