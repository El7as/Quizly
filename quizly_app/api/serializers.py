from rest_framework import serializers


from ..models import Quiz, Question, Option



class OptionSerializer(serializers.ModelSerializer):


    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']

    

class QuestionSerializer(serializers.ModelSerializer):
    question_title = serializers.CharField(source='text')
    question_options = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()


    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at'] 


    def get_question_options(self, obj):
        return [option.text for option in obj.options.all()]

    
    def get_answer(self, obj):
        correct_option = obj.options.filter(is_correct=True).first()
        return correct_option.text if correct_option else None
    


class QuestionListSerializer(serializers.ModelSerializer):
    question_title = serializers.CharField(source='text')
    question_options = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer']


    def get_question_options(self, obj):
        return [option.text for option in obj.options.all()]
    

    def get_answer(self, obj):
        correct_option = obj.options.filter(is_correct=True).first()
        return correct_option.text if correct_option else None
    


class QuizSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(source='url')
    questions = QuestionSerializer(many=True, read_only=True)


    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']



class QuizListSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(source='url')
    questions = QuestionListSerializer(many=True, read_only=True)


    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description','created_at', 'updated_at', 'video_url', 'questions']

