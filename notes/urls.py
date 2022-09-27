from django.urls import path


from notes import views
urlpatterns=[
    path('note/',views.NotesApi.as_view(), name='note'),

]