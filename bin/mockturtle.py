#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Interpreter for a subset of the turtle graphics language.

################ USAGE

Doing a 'mockturtle.py -h' will get you:

  usage: turtle graphics interpreter [-h] [-x WX] [-y WY]
                                     [-p TURTLE_PROGRAM] [-s {0..25}]
                                     [-d DELAY]

  optional arguments:
    -h, --help            show this help message and exit
    -x WX, --wx WX        width of window
    -y WY, --wy WY        height of window
    -p TURTLE_PROGRAM, --turtle_program TURTLE_PROGRAM
                          filename of turtle program to execute
    -s {0..25}, --speed {0..25}
                          speed of turtles
    -d DELAY, --delay DELAY
                          delay (ms) between drawing line segments

################ MODES OF RUNNING

Three modes of running are supported.

 - The principal way is by executing this script: this shows a gui.
   See EXAMPLE 1 and EXAMPLE 3, below.
 - The first text-based method is by running the TurtleShell after importing
   this file as a module.  See EXAMPLE 2 and EXAMPLE 4.
 - Alternatively, one can import the module and create Turtle objects,
   running their functions directly.  See EXAMPLE 5.

################ FORMS OF INPUT

If we run a turtle shell (whether within an associated TurtleApp, or
in text mode), then then commands of the turtle graphics language can
be typed into a command shell (EXAMPLES 1 and 2, below), or can be
loaded from a file whose name is passed as input (EXAMPLES 3 and 4).

Otherwise, commands are passed using functions within Turtle(),
as in EXAMPLE 5.

################ EXAMPLES

#####
##### EXAMPLE 1

This draws a line from the center to 100 units north, s l o w l y.

 % ./mockturtle.py -s 1 -d 100              
  t: turtle rob
  t: move rob 100
  t: bye
 % 

#####
##### EXAMPLE 2

Text-based use of the TurtleShell.

 % python3
 Python 3.6.7 (default, Oct 22 2018, 11:32:17) 
 [GCC 8.2.0] on linux
 Type "help", "copyright", "credits" or "license" for more information.
 >>> import mockturtle as mt
 >>> mt.TurtleShell().cmdloop()
  t: turtle bill
  t: move bill 90
     drew from (0.00, 0.00) to (0.00, 90.00)
  t: right bill 30
  t: move bill 20
     drew from (0.00, 90.00) to (10.00, 107.32)
  t: status
           bill:  (  10.00,  107.32) |  60.00° | DOWN | black
  t: bye
 >>> quit()
 %

#####
##### EXAMPLE 3

This draws a sample file quickly (not instantaneously).

 % ./mockturtle.py -s 20 -d 10 -p ../turtle_programs/squares.tt
  t: bye
 %

#####
##### EXAMPLE 4

Show the effects of a 'red square' program, text-based TurtleShell.

 % python3
 Python 3.6.7 (default, Oct 22 2018, 11:32:17) 
 [GCC 8.2.0] on linux
 Type "help", "copyright", "credits" or "license" for more information.
 >>> import mockturtle as mt
 >>> ts = mt.TurtleShell(turtle_program='../turtle_programs/redsquare.tt').cmdloop()
      drew from (0.00, 0.00) to (0.00, 50.00)
     drew from (0.00, 50.00) to (-50.00, 50.00)
     drew from (-50.00, 50.00) to (-50.00, 0.00)
     drew from (-50.00, 0.00) to (-0.00, 0.00)
  t: bye
 >>> quit()
 %

#####
##### EXAMPLE 5

Text-based turtle drawing without the interpreter.

 % python3
 Python 3.6.7 (default, Oct 22 2018, 11:32:17) 
 [GCC 8.2.0] on linux
 Type "help", "copyright", "credits" or "license" for more information.
 >>> import mockturtle as mt
 >>> bill = mt.Turtle()
 >>> bill.left(50)
 >>> bill
 mockturtle.Turtle object: (   0.00,    0.00) | 140.00° | DOWN | black
 >>> bill.move(100)
     drew from (0.00, 0.00) to (-76.60, 64.28)
 >>> quit()
 %

################ PROGRAM STRUCTURE

