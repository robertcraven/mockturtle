# mockturtle
Simple python interpreter for a subset of the turtle graphics language.

AUTHOR: Robert Craven  
EMAIL:  robert.craven@gmail.com

## USAGE

Doing a 'mockturtle.py -h' will show usage.

## MODES OF RUNNING

Three modes of running are supported.

 - The principal way is by executing this script: this shows a gui.
   See EXAMPLE 1 and EXAMPLE 3, below.
 - The first text-based method is by running the TurtleShell after importing
   this file as a module.  See EXAMPLE 2 and EXAMPLE 4.
 - Alternatively, one can import the module and create Turtle objects,
   running their functions directly.  See EXAMPLE 5.

## FORMS OF INPUT

If we run a turtle shell (whether within an associated TurtleApp, or
in text mode), then then commands of the turtle graphics language can
be typed into a command shell (EXAMPLES 1 and 2, below), or can be
loaded from a file whose name is passed as input (EXAMPLES 3 and 4).

Otherwise, commands are passed using functions within Turtle(),
as in EXAMPLE 5.

## EXAMPLES

### EXAMPLE 1

This draws a line from the center to 100 units north, s l o w l y.

> % ./mockturtle.py -s 1 -d 100              
>  t: turtle rob  
>  t: move rob 100  
>  t: bye  
> % 

### EXAMPLE 2

Text-based use of the TurtleShell.

> % python3  
> Python 3.6.7 (default, Oct 22 2018, 11:32:17)   
> [GCC 8.2.0] on linux  
> Type "help", "copyright", "credits" or "license" for more information.  
> '>>>' import mockturtle as mt  
>  '>>>' mt.TurtleShell().cmdloop()  
>  t: turtle bill   
>  t: move bill 90  
>     drew from (0.00, 0.00) to (0.00, 90.00)  
>  t: right bill 30  
>  t: move bill 20  
>     drew from (0.00, 90.00) to (10.00, 107.32)  
>  t: status  
>           bill:  (  10.00,  107.32) |  60.00° | DOWN | black  
>  t: bye  
> '>>>'' quit()  
> %

### EXAMPLE 3

This draws a sample file quickly (not instantaneously).

 % ./mockturtle.py -s 20 -d 10 -p ../turtle_programs/squares.tt
  t: bye
 %

### EXAMPLE 4

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

### EXAMPLE 5

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

## PROGRAM STRUCTURE

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

## MAIN CLASSES AND FUNCTIONS

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

## SHUTTING DOWN

Behaviour when shutting the thing down has involved some compromise.
(Partly because of 'threading', partly because of issues with the
interaction of cmd.Cmd.cmdloop() and tk.mainloop(), I think.)  

If the prompt is waiting for a command, then just write 'bye'.
(Shutting the window, of CTRL-C, etc., will not work as they ought.)
If the application is running a program passed from file, then either
close the window or CTRL-C in the terminal should work.

## SUBSET OF TURTLE LANGUAGE

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

  x, for 'move', must be castable to a float (so it can be negative or 0)
  x, for 'left' and 'right', must be castable to a float in [0,360)
  c - must be one of ['azure', 'beige', 'black', 'blue', 'brown',
                      'chartreuse', 'chocolate', 'coral', 'cyan',
                      'firebrick', 'gainsboro', 'gold', 'gray','green',
                      'indigo', 'lavender', 'lime', 'magenta',
                      'maroon', 'olive', 'orange', 'pink', 'plum',
                      'purple', 'red', 'salmon', 'tan', 'thistle',
                      'tomato', 'violet', 'white', 'yellow']
