from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('profile', views.profile, name='iporofile'),
    path('family', views.family, name='citizen-family'),
    path('events', views.events, name='citizen-events'),
    path('event/<int:id>', views.event_single, name='event-single'),
    path('family/<int:id>', views.family_single, name='family-single'),
    path('family/add', views.family_member_add, name='family-member-add'),
    path('family/member/delete/<int:id>', views.family_member_delete, name='family-member-delete'),
    path('family/edit/<int:id>', views.family_member_edit, name='family-member-edit'),
    path('message/new', views.new_message, name='message-new'),
    path('message/all', views.all_messages, name='messages-all'),
    path('stories/all', views.historyView, name='stories-all'),
    path('voting/all', views.voting_all, name='voting-all'),
    path('voting/<int:id>', views.voting_single, name='voting-single'),
    path('voting/member', views.vote_increase, name='vote-increase'),
    path('kwimuka', views.kwimuka, name='kwimuka'),
    path('kwimuka/cancel/<int:id>', views.cancelKwimuka, name='kwimuka-cancel'),

]