import pygame
import sys
import time
import random
import requests
from io import BytesIO

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Python Quiz")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 223, 0)
DARK_YELLOW = (204, 173, 0)
DARK_GRAY = (80, 80, 80)
LIGHT_GRAY = (200, 200, 200)
GREEN = (85, 170, 85)
RED = (255, 85, 85)
LIGHT_BLUE = (51, 102, 204)
DARK_BLUE = (0, 51, 153)

font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 48)

quiz_duration = 300  #5 minutes
start_time = None

# Intro image
url = "https://thumbs.dreamstime.com/b/male-hand-holding-megaphone-quiz-time-speech-bubble-loudspeaker-banner-business-marketing-advertising-vector-125104939.jpg"
response = requests.get(url)
image_bytes = BytesIO(response.content)
intro_image = pygame.image.load(image_bytes)
intro_image = pygame.transform.scale(intro_image, (400, 400))

quiz_data = [
    {"question": "What is the first step to start coding in Python?",
     "choices": ["Installing an IDE", "Downloading necessary packages", "Install Python", "All of the above"],
     "answer": "All of the above"},
     
    {"question": "Which symbol is used to create a comment in Python?",
     "choices": ["#", "//", "/* */", "--"],
     "answer": "#"},

    {"question": "Which one correctly prints 'Hello World' in Python?",
     "choices": ["print('Hello World')", "Print('Hello World')", "print(hello world)", "print(Hello World)"],
     "answer": "print('Hello World')"},

    {"question": "Which operator is used to compare two values for equality in Python?",
     "choices": ["=", "==", "===", "!="],
     "answer": "=="},

    {"question": "What data type is the number 9 in Python?",
     "choices": ['string', 'int', 'float', 'list'],
     "answer": "int"},

    {"question": "Python enables reading data from the file and writing data into a file",
     "choices": ['True', 'False'],
     "answer": "True"},

    {"question": "Which package manager is commonly used with Python?",
     "choices": ["conda", "npm", "pip", "brew"],
     "answer": "pip"},

    {"question": "What does the .py file extension represent in programming?",
     "choices": ["Python file extension", "A configuration file for Python settings", "A module containing Python code", "All of the above"],
     "answer": "Python file extension"},

    {"question": "What file extension is used for a Jupyter Notebook?",
     "choices": [".ipynb", ".ahk", ".py", ".rmd"],
     "answer": ".ipynb"},

    {"question": "Which of the following is NOT true about Python?",
     "choices": ["Python is case-sensitive", "Integers are whole numbers", "'import' is a function", "pandas is used for data manipulation"],
     "answer": "'import' is a function"},

    {"question": "Which command checks the version of Python installed on your system?",
     "choices": ["python -version", "python --version", "import sys; sys.get_python_version()", "print(python.version)"],
     "answer": "python --version"},

    {"question": "Which of the following is a common Python library for data analysis?",
     "choices": ["XlsxWriter", "matplotlib", "pandas", "seaborn"],
     "answer": "pandas"},

    {"question": "Which function would you use to display something on the screen in Python?",
     "choices": ["display()", "print()", "show()", "output()"],
     "answer": "print()"},

    {"question": "What is the purpose of indentation in Python?",
     "choices": ["To make the code look nicer", "To define the logical structure", "To separate lines", "It has no purpose"],
     "answer": "To define the logical structure"},

    {"question": "What does 'float' represent in Python?",
     "choices": ["A type of variable that stores text", "A whole number", "A decimal number", "A function"],
     "answer": "A decimal number"},
]

# Shuffle
def shuffle_quiz_data():
    random.shuffle(quiz_data)
    for question in quiz_data:
        random.shuffle(question["choices"])

# Variables
current_question = 0
score = 0
user_answers = [None] * len(quiz_data)
finalized_answers = [False] * len(quiz_data)
show_feedback = False
quiz_started = False
quiz_ended = False
passing_score = 0.8

