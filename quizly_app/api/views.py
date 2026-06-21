from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response


from ..models import Quiz, Question, Option

from .serializers import QuizSerializer, QuizListSerializer
from ..services.YouTubeTranscriptExtractor import YouTubeTranscriptExtractor
from ..services.gemini_quiz_generator import GeminiQuizGenerator



class QuizView(APIView):
    """
    Handles listing quizzes (GET) and generating a new quiz from a YouTube URL (POST).
    """

    permission_classes = [permissions.IsAuthenticated]


    def get(self, request):
        """
        Return all quizzes belonging to the authenticated user.
        """

        quizzes = Quiz.objects.filter(user=request.user)
        serializer = QuizListSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        """
        Create a new quiz from a YouTube video URL.
        """

        video_url = request.data.get('url')

        if not video_url or not ('youtube.com' in video_url or 'youtu.be' in video_url):
            return Response({'detail': 'Invalid URL or request data.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
           
            extractor = YouTubeTranscriptExtractor() 
            transcript = extractor.get_transcript(video_url)

            generator = GeminiQuizGenerator()
            quiz_data = generator.generate_quiz(transcript)

            quiz = Quiz.objects.create(user=request.user, title='Automatisch generiertes Quiz',
                                       description='Erstellt aus YouTube-Video', url=video_url)
            
            for q in quiz_data:
                question = Question.objects.create(quiz=quiz, text=q['question'])
                for opt in q['options']:
                    Option.objects.create(question=question, text=opt, is_correct=(opt == q['answer']))

            serializer = QuizSerializer(quiz)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


class QuizDetailView(APIView):
    """
    Handles retrieving, updating, and deleting a single quiz.
    Only the quiz owner is allowed to access or modify it.
    """

    permission_classes = [permissions.IsAuthenticated]


    def get_object(self, pk):
        """
        Return the quiz instance or None if it does not exist.
        """

        try:
            return Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return None
        

    def get(self, request, pk):
        """
        Retrieve a single quiz if the user owns it.
        """

        quiz = self.get_object(pk)

        if quiz is None:
            return Response({'detail': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

        if quiz.user != request.user:
            return Response({'detail': 'No authorization'}, status=status.HTTP_403_FORBIDDEN)

        serializer = QuizListSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def patch(self, request, pk):
        """
        Update quiz title and description. Only the owner may update the quiz.
        """

        quiz = self.get_object(pk)

        if quiz is None:
            return Response({'detail': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if quiz.user != request.user:
            return Response({'detail': 'No authorization'}, status=status.HTTP_403_FORBIDDEN)

        title = request.data.get('title')
        description = request.data.get('description')

        if not title or not description:
            return Response({'detail': 'Title and description must be provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = QuizListSerializer(quiz, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        """
        Delete a quiz if the user owns it.
        """

        quiz = self.get_object(pk)

        if quiz is None:
            return Response({'detail': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if quiz.user != request.user:
            return Response({'detail': 'No authorization'}, status=status.HTTP_403_FORBIDDEN)
        
        quiz.delete()
        return Response(status=status.HTTP_200_OK)
    

