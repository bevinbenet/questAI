import requests
import json
import pytesseract
from PIL import Image
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_question_paper(eName,prog,sub,secNum,imgName,quesMarks,time):

    genai.configure(api_key="AIzaSyA0VeSCntKzB9PVXxK4bujq1JCwiGsVT_8")

    #Code for connecting using API and running prompts
    try:
        #API model details
        generation_config = {
        "temperature": 1,
        "max_output_tokens": 5000,
        }
        model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)
    except: 
        print("Error with API key or network")
    #Exam Details
    examName = eName
    program  =  prog
    subject  = sub
    timeExam = time

    #This holds the number of questions and mark for each question in each section.
    #This should be made as user input

    sectionNumber = int(secNum)
    questionNumber = []
    markSection = []
    total=0
    for item in quesMarks:
        section = item['section']
        mark = item['marks']
        questionNumber.append(section)
        markSection.append(mark)

    for item in quesMarks:
        section = item['section']
        mark = item['marks']
        total += int(section) * int(mark)
    print(total)




    #Text based on which question is created.
    textbook = " "
    image_path = imgName
    try:
        pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
        # Open the image
        img = Image.open(image_path)

        # Extract text using Tesseract
        text = pytesseract.image_to_string(img)

        # Print the extracted text
        print(text)
        textbook = text

    except FileNotFoundError:
        print("Error: Image file not found. Please check the path.")

    except Exception as e:
        print(f"Error: {e}")

    '''
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = 'HYb4xri7Au9GhGs4TsraJIrSWZQY9vtn'

    # Specify the path to the image file on your system
    image_path = imgName

    # Open the image file
    with open(image_path, 'rb') as file:
        image_data = file.read()

    url = "https://api.apilayer.com/image_to_text/upload"

    headers = {
        'apikey': api_key
    }

    # The body of the request contains the image data
    body = image_data

    response = requests.post(url, headers=headers, data=body)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response content
        textbook = response.text
        #print(response.text)

    else:
        # Print the error message if the request failed
        print("Error:", response.text)'''

    #Final combined prompt
    finalPrompt='' 
    prompts = [] #Holds all the prompts for each section 
    prompts.append("Create questions on the criteria based on the text \" "+textbook+" \" which is from a textbook. Each question should be very unique .The criterias are:")
    for i in range(0,sectionNumber):
        k=i+1
        prompts.append("Create "+str(questionNumber[i])+" questions for section "+str(k)+" with each question having "+str(markSection[i])+" marks. ")
    prompts.append("Give as JSON data format and nothing else even on the start so questions can be easily extracted like.Strictly follow the format. The format should be:{\"questions\":[{\"question\":\"In the Internet model, which layer is responsible for error detection and correction?\",\"section\":1,\"marks\":1}...Rest of the questions..]}")
    #Joins all the individual prompts into single prompt
    for j in prompts:
        finalPrompt+=j
    #print(finalPrompt)
    #Executes the prompt 
    prompt_parts = finalPrompt
    response = model.generate_content(prompt_parts)
    response1 = response.text

    #prints the result
    #print(response.text)
    #Using JSON code
    json_data = response1
    #json_data = json_data.split('\n')[1:-1]
    #json_data = '\n'.join(json_data)
    # Provided JSON-formatted string output
    # Parse the JSON string into a Python dictionary
    data = json.loads(json_data)
   
    questions = []
    for section in data.values():
        for item in section:
            questions.append(item["question"])
           
   
    #Prints Questions
    def create_question_paper(file_path, questions):
        # Create a PDF document with A4 size
        doc = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=40, rightMargin=40, topMargin=30, bottomMargin=30)

        # Set font and styles
        styles = getSampleStyleSheet()

        question_style = ParagraphStyle(
            'CustomQuestion',
            parent=styles['BodyText'],
            fontSize=10,    # Change font size for questions
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
            fontSize=15,    # Change font size
            textColor=colors.black,  # Change text color
            alignment=1,     # Center-aligned
            fontName='Times-Roman', 
            fontWeight='Bold'  # Make text bold
        )

        content.append(Paragraph(examName, heading_style))
        content.append(Spacer(1, 10))  # Increase spacing above the first section heading

        content.append(Paragraph(program , heading_style))
        content.append(Spacer(1, 10))  # Increase spacing above the second section heading

        content.append(Paragraph(subject, heading_style))
        content.append(Spacer(1, 10))  # Increase spacing above the third section heading

        # Add time and marks information with time left-aligned and marks right-aligned on the same line
        time_marks_table_data = [[timeExam+" hours", str(total)+" marks"]]
        time_marks_table = Table(time_marks_table_data, colWidths=[250, 250])
        time_marks_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT'),
                                            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                                            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold')]))
        content.append(time_marks_table)

        # Add space before the first section heading
        content.append(Spacer(1, 20))  # Add space before the first section heading
        
        for i in range(0,sectionNumber):
            section = "Section "+str((i+1))
            # Add customized section heading with increased spacing, font size, and color
            section_heading_style = heading_style.clone('CustomHeadingSection')
            section_heading_style.spaceAfter = 10  # Adjust spacing for section headings
            content.append(Paragraph(section, section_heading_style))
            content.append(Spacer(1, 20))  # Increase spacing after each section heading

            # Add questions with customized font size
            for i in range(1, int(questionNumber[i]) + 1):
                if questions:
                    question_text = f"{i}. {questions.pop(0)}"  # Extract question from the list
                    content.append(Paragraph(question_text, question_style))
            content.append(Spacer(1, 20)) #Spacing before each section heading
        # Build the PDF document
        doc.build(content)
        return output_file
    output_file = "questionPaper.pdf"
    create_question_paper(output_file, questions)

    
