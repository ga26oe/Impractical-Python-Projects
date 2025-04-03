import random
import tkinter as tk

class Game(tk.Frame):
    """GUI application for Monty Hall Problem game."""

    doors = ('a', 'b', 'c') # tuple so it is immutable -- don't want it to be changed
    # later, we will make lists from this tuple so we can manipulate the doors
    # doors is a class attribute, because it is outside the methods
    # similar to how variables outside of function in procedural programs become global variables
    
    def __init__(self, parent): # initializer for the game objext, parent will be the root window
        """Initialize the frame."""
        super(Game, self).__init__(parent) # pass Game to super(), which means we want to invode a method of the superclass of Game, which is Frame
        self.parent = parent
        self.img_file = 'all_closed.png' # current image of doors
        self.choice = '' # players door choice 
        self.winner = '' # winning door
        self.reveal = '' # revealed goat door
        self.first_choice_wins = 0 # counter for stats
        self.pick_change_wins = 0 # counter for stats
        self.create_widgets() # method to create the label, button, text widgets to run the game
    
    def create_widgets(self):
        """Create label, button, and text widgets for game."""
        # create label to hold image of doors
        img = tk.PhotoImage(file='all_closed.png') # don't need to use "self", since it is only used locally within the method
        self.photo_lbl = tk.Label(self.parent, image=img, text = '', borderwidth=0)
        self.photo_lbl.grid(row=0, column=0, columnspan=10, sticky='W') # place the label in the parent window using grid() and let is span 10 columns and left-justify using W
        self.photo_lbl.image = img # finish photo label by creating reference to image obect -- fix tkinter problem with python garbage-collector
        
        # create the instruction label -- list of tuples, each containing options for making a Label object
        instr_input = [
            ('Behind one door is Cash!', 1, 0, 5, 'W'),
            ('Behind the others: Goats!', 2, 0, 5, 'W'),
            ('Pick a door:', 1, 3, 1, 'E')
        ]
        for text, row, column, columnspan, sticky in instr_input:
            instr_lbl = tk.Label(self.parent, text=text)
            instr_lbl.grid(row=row, column=column, columnspan=columnspan, sticky=sticky, ipadx=30)

        
        
        

        

        