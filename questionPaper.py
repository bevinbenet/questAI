from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_question_paper(file_path):
    # Create a PDF document with A4 size
    doc = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=40, rightMargin=40, topMargin=30, bottomMargin=30)

    # Set font and styles
    styles = getSampleStyleSheet()

    question_style = ParagraphStyle(
        'CustomQuestion',
        parent=styles['BodyText'],
        fontSize=15,    # Change font size for questions
        spaceAfter=3,   # Add space after each question
        leading=20,
    )

    # Content for the question paper (adjust as needed)
    content = []

    # Add customized headings with increased spacing, font size, and color
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        spaceAfter=12,  # Increase spacing after heading
        fontSize=18,    # Change font size
        textColor=colors.darkblue,  # Change text color
        alignment=1,     # Center-aligned
        fontWeight='Bold'  # Make text bold
    )

    content.append(Paragraph("Your Exam Name", heading_style))
    content.append(Spacer(1, 10))  # Increase spacing above the first section heading

    content.append(Paragraph("Subject: Your Subject", heading_style))
    content.append(Spacer(1, 10))  # Increase spacing above the second section heading

    content.append(Paragraph("Date: Your Date", heading_style))
    content.append(Spacer(1, 10))  # Increase spacing above the third section heading

    # Add time and marks information with time left-aligned and marks right-aligned on the same line
    time_marks_table_data = [["Time: 2 hours", "Marks: 100"]]
    time_marks_table = Table(time_marks_table_data, colWidths=[250, 250])
    time_marks_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT'),
                                          ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                                          ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold')]))
    content.append(time_marks_table)

    # Add space before the first section heading
    content.append(Spacer(1, 20))  # Add space before the first section heading

    # Add sections with questions
    sections = [("Section A", 8), ("Section B", 6), ("Section C", 2)]

    for section, num_questions in sections:
        # Add customized section heading with increased spacing, font size, and color
        section_heading_style = heading_style.clone('CustomHeadingSection')
        section_heading_style.spaceAfter = 10  # Adjust spacing for section headings
        content.append(Paragraph(section, section_heading_style))
        content.append(Spacer(1, 20))  # Increase spacing after each section heading

        # Add questions with customized font size
        for i in range(1, num_questions + 1):
            question_text = f"{i}.Your question goes here. It may be a long question that might overflow to the next line if necessary."
            content.append(Paragraph(question_text, question_style))
        content.append(Spacer(1, 20)) #Spacing before each section heading
    # Build the PDF document
    doc.build(content)

if __name__ == "__main__":
    output_file = "questionPaper.pdf"
    create_question_paper(output_file)
