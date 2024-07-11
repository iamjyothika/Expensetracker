from django.urls import path,include
from .views import ExpenseCreateView,ExpenseDetailView,CategoryCreateView,CategoryDetailView,UserLoginView,UserRegistrationView,CategoryList,ExpenseFilterView

urlpatterns=[
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('expense/',ExpenseCreateView.as_view()),
    path('expense/<int:id>/', ExpenseDetailView.as_view()),
    path('category/', CategoryCreateView.as_view()),
    path('category/<int:id>/',CategoryDetailView.as_view()) ,
    path("listcategory/",CategoryList.as_view()),
    path('expensesfilter/', ExpenseFilterView.as_view(), name='expense-filter'),



]