Using tkinter (as tk) for graphics, we open a root window, and for the
main application subclass tk.Frame (as TurtleApp).  This packs a
canvas, which can be dragged to show what stray turtles are up to.
The main application then starts a thread in which a sublcass of
cmd.Cmd (TurtleShell) is used for the interpreter.  The interpreter
then (optionally) reads the commands of any input file, and waits for
further commands at a prompt.

Both cmd.Cmd and tkinter run on a loop, and the interaction of these
has presented some complications.  (Especially in shutting down)  The
main tk loop runs in the main thread (as is strongly recommended).
The cmd.Cmd loop runs in a secondary thread.

Multiple turtles can be created, each an instance of a Turtle class.
The speed at which they all draw can be controlled by command-line
arguments; the idea and the form of the relevant mathematics has been
taken from the python standard library 'turtle' module.  Animation is
simulated by drawing lines in segments and delaying between each
segment.  The number of segments is controlled indirectly by the
'speed' command-line argument; the delay is controlled directly by
its command-line argument.

Turtles themselves do not do their actions concurrently.  And no
turtle  itself is drawn on the canvas (only the lines appear).

################ MAIN CLASSES AND FUNCTIONS

  class TurtleApp(tk.Frame)
    - Main tk object for controlling the interpreter and graphics

  class TurtleShell(cmd.Cmd)
    - Main object for controlling the interpreter and parsing
      commands.

  class Turtle:
    - An instance for each turtle created, storing its location,
      orientation, and so on.

  def command_line_args():
    - Get command-line arguments using argparse

################ SHUTTING DOWN

Behaviour when shutting the thing down has involved some compromise.
(Partly because of 'threading', partly because of issues with the
interaction of cmd.Cmd.cmdloop() and tk.mainloop(), I think.)  

If the prompt is waiting for a command, then just write 'bye'.
(Shutting the window, of CTRL-C, etc., will not work as they ought.)
If the application is running a program passed from file, then either
close the window or CTRL-C in the terminal should work.

################ SUBSET OF TURTLE LANGUAGE

We accept the following language:

  turtle name   - create a new turtle identified by the given name
  move name x   - moves the named turtle forward by x units
  left name x   - rotate the turtle anticlockwise by x degrees
  right name x  - rotate the turtle clockwise by x degrees
  pen name up   - lift the pen off the 'paper'
  pen name down - put the pen down so subsequent moves draw on screen
  colour name c - set the drawing colour of the turtle appropriately

In addition:

  bye           - closes the application
  status        - prints the current states of all the terminals

where:

  x, for 'move', must be castable to a float (so it can be negative
      or 0)
  x, for 'left' and 'right', must be castable to a float in [0,360)
  c - must be one of ['azure', 'beige', 'black', 'blue', 'brown',
                      'chartreuse', 'chocolate', 'coral', 'cyan',
                      'firebrick', 'gainsboro', 'gold', 'gray','green',
                      'indigo', 'lavender', 'lime', 'magenta',
                      'maroon', 'olive', 'orange', 'pink', 'plum',
                      'purple', 'red', 'salmon', 'tan', 'thistle',
                      'tomato', 'violet', 'white', 'yellow']

