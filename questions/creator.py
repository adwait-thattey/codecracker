from .models import Question, Category
from django.contrib.auth.models import User
import random

def make_questions(count):
    cat_set = Category.objects.all()
    user_set = User.objects.all()

    DIFFICULTY = [
        'Easy',
        'Medium',
        'Hard'
    ]

    for i in range(count):
        i = str(i)
        print(DIFFICULTY[random.randint(0,len(DIFFICULTY)-1)])
        q = Question.objects.create(
            author=user_set[random.randint(0,len(user_set)-1)],
            category=cat_set[random.randint(0,len(cat_set)-1)],
            title = "Test Question" + i,
            short_description = "Sample Short Description for question" + i,
            description = "Sample Full Description for question" + i,
            input_format= "Sample Inp Format for question" + i,
            constraints= "Sample Inp Format for question" + i,
            output_format= "Sample Inp Format for question" + i,
            sample_input= "Sample Inp Format for question" + i,
            sample_output= "Sample Inp Format for question" + i,
            time_limit= random.randint(2,5),
            unique_code= "samques" + i,
            difficulty=DIFFICULTY[random.randint(0,len(DIFFICULTY)-1)],
            view_count=random.randint(0,100),
            submission_count=random.randint(0,100)


        )
        print(q.difficulty)
def make_users(count):
    for i in range(count):
        User.objects.create_user(username="test_user_" + str(i), password="Hello World")
