from rest_framework import serializers
from .models import Board, Todo, Reminder

class TodoSerializer( serializers.ModelSerializer ):
    # Serializer for TODOs
    class Meta:
        model = Todo
        fields = ( 'board', 'title', 'done', 'created', 'updated' )

class BoardSerializer( serializers.ModelSerializer ): 
    # Serializer for boards
    class Meta:
        model = Board
        fields = ( 'name', 'todos', 'todo_count') # the fields we want to be able to return on API calls
    
    todos = TodoSerializer( source = 'todo_set', many = True, required = False ) # needed so boards can return their TODOs for the API
    todo_count = serializers.IntegerField(min_value = 0, max_value = None, required = False) # needed so boards can return their todo_count for the API

class ReminderSerializer( serializers.ModelSerializer ):
    # Serializer for reminders
    class Meta:
        model = Reminder
        fields = ( 'email', 'text', 'delay' )

