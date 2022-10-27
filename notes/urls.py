from django.urls import path


from notes import views
urlpatterns=[
    path('note/',views.NotesApi.as_view(), name='note'),
    path('collaborate/',views.Collaborator.as_view(),name="collaborate"),
    path('label/',views.LabelView.as_view(),name="label"),
    path('lbl/',views.LabelNote.as_view(),name="lbl")

]