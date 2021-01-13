import os
from xml.dom.minidom import getDOMImplementation

import docx

from question import Question

DOCX_DIR = "docx/"
XML_DIR = "xml/"
MULTIPLE_CHOICE = ("A.", "B.", "C.", "D.", "E.")
TRUE_FALSE = ("1.", "2.")
ANSWER_MARKER = " _ANSWER_"

for docx_file in os.listdir(DOCX_DIR):
    content = []
    question_list = []
    q_index = 1
    if docx_file != ".gitignore":
        file_path = DOCX_DIR + docx_file
        name_arr = docx_file.split(" ")
        prefix = f"{name_arr[0].upper()}_{name_arr[1]}_Q_"
        for index, p in enumerate(docx.Document(file_path).paragraphs):
            if index == 0:
                pass
            else:
                if p.text != "":
                    if not (p.text.startswith(MULTIPLE_CHOICE) or p.text.startswith(TRUE_FALSE)):
                        q_name = f"{prefix}{q_index}"
                        content.append(q_name)
                        content.append(p.text)
                        q_index += 1
                    else:
                        opts = p.text
                        for run in p.runs:
                            if run.bold:
                                opts += ANSWER_MARKER
                        content.append(opts)

        for i, e in enumerate(content):
            if not (e.startswith(MULTIPLE_CHOICE) or e.startswith(TRUE_FALSE) or e.startswith(
                    f"{name_arr[0].upper()}_{name_arr[1]}_Q_")):
                question_name = content[i - 1]
                question_text = e
                question_opts = {}
                question_type = ""
                if content[i + 1].startswith(MULTIPLE_CHOICE):
                    question_type = "multichoice"
                    question_opts["A"] = content[i + 1][3:]
                    question_opts["B"] = content[i + 2][3:]
                    question_opts["C"] = content[i + 3][3:]
                    question_opts["D"] = content[i + 4][3:]
                    question_opts["E"] = content[i + 5][3:]
                elif content[i + 1].startswith(TRUE_FALSE):
                    question_type = "truefalse"
                    question_opts["A"] = content[i + 1][3:]
                    question_opts["B"] = content[i + 2][3:]
                question = Question(question_name, question_text, question_type, question_opts)
                question_list.append(question)

        impl = getDOMImplementation()
        dom = impl.createDocument(None, "quiz", None)
        quiz_elem = dom.documentElement

        cat_question = dom.createElement("question")
        cat_question.setAttribute("type", "category")
        category = dom.createElement("category")
        text = dom.createElement("text")
        text.appendChild(dom.createTextNode(f"$course$/top/{name_arr[0]} {name_arr[1]}"))
        category.appendChild(text)
        cat_question.appendChild(category)
        quiz_elem.appendChild(cat_question)

        for question in question_list:
            question_elem = question.to_xml(dom)
            quiz_elem.appendChild(question_elem)

        with open(f"{XML_DIR}/{docx_file[0:23]}.xml", "w") as f:
            f.write(quiz_elem.toprettyxml())
