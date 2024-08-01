import fitz
import csv
import os
import random


def check_overflow(questions_open_new, questions_open_old, questions_mcq_new, questions_mcq_old,
                   bank_open_questions_new, bank_open_questions_old, bank_mcq_questions_new, bank_mcq_questions_old):
    """Checks if the requested number of questions is not higher than available questions in question banks.
    If so, requested number gets adjusted to fit available questions."""

    # OKAY, THIS SUCKS, MAYBE I SHOULD REWRITE IT IN THE FORESEEABLE FUTURE
    if questions_open_new > len(bank_open_questions_new):
        questions_open_new = len(bank_open_questions_new)

    if questions_open_old > len(bank_open_questions_old):
        questions_open_old = len(bank_open_questions_old)

    if questions_mcq_new > len(bank_mcq_questions_new):
        questions_mcq_new = len(bank_mcq_questions_new)

    if questions_mcq_old > len(bank_mcq_questions_old):
        questions_mcq_old = len(bank_mcq_questions_old)

    return questions_open_new, questions_open_old, questions_mcq_new, questions_mcq_old


def create_temp():
    """Creates temp directory for temporary files from the pdflatex compilation process."""

    path = "temp"
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)


def randomize_order(question_bank, questions_number):
    """Generates list of numbers in random order without repetition. Length is related to number of questions to
     be generated. This order is used for randomizing question order. """
    return random.sample(range(0, len(question_bank)), questions_number)


def merge_pdfs(filename, pdf_filenames_list, pdf_filenames_solution_list, output_solution_switch):
    """Merges all PDFs from pdf_names list (temp folder) into one: test_name.pdf,
    same applies for solution file if answer_switch = True"""

    mergepdf = fitz.open()

    for pdf in pdf_filenames_list:
        with fitz.open(pdf) as filenames_to_merge:
            mergepdf.insert_pdf(filenames_to_merge)
    mergepdf.save(filename + ".pdf")

    if output_solution_switch:
        mergepdf = fitz.open()
        for pdf in pdf_filenames_solution_list:
            with fitz.open(pdf) as filenames_to_merge:
                mergepdf.insert_pdf(filenames_to_merge)
        mergepdf.save(filename + "_answers.pdf")


def load_csv_into_list(questions_file, question_type):
    """Loads data row by row from CSVs based on question type, question source file into a list."""

    temporary_bank = []

    for file in questions_file:
        with open(file, newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader:
                if row[0] == question_type:
                    temporary_bank.append(row)

    return temporary_bank


def write_content_header(filename, version, testid, paper_size, font_size, landscape, language, header_left,
                         header_center, header_right):
    """Writes header with defined variables into .tex files."""

    if landscape:
        landscape = ",landscape"
    else:
        landscape = ""

    """Writes header into .tex file with several variables."""
    content_open = [
        "\\documentclass[addpoints,"+font_size+"pt,"+paper_size+"paper]{exam}",
        "\\usepackage[utf8]{inputenc}",
        "\\usepackage["+language+"]{babel}",
        "\\usepackage[left=1.5cm,right=1.5cm,top=2cm,bottom=2cm"+landscape+"]{geometry}",
        "\\newcommand{\\tf}[1][{}]{\\fillin[#1][0.5in]}",
        "\\pointsinleftmargin",
        "\\boxedpoints",
        "\\begin{document}",
        "\\pagestyle{headandfoot}",
        # "\\header{INF 1.G}{Name: \\fillin}{Points: \hspace{5pt} / \\numpoints }",
        "\\header{"+header_left+"}{"+header_center+"}{"+header_right+"}",
        "\\headrule",
        "\\footer{ArchaneExamz v" + version + "}{Test ID: " + str(testid + 1) + "}{\\thepage\,/\,\\numpages}",
        "\\footrule",
        "",
        "\\begin{questions}"]

    with open(filename + ".tex", 'w', encoding="utf-8") as f:
        for line in content_open:
            f.write(line)
            f.write('\n')


def write_content_open_question(random_order, question_bank, filename):
    """Generates open questions and writes them into .tex file."""

    for n in range(0, len(random_order)):
        # BY PICKING ELEMENTS ONE BY ONE FROM RANDOMIZED LIST YOU GET THE REQUIRED RANDOMIZATION
        x = random_order[n]

        question = question_bank[x][1]
        solution = question_bank[x][7]

        content_body = [
            "\\question " + question,
            # "\\fillwithdottedlines{3cm}",
            "\\begin{solution}",
            solution,
            "\\end{solution}",
            ""
        ]

        # WRITE CONTENT INTO .TEX FILE
        with open(filename + ".tex", 'a', encoding="utf-8") as f:
            for line in content_body:
                f.write(line)
                f.write('\n')


def write_content_mcq_question(random_order, question_bank, filename):
    """Generates multi-choice questions and writes them into .tex file."""

    for n in range(0, len(random_order)):
        # BY PICKING ELEMENTS ONE BY ONE FROM RANDOMIZED LIST YOU GET THE REQUIRED RANDOMIZATION

        x = random_order[n]
        question = question_bank[x][1]

        # PARSING CHOICES - MUST HAPPEN BEFORE SHUFFLING, OTHERWISE THE CORRECT CHOICE IS LOST
        choice1 = "\\CorrectChoice " + question_bank[x][2]
        choice2 = "\\choice " + question_bank[x][3]
        choice3 = "\\choice " + question_bank[x][4]
        choice4 = "\\choice " + question_bank[x][5]
        choice5 = "\\choice " + question_bank[x][6]
        solution = question_bank[x][7]

        # RANDOMIZING CHOICE ORDER WITH RANDOM.SHUFFLE
        choices = [choice1, choice2, choice3, choice4, choice5]
        random.shuffle(choices)

        content_body = [
            "\\question " + question,
            "",
            "\\begin{oneparchoices}",
            choices[0],
            choices[1],
            choices[2],
            choices[3],
            choices[4],
            "\\end{oneparchoices}",
            "\\begin{solution}",
            solution,
            "\\end{solution}",
            ""
        ]

        # WRITE CONTENT INTO .TEX FILE
        with open(filename + ".tex", 'a', encoding="utf-8") as f:
            for line in content_body:
                f.write(line)
                f.write('\n')


def write_content_close(filename):
    """Writes closing content into .tex file"""

    content_close = [
        "\\end{questions}",
        "\\end{document}"
    ]
    with open(filename + ".tex", 'a', encoding="utf-8") as f:
        for line in content_close:
            f.write(line)
            f.write('\n')


def output_answers(filename):
    """Creates a copy of the current .tex file, inserts \\printanswers argument and saves the file
    for future compilation."""

    with open(filename + ".tex", 'r', encoding="utf-8") as original_file:
        # Read the contents of the original file
        file_contents = original_file.readlines()

    # insert a new line of text at the 4 row
    new_line = "\\printanswers\n"
    file_contents.insert(4, new_line)

    # open a new file in write mode
    with open(filename + "_answers.tex", 'w', encoding="utf-8") as new_file:
        # write the modified contents to the new file
        new_file.writelines(file_contents)


def compile_pdflatex(filename, output_solution_switch):
    """Runs pdflatex compilation twice, because it's needed for certain values (page numbers etc. to work correctly.)"""

    for twice in range(2):
        if output_solution_switch:
            os.system("pdflatex " + filename + ".tex -output-directory=temp")
            os.system("pdflatex " + filename + "_answers.tex -output-directory=temp")
        else:
            os.system("pdflatex " + filename + ".tex -output-directory=temp")