"""

import argparse
import cmd
from functools import partial
import math
import os.path
import signal
import sys
import threading
import time
import tkinter as tk

########################
########################

class TurtleApp(tk.Frame):
    """
    Main tk object for controlling the interpreter and graphics.

    Lines are drawn on a tk.Canvas which lives inside the TurtleApp.  

    Drawing lines is controlled by draw_line(...), which draws lines
    in segments using the tk.creat_line object.  Number of segments
    and speed are parameters; these control the apparent speed of
    the turtles.  The behaviour here is an altered version of that
    found in the python turtle module.

    Since turtles can wander outside the initial size of the canvas
    (as determined by command-line arguments, by default 600x600),
    we allow the canvas to be dragged within the frame.

    We spawn a thread for the turtle shell interpreter.  (tkinter's
    interaction with threading module is, according to the internet,
    poor.  This means the main thread must be for the tkinter
    mainloop().)
    """

    def __init__(self, parent:tk.Widget, args:argparse.Namespace):
        """Turtle app constructor."""
        tk.Frame.__init__(self, parent)
        self.pack(expand=True, fill='both')
        self.parent = parent

        # Make a canvas on which turtles will draw lines.
        self.canvas = tk.Canvas(self)
        self.canvas.pack(anchor='center', expand=True, fill='both')
        # Register handlers to let us drag the canvas.
        self.canvas.bind("<ButtonPress-1>", self.drag_canvas_prepare)
        self.canvas.bind("<B1-Motion>", self.drag_canvas)
        
        # Values which control the drawing of lines.
        self.speed = args.speed
        self.delay = args.delay / 1000

        # Start turtle interpreter thread
        # -- args.wx/2 and args.wy/2 give the coordinates of the centre of
        #    the root window, _before_ any resizing or scrolling has occurred
        # -- orientation of 270 degrees is 'north' for a tk.Canvas
        threading.Thread(target=self.run_turtle_shell,
                         args=(args.wx/2, args.wy/2, 270.0, args.turtle_program)
                        ).start()

    
    def run_turtle_shell(self, x0:float, y0:float, theta:float, turtle_program:str):
        """
        Start the turtle interpreter shell.

                      x0: x-coordinate turtles will start at
                      y0: y-coordinate turtles will start at
                   theta: initial orientation in ° of turtles
          turtle_program: filename of turtle language script to read
        """

        turtleshell = TurtleShell(self, x0, y0, theta, turtle_program)
        # store reference to the TurtleShell in the parent (for clean exits)
        self.parent.turtleshell = turtleshell
        turtleshell.cmdloop()
        # If we get here, the TurtleShell has died, so kill the tk objects too.
        self.parent.quit()
        self.parent.update()

    def drag_canvas_prepare(self, event:tk.Event):
        """Handle event marking beginning of canvas drag (left mouse-click)."""
        self.canvas.scan_mark(event.x, event.y)

    def drag_canvas(self, event:tk.Event):
        """Handle event for canvas drag (mouse move while left button down)."""
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def draw_line(self, xs:float, ys:float, xe:float, ye:float, colour:str):
        """
        Draw line (xs,ys)--(xe-ye) on the canvas.

        We draw the line in segments.  The number of segments is
        controlled by the speed setting, an integer in [0,25], and
        set by a modification of a similar formula from the python
        turtle module.  A pause after each segment results in a
        simulation of animation.
        """

        xdelta = xe - xs
        ydelta = ye - ys
        delta = (xdelta**2 + ydelta**2)**0.5
        
        # Calculate the number of segments.  If speed=0, the line is drawn
        # instantaneously: one segment.
        if self.speed == 0:
            n_segments = 1
        else:
            n_segments = 1+int(delta/(2*(1.1**self.speed)*self.speed))
        # Deltas for each segment.
        dx = xdelta / n_segments
        dy = ydelta / n_segments

        x1 = xs
        y1 = ys
        for _ in range(n_segments):
            # End-point of next segment.
            x2 = x1 + dx
            y2 = y1 + dy
            # dDraw the line and pack it up.
            self.canvas.create_line(x1, y1, x2, y2, fill=colour, width=1.6)
            self.canvas.pack()
            # Set the beginning of the next segment.
            x1 = x2
            y1 = y2
            # Unless we are drawing instantaneously, delay until next segment.
            if self.speed > 0:
                time.sleep(self.delay)

########################
########################

class TurtleShell(cmd.Cmd):
    """Shell object for controlling interpretation of the turtle commands."""
    
    def __init__(self, app:TurtleApp=None,
                       x0:float=0.0, y0:float=0.0, theta:float=90.0,
                       turtle_program:str=None):
        """
        Make a command interpreter for the turtle graphics language.
        The defaults are determined by desired behaviour in text mode (when
        the shell might be made by a simple 'TurtleShell()').

                     app: TurtleApp object containing the interpreter lives.
                      x0: x-coordinate turtles will start at
                      y0: y-coordinate turtles will start at
                   theta: initial orientation in ° of turtles
          turtle_program: filename of turtle language script to read
        """

        cmd.Cmd.__init__(self)

        # The following are used in making new turtles.
        self.app = app
        self.x0 = x0
        self.y0 = y0
        self.theta = theta

        # If the filename of a turtle program was given at the command-line,
        # then read the lines of the program into the interpreter's command
        # queue (self.cmdqueue), to be executed when the interpreter starts
        # its loop.
        if turtle_program:
            with open(turtle_program) as f:
                self.cmdqueue = f.readlines()
            # after reading the program, wait a bit before interpreting it
            time.sleep(0.25)
        
        self.prompt = ' t: '            # interpreter prompt

        self.turtles = dict()           # dictionary of turtles
        self.colours =['azure', 'beige', 'black', 'blue', 'brown', 'chartreuse',
                       'chocolate', 'coral', 'cyan', 'firebrick', 'gainsboro',
                       'gold', 'gray', 'green', 'indigo', 'lavender', 'lime',
                       'magenta', 'maroon', 'olive', 'orange', 'pink', 'plum',
                       'purple', 'red', 'salmon', 'tan', 'thistle', 'tomato',
                       'violet', 'white', 'yellow']
        self.pen_states = ['down', 'up']

    def __str__(self) -> str:
        """String representation of the interpreter.

        This shows the current state of all the turtles.  If there aren't
        any, we say that.  This is printed by the command 'status' fed into
        the interpreter.
        """

        if not self.turtles:
            return '    No turtles!'
        else:
            return '\n'.join(f'{k: >14}:  {v}' for k,v in self.turtles.items())

    ############ Functions for interpreter commands from turtle language
    ############ (see docs for cmd.Cmd for explanation).

    # We get the arguments to the command using self.parse_args(), then
    # call the relevant function on the Turtle() object.

    def do_turtle(self, args:str):
        'Make a new turtle (or reset an existing turtle), e.g.: turtle bill'
        turtle_args = self.parse_args('turtle', args)
        if turtle_args:
            self.turtles[turtle_args[0]] = Turtle(self.app, self.x0, self.y0,
                                                  self.theta)

    def do_colour(self, args:str):
        'Set the colour of a turtle, e.g.: colour bill red'
        turtle_args = self.parse_args('colour', args)
        if turtle_args:
            self.turtles[turtle_args[0]].colour = turtle_args[1]

    def do_move(self, args:str):
        'Move a turtle a number of units, e.g.: move bill 100'
        turtle_args = self.parse_args('move', args)
        if turtle_args:
            self.turtles[turtle_args[0]].move(turtle_args[1])

    def do_left(self, args:str):
        'Rotate a turtle some degrees anti-clockwise, e.g.: left bill 10'
        turtle_args = self.parse_args('left', args)
        if turtle_args:
            self.turtles[turtle_args[0]].left(turtle_args[1])

    def do_right(self, args:str):
        'Rotate a turtle some degrees clockwise, e.g.: right bill 20'
        turtle_args = self.parse_args('right', args)
        if turtle_args:
            self.turtles[turtle_args[0]].right(turtle_args[1])

    def do_pen(self, args:str):
        'Put the pen up or down, e.g.: pen bill up'
        turtle_args = self.parse_args('pen', args)
        if turtle_args:
            self.turtles[turtle_args[0]].pen(turtle_args[1])

    ############ Added command to show the current states of the turtles.

    def do_status(self, args:str):
        'Print the current state of the turtles'
        print(self)

    ############ Commands for exiting the interpreter.

    def do_bye(self, args:str):
        'Exit the turtle shell'
        return True

    def do_EOF(self, args:str):
        'Exit the turtle shell'
        return True

    ############
    ############ Helpers

    def parse_args(self, command:str, args:str):
        """Parse arguments to the turtle language commands.

        See the preamble to the file for the syntax accepted.
        We print informative error messages to screen if there is something
        wrong about the arguments, and continue the interpreters cmd.Cmd
        loop.  (This is in keeping with cmd.Cmd's behaviour for unrecognized
        commands, and seems proper.)
        """

        # no arguments supplied (there always ought to be at least one)
        if not args:
            print(f"*** Unknown syntax for '{command}': arguments needed")
            return

        # get the individual arguments and their number
        turtle_arg_list = args.split()
        n_args = len(turtle_arg_list)

        ### arguments for 'turtle'
        if command == 'turtle':
            if n_args != 1:
                print(f"*** Unknown syntax for '{command}' (too many args): "
                      f"'{args}'")
                return
            else:
                return turtle_arg_list
        ### arguments for 'colour'
        elif command == 'colour':
            if n_args != 2:
                print(f"*** Unknown syntax for '{command}' (wrong #args): "
                      f"'{args}'")
                return
            elif not turtle_arg_list[0] in self.turtles:
                print(f"*** Unknown syntax for '{command}': "
                      f"'{turtle_arg_list[0]}'' is not a turtle")
                return
            elif not turtle_arg_list[1] in self.colours:
                print(f"*** Unknown syntax for '{command}': "
                      f"'{turtle_arg_list[1]}'' is not a known colour")
                return
            else:
                return turtle_arg_list
        ### arguments for 'move'
        elif command == 'move':
            if n_args != 2:
                print(f"*** Unknown syntax for '{command}' (wrong #args): "
                      f"{args}")
                return
            elif not turtle_arg_list[0] in self.turtles:
                print(f"*** Unknown syntax for '{command}': "
                      f"'{turtle_arg_list[0]}'' is not a turtle")
                return
            else:
                try:
                    delta = float(turtle_arg_list[1])
                except ValueError:
                    print(f"*** Unknown syntax for '{command}': "
                          f"'{turtle_arg_list[1]}'' is not a real number")
                    return
                turtle_arg_list[1] = delta
                return turtle_arg_list
        ### arguments for 'rotate' (i.e., 'left' and 'right')
        elif command =='left' or command == 'right':
            if n_args != 2:
                print(f"*** Unknown syntax for '{command}' (wrong #args): "
                      f"{args}")
                return
            elif not turtle_arg_list[0] in self.turtles:
                print(f"*** Unknown syntax for '{command}': "
                      f"'{turtle_arg_list[0]}'' is not a turtle")
                return
            else:
                try:
                    theta = float(turtle_arg_list[1])
                except ValueError:
                    print(f"*** Unknown syntax for '{command}': "
                          f"'{turtle_arg_list[1]}'' is not a real number")
                    return
                if theta < 0.0 or theta >= 360.0:
                    print(f"*** Unknown syntax for '{command}': "
                          f"'{turtle_arg_list[1]}'' should be in [0,360)")
                    return
                else:
                    turtle_arg_list[1] = theta
                    return turtle_arg_list
        ### arguments for 'pen'
        elif command == 'pen':
            if n_args != 2:
                print(f"*** Unknown syntax for '{command}' (wrong #args): "
                      f"{args}")
                return
            elif not turtle_arg_list[0] in self.turtles:
                print(f"*** Unknown syntax for '{command}': "
                      f"{turtle_arg_list[0]} is not a turtle")
                return
            elif not turtle_arg_list[1] in self.pen_states:
                print(f"*** Unknown syntax for '{command}': "
                      f"'{turtle_arg_list[1]}'' is not a known pen state")
                return
            else:
                return turtle_arg_list

########################
########################

class Turtle:
    """Class for storing current state of each turtle."""

    def __init__(self, app:TurtleApp=None,
                       x:float=0.0, y:float=0.0, theta:float=90.0):
        """
        Make a turtle.

        We store the current state of the turtle, and a reference to the
        tk.Frame object, if this exists (i.e., if we are not running in text
        mode only).  Co-ordinates are stored separately as x- and y-values
        (tuple-based storage would present no obvious advantage).

        The default values allow a more simple use of the constructor when
        we are in text mode.  In that mode, we can presume turtles start
        at the origin, that the coordinates are to be imagined in standard
        Cartesian fashion (+ve x and y go right and up), and that angles
        are measured anti-clockwise starting from the positive x axis.
        (So, we do things more intuitively than tkinter's representation.)
        """

        self.app = app
        self.x = x
        self.y = y
        self.theta = theta
        self.pen_down = True
        self.colour = 'black'


    def __str__(self) -> str:
        """
        String representation of turtle.

        This is primarily for use by the 'status' command by which the
        turtle language is here augmented, though it functions in text
        mode, too.
        """

        coords_str = f'({self.x: >7.2f}, {self.y: >7.2f})'
        theta_str = f'{self.theta: >6.2f}°'
        if self.pen_down:
            pen_state = 'DOWN'
        else:
            pen_state = 'UP'
        pen_state_str = f'{pen_state: ^4}'
        colour_str = f'{self.colour}'
        return f'{coords_str} | {theta_str} | {pen_state_str} | {colour_str}'


    def __repr__(self) -> str:
        """This is added to give a useful representation in text mode."""
        return f'mockturtle.Turtle object: {str(self)}'


    def left(self, dtheta:int):
        """Rotate the turtle anti-clockwise by dtheta degrees."""
        if self.app:
            self.theta = (self.theta - dtheta) % 360
        else:
            # text mode
            self.theta = (self.theta + dtheta) % 360


    def move(self, delta:float):
        """Move the turtle delta units in its current direction."""

        # calculate coords to move to
        theta_radians = math.radians(self.theta)
        x2 = self.x + (delta * math.cos(theta_radians))
        y2 = self.y + (delta * math.sin(theta_radians))

        if self.pen_down:
            if self.app:
                # if we have a gui, drawing is controlled by it
                self.app.draw_line(self.x, self.y, x2, y2, self.colour)
            else:
                # in text mode, we notify the line drawn to stdout
                print(f'    drew from ({self.x:.2f}, {self.y:.2f})'
                      f' to ({x2:.2f}, {y2:.2f})')
        
        # update turtle position
        self.x = x2
        self.y = y2


    def pen(self, pen_position:str):
        """Set the pen to be up or down."""
        if pen_position == 'up':
            self.pen_down = False
        elif pen_position == 'down':
            self.pen_down = True


    def right(self, dtheta:int):
        """Rotate the turtle clockwise by dtheta degrees."""
        if self.app:
            self.theta = (self.theta + dtheta) % 360
        else:
            # text mode
            self.theta = (self.theta - dtheta) % 360

########################
######################## setup functions, if running as script

def command_line_args():
    """Parse command-line arguments and run some simple checks."""

    # Get the command-line arguments
    parser = argparse.ArgumentParser('turtle graphics interpreter')
    parser.add_argument('-x', '--wx',
                        type=int,
                        default=600,
                        help='width of window')
    parser.add_argument('-y', '--wy',
                        type=int,
                        default=600,
                        help='height of window')
    parser.add_argument('-p', '--turtle_program',
                        help='filename of turtle program to execute')
    parser.add_argument('-s', '--speed',
                        type=int,
                        choices=range(0, 26),
                        default=3,
                        metavar='{0..25}',
                        help='speed of turtles')
    parser.add_argument('-d', '--delay',
                        type=int,
                        default=50,
                        help='delay (ms) between drawing line segments')
    args = parser.parse_args()

    # Run some checks
    if args.turtle_program:
        if not os.path.isfile(args.turtle_program):
            print(f'Error: turtle program file {args.turtle_program} not found')
            sys.exit(1)

    return args

#######################

def configure_root(root:tk.Tk, width:int, height:int):
    """Set up some basic properties for the root."""
    
    # register SIGTERM/SIGINT handler
    signal.signal(signal.SIGTERM, partial(bye_to_turtleshell, root))
    signal.signal(signal.SIGINT, partial(bye_to_turtleshell, root))
    """Set some basic properties of the root window."""
    root.geometry(f'{width}x{height}+750+50')
    root.title('Turtles')
    # register handler for close-window event
    root.protocol("WM_DELETE_WINDOW", lambda: bye_to_turtleshell(root))


def bye_to_turtleshell(root:tk.Tk, *args):
    """Handler if root window is closed, or SIGTERM/SIGINT received.

    We tell the interpreter to exit by putting 'bye' at the front of its
    command queue.  This stops the interpreter.  Code in
    TurtleApp.run_turtle_shell() then destroys all the tk objects.

    However, it will only do this the next time the cmd.Cmd's cmdloop()
    draws a line from its cmdqueue; so if the interpreter is waiting
    for something from the prompt, this has no effect (until the cmdloop()'s
    readline() exits).

    As a consequence, the correct way to stop everything, if the prompt is
    waiting for a command, is by writing 'bye' at the prompt.
    """
    
    if root.turtleshell:
        root.turtleshell.cmdqueue.insert(0, 'bye')

########################
########################

def main():

    args = command_line_args()                 # get command-line args and check
    root = tk.Tk()                             # make the root tk window
    configure_root(root, args.wx, args.wy)     # set root window properties
    TurtleApp(root, args)                      # start turtle app in the root 
    root.mainloop()                            # tk main event loop

########################

if __name__ == '__main__':
    main() 
