import json
from App.models import Topic, Exam, Question, Course, Answer
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
            iterable = data[d]
            exam_name = iterable[0]['topicname']
            exam = Topic.objects.create(course=course, name=exam_name)
            for i in iterable:
                question = Question.objects.create(text=i['question'], exam=exam)
                for x in range(6):
                    try:                            
                        answer = i[f"Answer{x+1}"]
                        Answer.objects.create(question=question, text=answer, is_correct=self.is_correct(i, x))
                    except KeyError:
                        continue
        print(f"added {Topic.objects.all().count()} topics")
        print(f"added {Question.objects.filter(exam__exam_type=Exam.ExamTypeChoices.TOPIC).count()} questions")
                    
    def is_correct(self, obj, x):
        index = {'a.' : 1, "b." : 2, "c." : 3, "d." : 4, "e." : 5, "f." : 6, 'a' : 1, "b" : 2, "c" : 3, "d" : 4, "e" : 5, "f" : 6}
        correct_answer : str = obj['correctanswer']
        return index[correct_answer.split()[-1].lower()] == (x+1)

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
