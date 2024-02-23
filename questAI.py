import pprint
import json
import google.generativeai as genai
import nltk
from nltk.tokenize import sent_tokenize
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

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
examName = "END SEMESTER EXAM 2024"
program  =  "SEMESTER 3 : INTEGRATED M.Sc. PROGRAMME COMPUTER SCIENCE"
subject  = "COURSE : 21UP3CPSTA01 :PROBABILITY AND STATISTICS"

#This holds the number of questions and mark for each question in each section.
#This should be made as user input
questionNumber = [10,6,4]
markSection    = [1,2,5]
sectionNumber = 3



#Text based on which question is created.
textbook = """
Regional Internet Service Providers
Regional internet service providers or regional ISPs are smaller ISPs that are connected
to one or more national ISPs. They are at the third level of the hierarchy with a smaller
data rate.
Local Internet Service Providers
Local Internet service providers provide direct service to the end users. The local
ISPs can be connected to regional ISPs or directly to national ISPs. Most end users are
connected to the local ISPs. Note that in this sense, a local ISP can be a company that
just provides Internet services, a corporation with a network that supplies services to its
own employees, or a nonprofit organization, such as a college or a university, that runs
its own network. Each of these local ISPs can be connected to a regional or national
service provider.

1.4 PROTOCOLS AND STANDARDS
In this section, we define two widely used terms: protocols and standards. First, we
define protocol, which is synonymous with rule. Then we discuss standards, which are
agreed-upon rules.
Protocols
In computer networks, communication occurs between entities in different systems. An

entity is anything capable of sending or receiving information. However, two entities can-
not simply send bit streams to each other and expect to be understood. For communication

to occur, the entities must agree on a protocol. A protocol is a set of rules that govern data
communications. A protocol defines what is communicated, how it is communicated, and
when it is communicated. The key elements of a protocol are syntax, semantics, and timing.
o Syntax. The term syntax refers to the structure or format of the data, meaning the
order in which they are presented. For example, a simple protocol might expect the
first 8 bits of data to be the address of the sender, the second 8 bits to be the address
of the receiver, and the rest of the stream to be the message itself.
o Semantics. The word semantics refers to the meaning of each section of bits.
How is a particular pattern to be interpreted, and what action is to be taken based
on that interpretation? For example, does an address identify the route to be taken
or the final destination of the message?
o Timing. The term timing refers to two characteristics: when data should be sent
and how fast they can be sent. For example, if a sender produces data at 100 Mbps
but the receiver can process data at only 1 Mbps, the transmission will overload the
receiver and some data will be lost.
Standards
Standards are essential in creating and maintaining an open and competitive market for
equipment manufacturers and in guaranteeing national and international interoperability
of data and telecommunications technology and processes. Standards provide guidelines"""



finalPrompt='' #Final combined prompt
prompts = [] #Holds all the prompts for each section 
prompts.append("Create questions on the criteria based on the text \" "+textbook+" \" which is from a textbook. Each question should be very unique no matter what.No no no same questions.The criterias are:")
for i in range(0,sectionNumber):
    k=i+1
    prompts.append("Create "+str(questionNumber[i])+" questions for section "+str(k)+" with each question having "+str(markSection[i])+" marks. ")
prompts.append("Give each section as individual python list.Also give only correct number of questions in each section. Give as JSON data format")
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
json_data = json_data.split('\n')[1:-1]
json_data = '\n'.join(json_data)
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

    content.append(Paragraph(examName, heading_style))
    content.append(Spacer(1, 10))  # Increase spacing above the first section heading

    content.append(Paragraph(program , heading_style))
    content.append(Spacer(1, 10))  # Increase spacing above the second section heading

    content.append(Paragraph(subject, heading_style))
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
            if questions:
                question_text = f"{i}. {questions.pop(0)}"  # Extract question from the list
                content.append(Paragraph(question_text, question_style))
        content.append(Spacer(1, 20)) #Spacing before each section heading
    
    # Build the PDF document
    doc.build(content)

if __name__ == "__main__":
    output_file = "questionPaper1.pdf"

    # Create the question paper
    create_question_paper(output_file, questions)
