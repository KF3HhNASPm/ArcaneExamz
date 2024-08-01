from arcane_examz_functions import *

# CONFIGURATION
version = "0.4"
# TEST PARAMETERS FOR GENERATOR
questions_open_new = 3
questions_open_old = 2

questions_mcq_new = 2
questions_mcq_old = 2

number_of_tests = 2
# FOR TEST NAME DO NOT USE ANY SPECIAL CHARACTERS
test_name = "example"

# PAPER SETTINGS - CHANGES VALUES IN LATEX DECLARATION (write_content_header)
paper_size = "a5"  # a4, a5, a6...
font_size = "11"
landscape = True  # True/False
language = "czech"  # czech/english/...
header_left = "textleft"
header_center = "textcenter "
header_right = "textright"

# SOURCE FILES = QUESTION BANKS (MULTIPLE FILES CAN BE ADDED WITH (,) DELIMITER)
file_question_bank_new = ["questions.csv"]
file_question_bank_old = ["questions_old.csv"]

# output_solution_switch - IF TRUE, CREATES SOLUTION FILE, COMPILES AND MERGES INTO test_name_answers.PDF
output_solution_switch = True  # True/False

# LOADS QUESTIONS FROM CSV FILES ROW BY ROW INTO LISTS BASED ON question_type PARAMETER AND SOURCE FILE
# OPEN QUESTIONS
bank_open_questions_new = load_csv_into_list(file_question_bank_new, "OPEN")
bank_open_questions_old = load_csv_into_list(file_question_bank_old, "OPEN")

# MULTICHOICE QUESTIONS
bank_mcq_questions_new = load_csv_into_list(file_question_bank_new, "MULTI")
bank_mcq_questions_old = load_csv_into_list(file_question_bank_old, "MULTI")

# CALCULATES NUMBER OF QUESTIONS FOR NEW/OLD CATEGORY ###### MAY NEEDS REWRITE - no ration, just check max value

questions_open_new, questions_open_old, questions_mcq_new, questions_mcq_old = check_overflow(questions_open_new,
                                                                                              questions_open_old,
                                                                                              questions_mcq_new,
                                                                                              questions_mcq_old,
                                                                                              bank_open_questions_new,
                                                                                              bank_open_questions_old,
                                                                                              bank_mcq_questions_new,
                                                                                              bank_mcq_questions_old)

# CREATES TEMP DIR FOR PDFLATEX OUTPUT = LESS MESS IN THE MAIN DIR
if not os.path.exists("/temp/"):
    create_temp()

# LISTS FOR SCRAPING NAMES OF CREATED FILES FOR FUTURE MERGING
pdf_filenames_list = []
pdf_filenames_solution_list = []

# LOOP FOR EACH TEST TO BE GENERATED
for i in range(number_of_tests):
    # GENERATES UNIQUE FILENAME FOR EACH TEST, ADDS THIS FILENAME TO pdf_names LIST, WHICH IS USED FOR MERGING
    # SAME APPLIES FOR pdf_names_answers WHICH IS A SOLUTION SHEET
    filename = "./temp/exam" + str(i)
    pdf_filenames_list.append(str(filename + ".pdf"))
    pdf_filenames_solution_list.append(str(filename + "_answers.pdf"))

    # GENERATES RANDOM ORDER OF NUMBERS IN RANGE EQUAL TO NUMBER OF REQUIRED QUESTIONS DEFINED IN number_of_questions
    random_order_open_questions_new = randomize_order(bank_open_questions_new, questions_open_new)
    random_order_open_questions_old = randomize_order(bank_open_questions_old, questions_open_old)
    random_order_mcq_questions_new = randomize_order(bank_mcq_questions_new, questions_mcq_new)
    random_order_mcq_questions_old = randomize_order(bank_mcq_questions_old, questions_mcq_old)

    # WRITES HEADER TO THE .TEX FILE
    write_content_header(filename, version, i, paper_size, font_size, landscape, language, header_left,
                         header_center, header_right)

    # IF BANK NOT EMPTY, GENERATE AND WRITE QUESTIONS
    if bank_open_questions_new:
        write_content_open_question(random_order_open_questions_new, bank_open_questions_new, filename)
    if bank_mcq_questions_new:
        write_content_mcq_question(random_order_mcq_questions_new, bank_mcq_questions_new, filename)
    if bank_open_questions_old:
        write_content_open_question(random_order_open_questions_old, bank_open_questions_old, filename)
    if bank_mcq_questions_old:
        write_content_mcq_question(random_order_mcq_questions_old, bank_mcq_questions_old, filename)

    # WRITES CLOSING CODE TO THE .TEX FILE
    write_content_close(filename)
    if output_solution_switch:
        output_answers(filename)

    # COMPILATION
    compile_pdflatex(filename, output_solution_switch)

# MERGING PDFs
merge_pdfs(test_name, pdf_filenames_list, pdf_filenames_solution_list, output_solution_switch)
