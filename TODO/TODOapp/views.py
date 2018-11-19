from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status, permissions
from datetime import datetime, timedelta
from .models import Board, Todo, Reminder
from .serializers import BoardSerializer, TodoSerializer, ReminderSerializer
from .tasks import send_reminder
import io

class BoardViewSet( viewsets.ModelViewSet ):
    queryset = Board.objects.all().order_by( 'name' )
    serializer_class = BoardSerializer

class TodoViewSet( viewsets.ModelViewSet ):
    queryset = Todo.objects.all().order_by( 'created' )
    serializer_class = TodoSerializer

class TodoList( APIView ):
    # request handling on /todos/
    def get( self, request ):
        # return all TODOs on get request
        todos = Todo.objects.all() # get a queryset
        serializer = TodoSerializer( todos, many = True ) # serialize it
        return Response( serializer.data )
    def post( self, request, format = None ):
        # save a new todo on post request
        serializer = TodoSerializer( data = request.data ) # serialize a dataset to save it
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status = status.HTTP_201_CREATED )
        else:
            return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )

class TodoDetails( APIView ):
    # request handling on /todos/pk/

    def get_object( self, pk ):
        # gets the corresponding todo
        try:
            return Todo.objects.get( pk = pk )
        except Todo.DoesNotExist:
            raise Http404
    
    def get( self, request, pk, format = None ):
        #return the specific todo on get request
        todo = self.get_object( pk )
        serializer = TodoSerializer( todo )
        return Response( serializer.data )
    
    def append_data( self, todo, data ):
        # grab rest of data, modify request data, return full data
        serializer = TodoSerializer( todo )

        # while updating name or status the serializer still needs all the data
        old_data = serializer.data
        created = old_data['created']
        board_pk = old_data['board']
        updated = timezone.now() # automatic handling of update time
        data['created'] = created
        data['updated'] = updated
        data['board'] = str(board_pk)
        return data

    def put( self, request, pk, format = None ):
        # updating a specific todo ( name or status )
        todo = self.get_object( pk )
        data = self.append_data( todo, request.data ) # update the data to a full dataset
        serializer = TodoSerializer( todo, data = data )
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data )
        else:
            return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )
    
    def delete( self, request, pk, format = None ):
        # delete specific todo
        todo = self.get_object( pk )
        todo.delete()
        return Response( status = status.HTTP_204_NO_CONTENT )

class BoardList( APIView ):
    def replace_todo( self, serializer ):
        # this function replaces list of TODOs with todo_count
        # deserialize, modifiy, serialize again

        # convert JSON into native python datatype
        json = JSONRenderer().render( serializer.data )
        stream = io.BytesIO( json )
        boards = JSONParser().parse( stream )
        # loop through the boards to replace list of TODOs and replace with todo_count
        for board in boards:
            todo_count = len( board['todos'] )
            board.pop( 'todos', None )
            board[ 'todo_count' ] = todo_count
        serializer_modified = BoardSerializer( data = boards, many = True )
        return serializer_modified
        
    def get( self, request ):
        # returns all boards on get request
        boards = Board.objects.all()
        serializer = BoardSerializer( boards, many = True )
        serializer_modified = self.replace_todo( serializer ) #replace todo's with todo_count in output of all boards
        if serializer_modified.is_valid():
            return Response( serializer_modified.data )
        else:
            return Response( serializer.data, status = status.HTTP_400_BAD_REQUEST )
    
    def post( self, request, format = None ):
        # saves a new board from a dataset
        serializer = BoardSerializer( data = request.data )
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status = status.HTTP_201_CREATED )
        else:
            return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )

class BoardDetail( APIView ):
    # request handling on /boards/pk/

    def get_object( self, pk ):
        # get the corresponding board
        try:
            return Board.objects.get( pk = pk )
        except Board.DoesNotExist:
            raise Http404

    def get( self, request, pk, format = None ):
        # returns the board on get request
        board = self.get_object( pk )
        serializer = BoardSerializer( board )
        return Response( serializer.data )

    def put( self, request, pk, format = None ):
        # modify board on put request
        board = self.get_object( pk )
        serializer = BoardSerializer( board, data = request.data )
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data )
        else:
            return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )
    
    def delete( self, request, pk, format = None ):
        # delete board on delete request
        board = self.get_object( pk )
        board.delete()
        return Response( status = status.HTTP_204_NO_CONTENT )

class BoardsNC( APIView ):
    # request handling on /boards/pk/nc/
    # this class returns boards with the TODOs filted by status
    def get_object( self, pk ):
        try:
            return Board.objects.get( pk = pk )
        except Board.DoesNotExist:
            raise Http404

    def filter( self, serializer ):
        # this function does the filtering
        # deserialize, filter, serialize

        # convert JSON to python native datatype
        json = JSONRenderer().render( serializer.data )
        stream = io.BytesIO( json )
        data = JSONParser().parse( stream )

        # access the TODOs sublist
        todos = data['todos']
        
        # lood through TODOs and remove those with status == done
        for todo in todos:
            if todo['done']:
                todos.remove(todo)

        # serialize and return filtered serializer
        serializer_filtered = BoardSerializer( data = data, many = False )
        if serializer_filtered.is_valid():
            return serializer_filtered
        else:
            return serializer

    def get( self, request, pk, format = None ):
        # return the filtered list of boards on get request
        board = self.get_object( pk )
        serializer = BoardSerializer( board )
        serializer_filtered = self.filter( serializer ) # filtering
        return Response( serializer_filtered.data )

class ReminderList( APIView ):
    # request handling on /reminders/
    def calc_eta( self, delay_date ):
        pass


    def get( self, request ):
        # returns a list of all reminder on get request
        reminders = Reminder.objects.all()
        serializer = ReminderSerializer( reminders, many = True )
        return Response( serializer.data )

    def post( self, request, format = None ):
        # saves a new reminder from dataset on post request
        serializer = ReminderSerializer( data = request.data )
        if serializer.is_valid():
            serializer.save()
            eta = serializer.data['delay'] # calculate value for eta in apply_async
            send_reminder.apply_async( (serializer.data['email'], serializer.data['text']), eta = eta )
            return Response( serializer.data, status = status.HTTP_201_CREATED )
        else:
            return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )

class ReminderDetails( APIView ):
    # request handling on /remainders/pk/
    def get_object( self, pk ):
        try:
            return Reminder.objects.get( pk = pk )
        except Reminder.DoesNotExist:
            raise Http404
    
    def get( self, request, pk, format = None ):
        # returns the corresponding reminder
        reminder = self.get_object( pk )
        serializer = ReminderSerializer( reminder )
        return Response( serializer.data )

    
    def delete( self, request, pk, format = None ):
        # deletes the corresponding reminder
        reminder = self.get_object( pk )
        reminder.delete()
        return Response( status = status.HTTP_204_NO_CONTENT )
