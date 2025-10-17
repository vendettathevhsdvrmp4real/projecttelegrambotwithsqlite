import json
import random

TOPICS = {
    'Проблем': 'Questionproblem.json'
}

def get_problem_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['Problemquestion']

problem_list = get_problem_data(TOPICS['Проблем'])

problem_answer_map = {q['question']: q['answer'] for q in problem_list}

def get_answer(user_question: str):
    return problem_answer_map.get(user_question)