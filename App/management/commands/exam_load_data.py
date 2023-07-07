import json
from App.models import Exam, Question, Course, Answer
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db.transaction import atomic


class Command(BaseCommand):
    help = "Customized load data for DB migration"
    accounts = []

    def iter_json(self, data : list):
        """ Iterates dumpdata dson file and yields a model name / field dict pairs.

        e.g.
            model = 'common.sitesettings'
            fields = {'name': 'ACME Products', 'timezone': 'Africa/Johannesburg'}
        """
        course = Course.objects.first()
        for d in data:
            exam_name = d['Exam Name']
                
            exam, is_created = Exam.objects.get_or_create(course=course, name=exam_name, exam_type=Exam.ExamTypeChoices.EXAM)
            question = Question.objects.create(text=d['Question'], exam=exam, 
                                question_type=self.question_type(d),                                                                            
                            )

            for x in range(6):
                try:                            
                    answer = d[f"Answer{x+1}"]
                    Answer.objects.create(question=question, 
                                          text=answer, is_correct=self.is_correct(d, x)
                                    )
                except KeyError:
                    continue
        print(f"added {Exam.objects.all().count()} exams")
        print(f"added {Question.objects.filter(exam__exam_type=Exam.ExamTypeChoices.EXAM).count()} questions")
        print("number of questions with img", Question.objects.filter(img__isnull=False).count())
    
    def question_type(self, question):
        if "&" in question['Correct-Answer'].lower().strip():
            return "MC"
        return "OC"
    
    def is_correct(self, obj, x):
        index = {1:['a.', 'a'], 2:["b.", "b"], 3 : ["c.", "c"], 4: ["d.", "d"], 5 : ["e.", "e"], 6 : ["f.", "f"]}
        
        #getting correct answer, something like: "Answer option b."
        _correct_answers : str = obj['Correct-Answer'].lower().strip()
        
        if "answer option" in _correct_answers:
            correct_answers = _correct_answers.split("answer option ")            
        else:
            correct_answers = _correct_answers.split("answer ")
        for o in correct_answers:
            if "&" in o:
                correct_answers = correct_answers + o.split("&")        
        return bool(set(index[(x + 1)]) & set(correct_answers))


    @atomic()
    def iter_data(self, file):
        """ Iterates dumpdata dson file and yields model instances.

        The downside to this approach is that one requires the code for the models,
        which is not neccessarily the case when migrating data/
        e.g.
            model_instance = <SiteSettings: ACNE Products ()>
        """
        with open(file, "r") as f:
            data_str = f.read()

        data = json.loads(data_str)

        self.iter_json(data)
        # print(payment_data)
        # for user in user_data:
        #     print("useR",self.set_account_data(user))

        # for item in serializers.deserialize("json", data_str):
        #     # item.save() would save it (unconfirmed)
        #     model_instance = item.object
        #     yield model_instance

    def add_arguments(self, parser):
        parser.add_argument(
            'file',
            type=str,
            help='Location of the manage.py loaddata backup file',
        )

        # parser.add_argument(
        #     'course_id',
        #     type=str,
        #     help='course id',
        # )


    def handle(self, **options):
        file = options['file']
        # self.course_id = options['course_id']
        if not Path(file).is_file():
            print(f"File '${file}' does not exist. EXIT.")
            return

        print(f"START - Customised loaddata")
        # for model, fields in self.iter_json(file):
        #     pass
        self.iter_data(file)
        print(f"COMPLETE.")