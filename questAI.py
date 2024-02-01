import pprint
import google.generativeai as palm
import nltk
from nltk.tokenize import sent_tokenize
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
palm.configure(api_key='AIzaSyCipXE392BMdk8cDQGFIYjsM4Xi9Pwk9Jo')

#Code for connecting using API and running prompts
try:
    #API model details
    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name
    print(model)

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
    Types of Software Development Projects
    A software development company is typically structured into a large
    number of teams that handle various types of software development
    projects. These software development projects concern the
    development of either software product or some software service. In
    the following subsections, we distinguish between these two types of
    software development projects.
    Software products
    We all know of a variety of software such as Microsoft’s Windows and the
    Office suite, Oracle DBMS, software accompanying a camcorder or a
    laser printer, etc. These software are available off-the-shelf for
    purchase and are used by a diverse range of customers. These are
    called generic software products since many users essentially use the
    same software. These can be purchased off-the-shelf by the customers.
    When a software development company wishes to develop a generic
    product, it first determines the features or functionalities that would be
    useful to a large cross section of users. Based on these, the
    development team draws up the product specification on its own. Of
    course, it may base its design discretion on feedbacks collected from a
    large number of users. Typically, eac h software product is targetted to
    some market segment (set of users). Many companies find it
    advantageous to develop product lines that target slightly different
    market segments based on variations of essentially the same software.
    For example, Microsoft targets desktops and laptops through its
    Windows 8 operating system, while it targets high-end mobile handsets
    through i t s Windows mobile operating system, and targets servers
    through its Windows server operating system.
    Software services
    A software service usually involves either development of a customised
    software or development of some specific part of a software in an
    outsourced mode. A customised software is developed according to the
    specification drawn up by one or at most a few customers. These need
    to be developed in a short time frame (typically a couple of months),
    and at the same time the development cost must be low. Usually, a
    developing company develops customised software by tailoring some of
    its existing software. For example, when an academic institution wishes
    to have a software that would automate its important activities such as
    student registration, grading, and fee collection; companies would
    normally develop such a software as a customised product. This means
    that for developing a customised software, the developing company
    would normally tailor one of its existing software products that it might
    have developed in the past for some other academic institution.
    In a customised software development project, a large part of the software
    is reused from the code of related software that the company might have
    already developed. Usually, only a small part of the software that is specific
    to some client is developed. For example, suppose a software development
    organisation has developed an academic automation software that
    automates the student registration, grading, Establishment, hostel and other
    aspects of an academic institution. When a new educational institution
    requests for developing a software for automation of its activities, a large
    part of the existing software would be reused. However, a small part of the
    existing code may be modified to take into account small variations in the
    required features. For example, a software might have been developed for an
    academic institute that offers only regular residential programs, the
    educational institute that has now requested for a software to automate its
    activities also offers a distance mode post graduate program where the
    teaching and sessional evaluations are done by the local centres.
    Another type of software service i s outsourced software. Sometimes, it can
    make good commercial sense for a company developing a large project to
    outsource some parts of its development work to other companies. The
    reasons behind such a decision may be many. For example, a company might
    consider the outsourcing option, if it feels that it does not have sufficient
    expertise to develop some specific parts of the software; or if it determines
    that some parts can be developed cost-effectively by another company. Since
    an outsourced project i s a small part of some larger project, outsourced
    projects are usually small in size and need to be completed within a few
    months or a few weeks of time.
    The types of development projects that are being undertaken by a
    company can have an impact on its profitability. For example, a company that
    has developed a generic software product usually gets an uninterrupted
    stream of revenue that is spread over several years. However, this entails
    substantial upfront investment in developing the software and any return on
    this investment is subject to the risk of customer acceptance. On the other
    hand, outsourced projects are usually less risky, but fetch only one time
    revenue to the developing company."""
    
  

    finalPrompt='' #Final combined prompt
    prompts = [] #Holds all the prompts for each section 
    prompts.append("Create questions on the criteria based on the text \" "+textbook+" \" which is from a textbook. Each question should be very unique no matter what.No no no same questions. Give just questions with no section headings.The criterias are:")
    for i in range(0,sectionNumber):
        k=i+1
        prompts.append("Create "+str(questionNumber[i])+" questions for section "+str(k)+" with each question having mark "+str(markSection[i])+".")

    #Joins all the individual prompts into single prompt
    for j in prompts:
        finalPrompt+=j
    #print(finalPrompt)
    #Executes the prompt 
    completion = palm.generate_text(
        model=model,
        prompt=finalPrompt,
        temperature=0,
        # The maximum length of the response
        max_output_tokens=1000,
    )

    #prints the result
    print(completion.result)
except: 
    print("Error with API key or network")

#This extracts questions only from result
sentences = sent_tokenize(completion.result)
desired_sentences = [sentence for sentence in sentences if "?" in sentence]
desired_sentences = [sentence for sentence in sentences if "." in sentence]

# Print extracted questions
#for sentence in desired_sentences:
    #print(sentence)

##Question Paper Code##

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
            question_text = f"{i}.Your question goes here. It may be a long question that might overflow to the next line if necessary."
            content.append(Paragraph(question_text, question_style))
        content.append(Spacer(1, 20)) #Spacing before each section heading
    # Build the PDF document
    doc.build(content)

if __name__ == "__main__":
    output_file = "questionPaper.pdf"
    create_question_paper(output_file)




#Logic for arranging questions into sections
questionNo=1 #question number variable
if(sum(questionNumber)==len(desired_sentences)):
    for i in range(0,sectionNumber):
        k=i+1
        print("\nSection "+ str(k));
   
        for j in range(questionNumber[i]):
            print(str(questionNo)+"."+desired_sentences[int(j)]);
            questionNo+=1
else:
    print("Error!! Recheck the section number and questions ")

#Code for printing as question paper format