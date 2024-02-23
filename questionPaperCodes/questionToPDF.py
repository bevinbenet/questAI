from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas

def create_question_paper():
    # Set up PDF document
    filename = "question_paper.pdf"
    pdf_canvas = canvas.Canvas(filename, pagesize=landscape(letter))

    # Set font
    pdf_canvas.setFont("Helvetica", 10)

    # Main heading
    pdf_canvas.setFont("Helvetica-Bold", 14)
    pdf_canvas.drawCentredString(297/2, 800, "College Name")

    # Sub heading
    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawCentredString(297/2, 780, "Course Name")

    # Section 1
    draw_section(pdf_canvas, "Section 1", "Time: 1 hour", "Marks: 20", 720, [
        "What is the capital of France?",
        "Who wrote 'Romeo and Juliet'?",
        # Add more questions as needed
    ])

    # Section 2
    draw_section(pdf_canvas, "Section 2", "Time: 30 minutes", "Marks: 10", 580, [
        "Define photosynthesis.",
        "Explain Newton's first law of motion.",
        # Add more questions as needed
    ])

    # Section 3
    draw_section(pdf_canvas, "Section 3", "Time: 15 minutes", "Marks: 5", 440, [
        "Question 1 in Section 3",
        "Question 2 in Section 3",
        # Add more questions as needed
    ])

    pdf_canvas.save()

def draw_section(canvas, section_title, time, marks, y_position, questions):
    # Section number
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(20, y_position, section_title)

    # Time
    canvas.setFont("Helvetica", 10)
    canvas.drawString(60, y_position, f"Time: {time}")

    # Marks
    canvas.drawString(180, y_position, f"Marks: {marks}")

    # Questions
    y_position -= 20
    for i, question in enumerate(questions, start=1):
        y_position -= 12
        canvas.drawString(60, y_position, f"{i}. {question}")

# Create the question paper
create_question_paper()
