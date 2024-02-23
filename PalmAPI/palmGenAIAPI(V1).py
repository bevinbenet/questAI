
import pprint
import google.generativeai as palm
import nltk


palm.configure(api_key='AIzaSyDQkQ7j1S5EtY5GVsV5j6R_mMYfIfapVZ0')


# In[3]:


models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
print(model)


# In[ ]:



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
some market segment (set of users). Many companies fin d it
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

section = 3
question = "Generate a "+section+" sections of questions,  using "+textbook+". Each section should have 5 questions and no need for answers.. Also give just the questions with no other text."
prompt1 = question


completion = palm.generate_text(
    model=model,
    prompt=prompt1,
    temperature=0,
    # The maximum length of the response
    max_output_tokens=1000,
)

print(completion.result)


# In[17]:


from nltk.tokenize import sent_tokenize

# Tokenize the text into sentences
sentences = sent_tokenize(completion.result)

# Extract sentences containing the word "Python"
desired_sentences = [sentence for sentence in sentences if "?" in sentence]

# Print the desired sentences
for sentence in desired_sentences:
    print(sentence)


# In[16]:


type(desired_sentences)


# In[17]:




# In[38]:


questionNumber=[]
markSection=[]
sectionNumber = int(input("Enter section number:"));


# In[39]:


for i in range(0,sectionNumber):
    questionNumber.append(int(input("Enter the number of question in section "+str(i+1)+" : ")));
    markSection.append(int(input("Enter the mark of each question in section "+str(i+1)+" : ")));
    

    


# In[40]:


print(questionNumber)
print(markSection)


# In[41]:


for sentence in desired_sentences:
    print(sentence)
    


# In[45]:


if(sum(questionNumber)==len(desired_sentences)):
    for i in range(0,sectionNumber):
        k=i+1
        print("\nSection "+ str(k));
   
        for j in range(questionNumber[i]):
            print(desired_sentences[int(j)]);

else:
    print("Error!! Recheck the section number and questions ")


        


# In[47]:


questionNumber=[]
markSection=[]
sectionNumber = 3;

questionNumber.append(8);
questionNumber.append(5);
questionNumber.append(2);

markSection.append(1);
markSection.append(2);
markSection.append(5);

if(sum(questionNumber)==len(desired_sentences)):
    for i in range(0,sectionNumber):
        k=i+1
        print("\nSection "+ str(k));
   
        for j in range(questionNumber[i]):
            print(desired_sentences[int(j)]);
else:
    print("Error!! Recheck the section number and questions ")


# In[ ]:




