import sys
import os
from flask import Flask, render_template, url_for, request
from questAI import generate_question_paper
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('quest.html')
UPLOAD_FOLDER = '/Users/bevinbenet/Desktop/college/Quest-AI/IMAGES'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

sectionQuesMarks = []
imageName=[]
@app.route('/submit', methods=['POST'])
def submit():
    institution_name= request.form.get('institution-name')
    exam_name= request.form.get('exam-name')
    subject_name= request.form.get('subject-name')
    exam_duration= request.form.get('exam-duration')
    exam_marks = request.form.get('exam-marks')
    num_of_sections = request.form.get('numSection')
    section1 = request.form.get('section1')

    
    for i in range(0,int(num_of_sections)):
        section_dict = {
            'section': request.form.get('section'+str(i)),
            'marks': request.form.get('markSection'+str(i))
        }
        sectionQuesMarks.append(section_dict)
    
    if 'files' in request.files:
        uploaded_files = request.files.getlist('files')
        for file in uploaded_files:
            # Save the uploaded file to a desired location
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            print(file.filename)
            image_path = "/Users/bevinbenet/Desktop/college/Quest-AI/IMAGES/" + file.filename
            print("File saved:", file.filename)
            imageName.append(image_path )
        print("Files uploaded successfully")
    else:
        print("No files received")
        return "No files received", 400
    try:
        generate_question_paper(exam_name,institution_name,subject_name,num_of_sections,image_path,sectionQuesMarks)

    except:
        return "Form submitted successfully but no Ques Created"
    
    return "Form submitted successfully"
        
app.config['SERVER_TIMEOUT'] = 120
if __name__ == '__main__':
    app.run(debug=True, port=8000)

