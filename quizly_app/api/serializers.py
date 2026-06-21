from rest_framework import serializers


from ..models import Quiz, Question, Option



class OptionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Option model.

    Exposes the option ID, the option text, and whether the option
    is the correct answer. Used inside question and quiz serializers.
    """

    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']

    

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Question model.

    Provides:
    - question_title: the question text
    - question_options: list of option texts
    - answer: the correct option text (if any)
    """

    question_title = serializers.CharField(source='text')
    question_options = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()


    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at'] 


    def get_question_options(self, obj):
        """
        Return a list of option texts for the question.
        """
                
        return [option.text for option in obj.options.all()]

    
    def get_answer(self, obj):
        """
        Return the correct option text, or None if no correct option exists.
        """
                
        correct_option = obj.options.filter(is_correct=True).first()
        return correct_option.text if correct_option else None
    


class QuestionListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing questions.

    Provides:
    - question_title: the question text
    - question_options: list of option texts
    - answer: the correct option text (if any)
    """
        
    question_title = serializers.CharField(source='text')
    question_options = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer']


    def get_question_options(self, obj):
        """
        Return a list of option texts for the question.
        """
                
        return [option.text for option in obj.options.all()]
    

    def get_answer(self, obj):
        """
        Return the correct option text, or None if no correct option exists.
        """

        correct_option = obj.options.filter(is_correct=True).first()
        return correct_option.text if correct_option else None
    


class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer for the Quiz model.

    Provides:
    - video_url: alias for the model field `url`
    - questions: nested list of serialized questions
    """

    video_url = serializers.CharField(source='url')
    questions = QuestionSerializer(many=True, read_only=True)


    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']



class QuizListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing quizzes.

    Provides:
    - video_url: alias for the model field `url`
    - questions: nested list of lightweight question serializers
    """
    
    video_url = serializers.CharField(source='url')
    questions = QuestionListSerializer(many=True, read_only=True)


    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description','created_at', 'updated_at', 'video_url', 'questions']
