# mockturtle

Simple python interpreter for a subset of the turtle graphics
language.

## Table of Contents

 - [Command-line usage and help](#command-line-usage-and-help)
 - [Platform](#platform)
 - [Modes of running](#modes-of-running)
 - [Forms of input](#forms-of-input)
 - [Examples](#examples)
 - [Program structure](#program-structure)
 - [Main classes and functions](#main-classes-and-functions)
 - [Shutting down](#shutting-down)
 - [Subset of the turtle language](#subset-of-the-turtle-language)

## Command-line usage and help

Doing a `mockturtle.py -h` from the command line will show command-line usage:

    usage: turtle graphics interpreter [-h] [-x WX] [-y WY] [-p TURTLE_PROGRAM]
                                       [-s {0..25}] [-d DELAY]
     
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

From within the interpreter, since it subclasses `cmd.Cmd`, you can enter
`?` to receive help, or `help X` to receive help on a specific command `X`,
e.g., `help move`.

## Platform

The program is written in python (> 3.6) and has been tested on Ubuntu Linux
18.04.  (It has not been written to run on Macs or Windows.  Indeed, for the
former the issue mentioned
[here](https://stackoverflow.com/questions/15817554/obscure-repeatable-crashes-in-multi-threaded-python-console-application-using-t)
has been observed to arise.)

## Modes of running

Three modes of running are supported.

 - The principal way is by executing this script: this shows a gui.
   See [Example 1](#example-1) and [Example 3](#example-3), below.
 - The first text-based method is by running the TurtleShell after importing
   this file as a module.  See [Example 2](#example-2) and
   [Example 4](#example-4).
 - Alternatively, one can import the module and create Turtle objects,
   running their functions directly.  See [Example 5](#example-5).

## Forms of input

If we run a turtle shell (whether within an associated `TurtleApp`, or
in text mode), then then commands of the turtle graphics language can
be typed into a command shell ([Example 1](#example-1) and
[Example 2](#example-2), below), or can be loaded from a file whose
name is passed as input ([Example 3](#example-3) and
[Example 4](#example-4)).

Otherwise, commands are passed using functions within the `Turtle` objects,
as in [Example 5](#example-5).

## Examples

### Example 1

This draws a line from the center to 100 units north, s l o w l y.

    % ./mockturtle.py -s 1 -d 100              
     t: turtle rob  
     t: move rob 100  
     t: bye  
    % 

The `-s 1` sets the speed of the turtles to be slow; and the `-d 100` also
contributes to the speed setting by setting a delay of 100ms between segments
of a line drawn.   (See [Program structure](#program-structure) for more
details.)

### Example 2

Text-based use of the `TurtleShell`.

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

Here the program is imported as a module named as `mt`.  We then run the 
command interpreter by first creating a `TurtleShell`, and then starting
the command interpreter's loop with `cmdloop()`.

### Example 3

This draws a sample file quickly (not instantaneously).

    % ./mockturtle.py -s 20 -d 10 -p ../turtle_programs/squares.tt
     t: bye
    %

The speed settings (`-s 20`, `-d 10`) are much quicker than for
[Example 1](#example-1).  We read a program from a file (using `-p`),
and the interpreter executes the commands.  When done, the interpreter
allows us to enter any new commands at a prompt (` t: `).  We exit
using `bye`.

### Example 4

Show the effects of a 'red square' program, text-based `TurtleShell`.

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

This is similar to [Example 2](#example-2), except we read from a file.

### Example 5

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

Here the `mockturtle` module is imported, but we do not start the command
interpreter.  Instead, we create `Turtle` objects and run their functions
directly.

## Program structure

Using `tkinter` (as `tk`) for graphics, we open a root window, and for the
main application subclass `tk.Frame` (as `TurtleApp`).  This packs a
canvas, which can be dragged to show what stray turtles are up to.
The main application then starts a thread in which a sublcass of
`cmd.Cmd` (`TurtleShell`) is used for the interpreter.  The interpreter
then (optionally) reads the commands of any input file, and waits for
further commands at a prompt.

Both `cmd.Cmd` and `tkinter` run on a loop, and the interaction of these
has presented some complications.  (Especially in shutting down)  The
main tk loop runs in the main thread (as is strongly recommended).
The `cmd.Cmd` loop runs in a secondary thread.

Multiple turtles can be created, each an instance of the `Turtle` class.
Animation is simulated by drawing lines in segments and delaying between each
segment.  The number of segments is controlled indirectly by the
'speed' command-line argument.  This should be an integer between 0 and
25 inclusive: 1 is slowest, 25 is fastest but still animated, and 0 is
instantaneous.  The delay between drawing segments is controlled directly
by the 'delay' command-line argument.  (The idea and the form of the
relevant mathematics here has been taken from the python standard
library `turtle` module, with some modifications of parameters.)

Turtles themselves do not do their actions concurrently.  And no
turtle  itself is drawn on the canvas (only the lines appear).

## Main classes and functions

  - `class TurtleApp(tk.Frame)`:  
    Main `tk` object for controlling the interpreter and graphics

  - `class TurtleShell(cmd.Cmd)`:  
    Main object for controlling the interpreter and parsing
    commands.

  - `class Turtle`:  
    An instance for each turtle created, storing its location,
    orientation, and so on.

  - `def command_line_args()`:  
    Get command-line arguments using `argparse`

## Shutting down

Behaviour when shutting the thing down has involved some compromise.
(Partly because of `threading`, partly because of issues with the
interaction of `cmd.Cmd.cmdloop()` and `tk.mainloop()`, I think.)  

If the prompt is waiting for a command, then just write `bye`.
(Shutting the window, of `CTRL-C`, etc., will not work as they ought; though
`CTRL-D` does.)
If the application is running a program passed from file, then either
close the window or `CTRL-C` in the terminal should work.

## Subset of the turtle language

We accept the following language:

 - `turtle name`  
   create a new turtle identified by the given name
 - `move name x`  
   moves the named turtle forward by x units
 - `left name x`  
   rotate the turtle anticlockwise by x degrees
 - `right name x`  
   rotate the turtle clockwise by x degrees
 - `pen name up`  
   lift the pen off the 'paper'
 - `pen name down`  
   put the pen down so subsequent moves draw on screen
 - `colour name c`  
   set the drawing colour of the turtle appropriately

In addition:

 - `bye`  
   closes the application
 - `status`  
   prints the current states of all the terminals

where:

  - x, for `move`, must be castable to a `float` (so it can be negative or 0)
  - x, for `left` and `right`, must be castable to a `float` in [0,360)
  - c must be one of `azure`, `beige`, `black`, `blue`, `brown`,
    `chartreuse`, `chocolate`, `coral`, `cyan`,
    `firebrick`, `gainsboro`, `gold`, `gray`,`green`,
    `indigo`, `lavender`, `lime`, `magenta`,
    `maroon`, `olive`, `orange`, `pink`, `plum`,
    `purple`, `red`, `salmon`, `tan`, `thistle`,
    `tomato`, `violet`, `white`, `yellow`
