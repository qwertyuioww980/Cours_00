from rest_framework import viewsets,generics,permissions,status
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from .models import (UserProfile, Teacher, NetworkTeachers, Category,
                     Subcategory, Language, Course,Chapter,NetworkStudent,
                     Lesson,Assignment,Exam,Question,Option,Certificate,Review,ReviewLike)
from .serializers import (UserProfileSerializer, TeacherSerializer,NetworkTeachersSerializer,
                          CategoryListSerializer,CategoryDetailSerializer,SubcategoryListSerializer,SubcategoryDetailSerializer,
                          LanguageSerializer,
                          CourseListSerializer,CourseDetailSerializer,ChapterSerializer,
                          NetworkStudentSerializer,LessonSerializer,LessonDetailSerializer,AssignmentSerializer,
                          ExamListSerializer,ExamDetailSerializer,QuestionSerializer,OptionSerializer,
                          CertificateSerializer,ReviewSerializer,ReviewLikeSerializer,CourseCreateSerializer,UserRegisterSerializer,LoginSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CourseFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from .pagination import CoursePagination
from .permission import TeacherPermission, StudentPermission
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken




class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'detail': 'Refresh токен не предоставлен.'}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Вы успешно вышли.'}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({'detail': 'Недействительный токен.'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


    def get_queryset(self):
        return UserProfile.objects.filter(id = self.request.user.id)



class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class NetworkTeachersViewSet(viewsets.ModelViewSet):
    queryset = NetworkTeachers.objects.all()
    serializer_class = NetworkTeachersSerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class SubcategoryListAPIView(generics.ListAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategoryListSerializer


class SubcategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategoryDetailSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['course_name']
    ordering_fields = ['price','created_at']
    pagination_class = CoursePagination
    permission_classes = [permissions.IsAuthenticated]


class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer


class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = [TeacherPermission]


class CourseEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = [TeacherPermission]

    def get_queryset(self):
        return Course.objects.filter(created_by = self.request.user)


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


class NetworkStudentViewSet(viewsets.ModelViewSet):
    queryset = NetworkStudent.objects.all()
    serializer_class = NetworkStudentSerializer


class LessonAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetailAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonDetailSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class ExamListAPIView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamListSerializer


class ExamDetailAPIView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamDetailSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class CertificateAPIView(generics.ListAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [StudentPermission]

    def get_queryset(self):
        return Certificate.objects.filter(student=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [StudentPermission]


class ReviewLikeViewSet(viewsets.ModelViewSet):
    queryset = ReviewLike.objects.all()
    serializer_class = ReviewLikeSerializer
    permission_classes = [StudentPermission]