next_button_rect = None
previous_button_rect = None
start_button_rect = pygame.Rect(screen_width // 2 - 50, 500, 100, 50)
option_rects = []
close_button_rect = None

# Functions
def draw_text(text, font, color, surface, x, y, center=False, max_width=None):
    words = text.split(' ')
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        word_width, _ = font.size(word + ' ')
        if max_width is not None and current_width + word_width > max_width:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width
        else:
            current_line.append(word)
            current_width += word_width
    lines.append(' '.join(current_line))

    y_offset = y
    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(center=(x, y_offset)) if center else text_surface.get_rect(topleft=(x, y_offset))
        surface.blit(text_surface, text_rect)
        y_offset += font.get_height()

def display_intro():
    screen.fill(YELLOW)
    screen.blit(intro_image, (screen_width // 2 - 200, 50))
    pygame.draw.rect(screen, LIGHT_BLUE, start_button_rect)
    pygame.draw.rect(screen, DARK_BLUE, start_button_rect, 2)
    draw_text("Start", font, WHITE, screen, start_button_rect.centerx, start_button_rect.centery, center=True)

feedback_font = pygame.font.Font(None, 40)

def display_question():
    global next_button_rect, previous_button_rect, option_rects
    screen.fill(YELLOW)
    question_data = quiz_data[current_question]

    elapsed_time = int(time.time() - start_time)
    remaining_time = max(quiz_duration - elapsed_time, 0)
    minutes, seconds = divmod(remaining_time, 60)
    timer_text = f"Time Left: {minutes:02}:{seconds:02}"
    draw_text(timer_text, font, RED, screen, screen_width - 180, 20)

    progress_text = f"Question {current_question + 1} of {len(quiz_data)}"
    draw_text(progress_text, small_font, DARK_YELLOW, screen, screen_width - 180, 60)

    draw_text(question_data["question"], large_font, BLACK, screen, 50, 120, max_width=700)

    option_rects = []
    for i, choice in enumerate(question_data["choices"]):
        color = LIGHT_BLUE if user_answers[current_question] != i else DARK_BLUE
        rect = pygame.Rect(50, 200 + i * 70, 700, 50)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, DARK_BLUE, rect, 2)
        option_text = f"{i + 1}. {choice}"
        draw_text(option_text, font, WHITE, screen, rect.x + 10, rect.y + 10)
        option_rects.append((rect, i))

    if show_feedback or finalized_answers[current_question]:
        correct_text = "Correct!" if user_answers[current_question] is not None and quiz_data[current_question]["choices"][user_answers[current_question]] == quiz_data[current_question]["answer"] else f"Incorrect! Correct answer: {quiz_data[current_question]['answer']}"
        feedback_color = GREEN if correct_text == "Correct!" else RED
        draw_text(correct_text, feedback_font, feedback_color, screen, screen_width // 2, 500, center=True, max_width=700)

    next_button_rect = pygame.Rect(screen_width // 2 + 60, 550, 100, 40)
    previous_button_rect = pygame.Rect(screen_width // 2 - 160, 550, 100, 40)
    
    pygame.draw.rect(screen, LIGHT_BLUE, next_button_rect)
    pygame.draw.rect(screen, DARK_BLUE, next_button_rect, 2)
    pygame.draw.rect(screen, LIGHT_BLUE, previous_button_rect)
    pygame.draw.rect(screen, DARK_BLUE, previous_button_rect, 2)
    
    draw_text("Next", font, WHITE, screen, next_button_rect.centerx, next_button_rect.centery, center=True)
    draw_text("Previous", font, WHITE, screen, previous_button_rect.centerx, previous_button_rect.centery, center=True)
    
    pygame.draw.rect(screen, LIGHT_BLUE, next_button_rect)
    pygame.draw.rect(screen, DARK_BLUE, next_button_rect, 2)
    pygame.draw.rect(screen, LIGHT_BLUE, previous_button_rect)
    pygame.draw.rect(screen, DARK_BLUE, previous_button_rect, 2)
    
    draw_text("Next", font, WHITE, screen, next_button_rect.centerx, next_button_rect.centery, center=True)
    draw_text("Previous", font, WHITE, screen, previous_button_rect.centerx, previous_button_rect.centery, center=True)

def check_answer(choice_idx):
    global show_feedback
    if not finalized_answers[current_question]:
        user_answers[current_question] = choice_idx
        show_feedback = True

def finalize_answer():
    if user_answers[current_question] is None:
        user_answers[current_question] = -1
    finalized_answers[current_question] = True

def next_question():
    global current_question, show_feedback, quiz_ended
    finalize_answer()
    if current_question < len(quiz_data) - 1:
        current_question += 1
        show_feedback = finalized_answers[current_question]
    else:
        quiz_ended = True
        end_quiz()

def previous_question():
    global current_question, show_feedback
    if current_question > 0:
        current_question -= 1
        show_feedback = finalized_answers[current_question]

def end_quiz():
    global close_button_rect
    screen.fill(YELLOW)
    
    answered_correctly = sum(
        1 for i, answer in enumerate(user_answers) 
        if answer != -1 and quiz_data[i]["choices"][answer] == quiz_data[i]["answer"]
    )
    score_percentage = int((answered_correctly / len(quiz_data)) * 100)
    passed = score_percentage >= int(passing_score * 100)

    result_text = f"Congratulations! You scored {score_percentage}%" if passed else f"Quiz Failed! You scored {score_percentage}%"
    result_color = GREEN if passed else RED
    draw_text(result_text, large_font, result_color, screen, screen_width // 2, 50, center=True, max_width=700)

    if passed:
        image_url = "https://www.shutterstock.com/image-photo/beige-cat-holds-gold-cup-600nw-2116209404.jpg"
    else:
        image_url = "https://img.tripi.vn/cdn-cgi/image/width=700,height=700/https://gcs.tripi.vn/public-tripi/tripi-feed/img/474174ewO/anh-meme-meo-khoc-cuc-cute_042216244.jpg"

    response = requests.get(image_url)
    image_bytes = BytesIO(response.content)
    result_image = pygame.image.load(image_bytes)
    result_image = pygame.transform.scale(result_image, (400, 350))
    screen.blit(result_image, (screen_width // 2 - 200, 100))

    close_button_rect = pygame.Rect(screen_width // 2 - 50, screen_height - 100, 100, 50)
    pygame.draw.rect(screen, LIGHT_BLUE, close_button_rect)
    pygame.draw.rect(screen, DARK_BLUE, close_button_rect, 2)
    draw_text("Close", font, WHITE, screen, close_button_rect.centerx, close_button_rect.centery, center=True)

    pygame.display.flip()

running = True
shuffle_quiz_data()
while running:
    if not quiz_started:
        display_intro()
    elif not quiz_ended:
        elapsed_time = int(time.time() - start_time)
        if elapsed_time >= quiz_duration:
            quiz_ended = True
            end_quiz()
        else:
            display_question()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if not quiz_started and start_button_rect.collidepoint(mouse_pos):
                quiz_started = True
                start_time = time.time()
            if quiz_started:
                for rect, idx in option_rects:
                    if rect.collidepoint(mouse_pos):
                        check_answer(idx)
                if next_button_rect and next_button_rect.collidepoint(mouse_pos):
                    next_question()
                if previous_button_rect and previous_button_rect.collidepoint(mouse_pos):
                    previous_question()
            if close_button_rect and close_button_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

    pygame.display.flip()
