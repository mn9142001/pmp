from rest_framework import  serializers
from App.models import Course, Lesson, Comment, Topic, Exam, Question, Answer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        password = serializers.CharField(
            write_only=True,
            required=True,
            style={'input_type': 'password', 'placeholder': 'Password'}
        )
	
        fields = ('id', 'email', 'password', 'username')
    
    def create(self, validated_data):
        user=User.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email'],
        password=validated_data['password'],       
        )
        return user


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'user', 'lesson', 'username']


class LessonSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    course=serializers.StringRelatedField()

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'video_file', 'pdf_file', 'course', 'comments']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        comments = Comment.objects.filter(lesson=instance)
        data['comments'] = CommentSerializer(comments, many=True).data
        return data
    

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer()
    lessons = LessonSerializer(source='lesson_set', many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'published_at', 'image', 'price', 'instructor', 'lessons']


class TopicSerializer(serializers.ModelSerializer):
    exam_type = serializers.HiddenField(default=Topic.ExamTypeChoices.TOPIC)
    class Meta:
        model = Topic
        fields = ['id', 'name', 'course', 'exam_type']


class ExamSerializer(serializers.ModelSerializer):
    exam_type = serializers.HiddenField(default=Topic.ExamTypeChoices.TOPIC)
    class Meta:
        model = Exam
        fields = ['id', 'name', 'course', 'exam_type']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(source='answer_set', many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'topic', 'exam', 'question_type', 'answers']