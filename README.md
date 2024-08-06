![logo](https://github.com/user-attachments/assets/5ce029f6-bdf1-4f82-beac-de624dabcf2d)
# What is it?
ArcaneExamz is my humble script for **generating randomized exams with questions and answers randomization** using LaTeX and Python. You can generate unique variants of your exam in seconds. You can also generate version with solutions at the same time. So far it works with **open and multichoice** questions.


Development is still in progress; tutorials will be added in the foreseeable future.
So far: works on windows, make sure you have latex installed - it's used for compilation... check in pycharm, it should work...
# I want to see how it works!
Right, check the PDF files in the repository. You can see that there two variants of the test. The questions come from .CSV files (you can edit them in excel, make sure to save them back as UTF-8 CSV). You can use any number of source files. I use one for current subject matter questions, the second file (old questions) are from the previous exams. You can edit how many questions from which category will be there. It's up to you. 

My tests are cumulative - some questions are part of the current subject matter, and some questions are from older tests - to keep the facts in the long-term memory and create logical connections. This script randomly picks _n_ questions from the files defined by user. If there are MULTI - multichoice questions, the order of them is also randomized. 

# How it works?
For me as a teacher it's important that you understand how it works. (full documentation will be added in the future) Script loads data from CSV files.
![Untitled 5](https://github.com/user-attachments/assets/070eb09c-20db-4621-969a-a4ac87650284)

# Requirements
- Windows (tested on W11)
- python installed
- pdflatex installed (check if pdflatex command in cmd works, if so, you should be fine)
- PyMuPDF==1.24.9

# Contribute
I write this script in my time, and I dare my students (or you) to help with development. There are several things to be added... if you miss something, please create an issue.
