import os
import random
from collections import defaultdict

class Question:
    def __init__(self, topic, text):
        self.topic = topic
        self.text = text

    def __str__(self):
        return f"{self.text}"

class Topic:
    def __init__(self, name):
        self.name = name
        self.questions = []

    def add_question(self, question):
        self.questions.append(question)

    def get_random_questions(self, count):
        if len(self.questions) < count:
            return random.sample(self.questions * (count // len(self.questions) + 1), count)
        return random.sample(self.questions, count)

    def __str__(self):
        return f"Topic: {self.name}"

class Student:
    def __init__(self, name):
        self.name = name
        self.questions = defaultdict(list)

    def add_question(self, topic, question):
        self.questions[topic].append(question)

    def __str__(self):
        questions_str = []
        for topic, questions in self.questions.items():
            questions_str.append(f"({topic}: {', '.join(map(str, questions))})")
        return f"{self.name} [{'; '.join(questions_str)}]"

def read_students(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        students = [Student(line.strip()) for line in file]
    return students

def read_topics(file_path):
    topics = {}
    current_topic = None
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith("Тема:"):
                topic_name = line.split(":", 1)[1].strip()
                current_topic = Topic(topic_name)
                topics[topic_name] = current_topic
            elif current_topic and line:
                current_topic.add_question(Question(current_topic.name, line))
    return topics

def generate_tickets(students, topics, question_distribution):
    topic_pool = {topic: list(topic.questions) for topic in topics.values()}
    
    for student in students:
        for topic_name, count in question_distribution.items():
            topic = topics[topic_name]
            questions = topic.get_random_questions(count)
            for question in questions:
                student.add_question(topic_name, question)
    return students

def write_tickets(students, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for student in students:
            file.write(str(student) + "\n\n")

def main():
    student_file = input("Введите путь к файлу со списком студентов: ").strip()
    topics_file = input("Введите путь к файлу с темами и вопросами: ").strip()
    output_file = input("Введите путь для сохранения билетов: ").strip()
    
    question_distribution = {}
    while True:
        topic = input("Введите тему (или 'end' для завершения): ").strip()
        if topic.lower() == 'end':
            break
        count = int(input(f"Сколько вопросов из темы '{topic}' должно быть в билете: "))
        question_distribution[topic] = count
    
    students = read_students(student_file)
    topics = read_topics(topics_file)
    
    students_with_tickets = generate_tickets(students, topics, question_distribution)
    
    write_tickets(students_with_tickets, output_file)
    print(f"Билеты сохранены в файл {output_file}")

if __name__ == "__main__":
    main()