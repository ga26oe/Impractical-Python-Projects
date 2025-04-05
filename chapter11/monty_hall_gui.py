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
        
        # radio buttons and text widgets
        self.door_choice = tk.StringVar() # use variables to track tkinter widget event
        self.door_choice.set(None)
        
        #button widget for the three doors
        a = tk.Radiobutton(self.parent, text='A', variable=self.door_choice, value='a', command=self.win_reveal)
        b = tk.Radiobutton(self.parent, text='B', variable=self.door_choice, value='b', command=self.win_reveal)
        c = tk.Radiobutton(self.parent, text='C', variable=self.door_choice, value='c', command=self.win_reveal)

        # create widgets for changing door choice
        self.change_door = tk.StringVar() # string variable that will hold either 'y' or 'n' 
        self.change_door.set(None)
        
        instr_lbl = tk.Label(self.parent, text='Change doors?')
        instr_lbl.grid(row=2, column=3, columnspan=1, sticky='E')

        self.yes = tk.Radiobutton(self.parent, state='disabled', text='Y', variable=self.change_door, value='y', command=self.show_final)
        self.no = tk.Radiobutton(self.parent, state='disabled', text='N', variable=self.change_door, value='n', command=self.show_final)

        
        # create text widgets for win statistics
        defaultbg = self.parent.cget('bg') # cget() gets bacground color of parent and returns current value for a tkinter option as a string
        self.unchanged_wins_txt = tk.Text(self.parent, width=20, height=1, wrap=tk.WORD, bg=defaultbg, fg='black', borderwidth=0)
        self.changed_wins_txt = tk.Text(self.parent, width=20, height=1, wrap=tk.WORD, bg=defaultbg, fg='black', borderwidth=0)

        #place the widgets in the frame
        a.grid(row=1, column=4, sticky='W', padx=20) #'W' means left
        b.grid(row=1, column=4, sticky='N', padx=20) #'N' means center
        c.grid(row=1, column=4, sticky='E', padx=20) #'E' means right
        self.yes.grid(row=2, column=4, sticky='W', padx=20)
        self.no.grid(row=2, column=4, sticky='N', padx=20)
        self.unchanged_wins_txt.grid(row=1, column=5, columnspan=5)
        self.changed_wins_txt.grid(row=2, column=5, columnspan=5)

    def update_image(self):
        """Update current doors image. Needed to open and close doors throughout game.
        No need to pass file name with OOP. all methods for object have direct access to
        attributes that begin with self"""
        img = tk.PhotoImage(file=self.img_file) # filename will be updated in other methods
        self.photo_lbl.configure(image=img)
        self.photo_lbl.image = img

    def win_reveal(self):
        """Randomly pick winner and reveal unchosen door with goat."""
        door_list = list(self.doors) # make a list of doors from class attribute doors, which is tuple. using list so we can change it
        self.choice = self.door_choice.get() # this value was determined when the user clicked their first door choice
        self.winner = random.choice(door_list)

        door_list.remove(self.winner)

        #see wheter players choice is still in door list; if it is remove it so it can't be revealed
        if self.choice in door_list:
            door_list.remove(self.choice)
            self.reveal = random.choice(door_list)
        else: # the player picked the winning door, so reveal any of the two doors randomy
            self.reveal = random.choice(door_list)
        
        self.img_file = ('reveal_{}.png'.format(self.reveal))
        self.update_image() # call the method that updates the doors

        # turn on and clear yes/no buttons
        self.yes.config(state='normal')
        self.no.config(state='normal')
        self.change_door.set(None)
        
        # close doors 2 seconds after opening
        self.img_file = 'all_closed.png'
        self.parent.after(2000, self.update_image)
    
    def show_final(self):
        """Takes the player's final door choice and reveal whats behind it. 
        Also keep track of the number of wins for switching doors or staying put"""
        door_list = list(self.doors) # make a new copy of door list

        switch_doors = self.change_door.get() # get the change_door variable and assign it to attribute 'switch_doors'

        if switch_doors == 'y': # if player wants to remove their first choice
            # remove both the door they picked and the door that was revealed, and assign the last door in the list to the user's door
            door_list.remove(self.choice)
            door_list.remove(self.reveal)
            new_pick = door_list[0]
            if new_pick == self.winner:
                self.img_file = 'money_{}.png'.format(new_pick)
                self.pick_change_wins += 1
            else:
                self.img_file = 'goat_{}.png'.format(new_pick)
                self.first_choice_wins +=1
        elif switch_doors == 'n':
            if self.choice == self.winner:
                self.img_file = 'money_{}.png'.format(self.choice)
                self.first_choice_wins += 1
            else:
                self.img_file = 'goat_{}.png'.format(self.choice)
                self.pick_change_wins += 1
        
        # update door image
        self.update_image()
        
        # complete the show_final() method by updating game window, disabling yes/no buttons, and closing all doors
        self.unchanged_wins_txt.delete(1.0, 'end') # begin deleting text and index of 1, 'end' ensures all text after the starting index is deleted
        self.unchanged_wins_txt.insert(1.0, 'Unchanged wins = {:d}'.format(self.first_choice_wins))

        self.changed_wins_txt.delete(1.0, 'end')
        self.changed_wins_txt.insert(1.0, 'Changed wins = {:d}'.format(self.pick_change_wins))

        # turn off yes/no buttons and clear door choice buttons
        self.yes.config(state='disabled')
        self.no.config(state='disabled')
        self.door_choice.set(None)

        # close doors 2 seconds after opening
        self.img_file = 'all_closed.png'
        self.parent.after(2000, self.update_image)

# set up root window and run event loop
root = tk.Tk()
root.title("Monty Hall Problem") 
root.geometry('1280x820') # pics are 1280 x 720
game = Game(root)
root.mainloop()
        
        
        

        
        











        

        

        
        
        

        

        