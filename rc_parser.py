import re

raw_data = list()
with open('raw.txt', encoding='utf-8') as rawData:
    raw_data = rawData.read()
    rawData.close()

question_extractor = re.compile(r'^\d+\. (?:(?!\d+\. ).*(?:\n|$))*')
questions = re.findall(r'^\d+\. (?:(?!\d+\. ).*(?:\n|$))*', raw_data, flags=re.MULTILINE)

final_string = "\t\"NAME\":\n\t[\n"

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
            solution = str(i)
        answers.append(parsed_answer)

    final_string += "\t\t{\n\t\t\t\"Question\": \"" + question + "\",\n"
    final_string += "\t\t\t\"Answers\": [\n"

    for ans_idx, answer in enumerate(answers):
        final_string += "\t\t\t\t\"" + answer.replace("\n", "") + "\""
        if ans_idx < (len(answers) - 1):
            final_string += ","
        final_string += "\n"

    final_string += "\t\t\t],\n"
    final_string += "\t\t\t\"Solution\": " + solution + "\n"
    
    final_string += "\t\t}"

    if idx < (len(questions) - 1):
        final_string += ","
    final_string += "\n"


final_string += "\t]"

print(final_string)

with open("processed.json", "w+", encoding="UTF-8") as file:
    file.write(final_string)
    file.close()