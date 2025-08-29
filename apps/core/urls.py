from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.core.views.application import ApplicationViewSet
from apps.core.views.auth import SignupView, LoginView
from apps.core.views.home import HomeView
from apps.core.views.recruitment import RecruitmentListView, RecruitmentDetailView
from apps.core.views.user import UserRecruitmentListView

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet)

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('auth/signup', SignupView.as_view(), name='signup'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('recruitments', RecruitmentListView.as_view(), name='recruitment'),
    path('recruitments/<int:pk>', RecruitmentDetailView.as_view(), name='recruitment_detail'),
    path("users/<int:pk>/recruitments", UserRecruitmentListView.as_view(), name="user_recruitment_list"),
    path('', include(router.urls)),
]
