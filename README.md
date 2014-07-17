Phonological CorpusTools
========================

This document contains installation instructions. For a description of available functionality, please refer to the manual included alongside this file.


## Standard installation (executable)

### Windows

(NOTE: This method requires that you are running a 64-bit version of windows. You can check this by in Control Panel -> System and Security -> System.)

Download the file 'corpustools-0.15-amd64.msi' from the Phonological CorpusTools page on SourceForge. It can be found here: http://sourceforge.net/projects/phonologicalcorpustools/files/0.15/win64/corpustools-0.15-amd64.msi/download . Double-click this file to install PCT to your computer. It can then be run the same as any other program, via Start -> Programs.

### Mac OS X

Download the file 'pct.zip' from the Phonological CorpusTools page on SourceForge. It can be found here: http://sourceforge.net/projects/phonologicalcorpustools/files/0.15/macosx/pct.zip/download . Unzip this file to access 'pct.app'. You can then double-click this file to run Phonological CorpusTools.

### Linux

There is currently no executable option available for Linux operating systems. Please use the fallback installation method below to install from source.


## Fallback installation (setup.py)

### Windows, Mac OS X, or Linux

Dependencies (be sure these are installed first):
- Python 3.3 or higher: https://www.python.org/downloads/release/python-341/
- Tk: http://www.tcl.tk/software/tcltk/

Download the source code for Phonological CorpusTools. In the top level directory, there is a file called 'setup.py'. Run it in *one* of the following ways:

1. Double-click it. If this doesn't work, access the file properties and ensure that you have permission to run the file; if not, give them to yourself. In Windows, this may require that you open the file in Administrator mode (also accessible through file properties). If your computer opens the .py file in a text editor rather than running it, you can access the file properties to set Python 3.x as the default program to use with run .py files. If the file is opened in IDLE (a Python editor), you can use the "Run" button in the IDLE interface to run the script instead.

2. Open a terminal window and run the file. In Linux or Mac OS X, there should be a Terminal application pre-installed. In Windows, you may need to install Cygwin ( https://www.cygwin.com/ ). Once the terminal window is open, nagivate to the top level CorpusTools folder---the one that has setup.py in it. (Use the command 'cd' to navigate your filesystem; Google "terminal change directory" for further instructions.) Once in the correct directory, run this command: "python3 setup.py install" (no quotes). You may lack proper permissions to run this file, in which case on Linux or Mac OS X you can instead run "sudo python3 setup.py install". If Python 3.x is the only version of Python on your system, it may be possible or necessary to use the command "python" rather than "python3".

Phonological CorpusTools should now be installed! Run it from a terminal window using the command "pct". You can also open a "Run" dialogue and use the command "pct" there. In Windows, the Run tool is usuall found in All Programs -> Accessories.