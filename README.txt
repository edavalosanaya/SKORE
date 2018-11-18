Development Team: Ashkan A., Zachary B., and Eduardo D.
SKORE (Smart Keyboard Operated by Robotic Educator)
Expected time for project and proper documentation completion: March 2019

Description:

This is our Electrical Senior Design Project. Eventually, this code will
provided with the user the capability of importing .mp3 and .pdf music files and
convert them into .midi and .pdf files. Additional software and hardware will be
utilized to guide the user with an LED rod, above the piano keyboard. Three
different modes of tutoring will be created: Beginner, Intermediate, and Expert.
Additionally, the 3D models of the LED rod will be upload when completed. The
complete schematic of the LED array will be provided when possible. The goal of
this project to provide to the open-source community with a complete product,
including software, electrical schematics, and LED rod's 3D models, to help
the public with the fabrication of their own piano tutoring device.

Further Description of the Device:

Tutoring Modes

+Beginner Mode will indicate the user of the finger placements and wait until the
user presses the key.
+Intermediate Mode will play the song at a tunable speed and the user must follow
along.
+Expert Mode will only light up the LED rod if the user incorrectly plays the
notes, this way the user test their knowledge of the piece.

Installation:
Note: pdf to midi file conversion is only functional with an Intel Processor
Windows 10 computer. Other features of the application theoretically function in
Linux and Mac as well, but they have not been tested in those operation systems yet.

For this application to function please install the following programs:
-Audiveris (Will require 64-bit OS and Intel Processor) [difficult installation] (v5.1.0:0bf682689)
    +https://github.com/audiveris
    -Java JDK version 8
        +http://www.oracle.com/technetwork/java/javase/downloads/index.html
    -Gradle
        +https://gradle.org/
    -Tesseract OCR
        +https://github.com/tesseract-ocr/tesseract
-Audacity (v2.1.0)
    +https://sourceforge.net/projects/audacity/files/latest/download
-Red Dot Forever (v1.04)
    +https://sourceforge.net/projects/reddot/files/latest/download
-MidiSheetMusic-2.6 (v2-6)
    +http://midisheetmusic.com/download.html
-AmazingMIDI (v1.70)
    +http://www.pluto.dti.ne.jp/~araki/amazingmidi/
-AnthemScore(Optional, not free)
    +https://www.lunaverus.com/
-Xenoplay [aka Xenoage Player] (v0.4.2007.06.26)
    +https://sourceforge.net/projects/xenoplay/
-PianoBooster (v0.6.4)
    +http://pianobooster.sourceforge.net/screenshots.html
-LoopBe1 (v1.6)
    +https://www.nerds.de/en/download.html
-Python 3.6.6
    -pip
        +Windows Installation:https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation
    -PyQt5 Library
        +https://www.riverbankcomputing.com/software/pyqt/download5
            -pip install worked better than traditional installation method
    -Pywinauto
        +https://pywinauto.github.io/
