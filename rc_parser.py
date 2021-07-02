import json
import re

raw_data = list()
with open('raw.txt', encoding='utf-8') as rawData:
    raw_data = rawData.read()
    rawData.close()

# question_extractor = re.compile(r'^\d+\. (?:(?!\d+\. ).*(?:\n|$))*')
questions = re.findall(r'^\d+\. (?:(?!\d+\. ).*(?:\n|$))*', raw_data, flags=re.MULTILINE)

preguntas_name = "NAME"
final_dict = {}
final_dict[preguntas_name] = []

for idx, item in enumerate(questions):
    question = re.findall(r'(^\d+\. )((?:(?!\w+\) ).*(?:\n|$))*)', item, flags=re.MULTILINE)
    question = question[0][1].replace("\n", " ").strip()

    raw_answers = re.findall(r'(^\w+\) )((?:(?!\w+\) ).*(?:\n|$))*)', item, flags=re.MULTILINE)
    answers = list()
    solution = ""
    for i, answer in enumerate(raw_answers):
        parsed_answer = answer[1]
        if re.match(r'(^\*)((.*\n|.*)*)', parsed_answer):
            parsed_answer = re.findall(r'(^\*)((.*\n|.*)*)', parsed_answer, flags=re.MULTILINE)[0][1]
            solution = i
        answers.append(parsed_answer)

    question_dict = {
        "Question": question,
        "Answers": list(map(lambda s: s.strip("\n"), answers)),
        "Solution": solution
    }
    final_dict[preguntas_name].append(question_dict)

# print(final_string)

print(json.dumps(final_dict, indent = 2, ensure_ascii=False)) # ensure_ascii no es necesario, pero da mas claridad en el archivo JSON: https://stackoverflow.com/questions/35582528/python-encoding-and-json-dumps

with open("processed.json", "w+", encoding="UTF-8") as file:
    file.write(json.dumps(final_dict, indent = 2, ensure_ascii=False))
    file.close()