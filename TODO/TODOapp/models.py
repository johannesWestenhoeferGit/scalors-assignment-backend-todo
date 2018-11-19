from django.db import models

class Board( models.Model ):
    # Model for boards
    name = models.CharField( max_length = 25 )
    def __str__( self ):
        return self.name

class Reminder( models.Model ):
    # Model for reminders
    email = models.EmailField()
    text = models.TextField()
    delay = models.DateTimeField()
    def __str__( self ):
        return self.text

class Todo( models.Model ):
    # Model for TODOs
    board = models.ForeignKey( Board, blank = True, null = True, on_delete = models.CASCADE )
    title = models.CharField( max_length = 25 )
    done = models.BooleanField()
    created = models.DateTimeField( 'date created' )
    updated = models.DateTimeField( 'date updated' )
    def __str__( self ):
        return self.title
    
    def __unicode__( self ):
        return '%s' % ( self.title )
