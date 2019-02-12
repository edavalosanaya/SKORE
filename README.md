<img src="https://user-images.githubusercontent.com/40870026/52389912-6e27bf80-2a5b-11e9-8bc6-0109e2915dbd.png" width="30%" height="30%" align="middle" />

---

(Source code, mechanical design, circuit design, and documentation are not complete yet: expected fully-completed by April 2019)

This repository contains the source files for SKORE, Smart Keyboard Operated By Robotic Educator. The goal in the project is to provide an easy method to learn any song in the piano. The project utilizes both Python3 and an Arduino to direct an modular LED bar, that goes above the piano keys, to indicate the user the upcoming notes. The project requires an Arduino, Windows 10 (highly recommended with an Intel Processor), access to a 3D printer, and (for now) access to a PBC printer.

<img src="https://user-images.githubusercontent.com/40870026/51092443-f49ef900-175c-11e9-855c-2f1d3c66700f.PNG" width="500" align='middle' />

Concept Design of the SKORE Project

### How it Works

The project utilizes a LED bar to assist the user in learning a song. The LED bar is controlled by an Arduino. Then through serial communication, Python coordinates the Arduino to follow the ON/OFF note events contained within the MIDI file. Through multiple file conversions, an mp3 and pdf can be converted to a MIDI file that can be interpreted to realize the tutoring feature of SKORE. Ultimately, the quality of the file conversion depends on the original quality and simplicity of the input file. Here's an simplified view of the SKORE system.

<img src="https://user-images.githubusercontent.com/40870026/51095438-5c177180-177a-11e9-9340-fca3899df69e.png" width=500 align='middle' >

### Tutoring Modes

 - Beginner Mode
    - Complete song assistance
 - Intermediate Mode
    - Play-along with upcoming note information
 - Expert Mode
    - Play-along

### Installation
Within the setup folder, there is a setup.exe that will install all the majority of the additional applications. You will still need to install Audiveris and optionally Anthemscore.

#### Beware!
The pdf to midi file conversion is only functional with an Intel Processor Windows 10 computer. Other features of the application theoretically work in Linux and Mac as well, but they have not been tested in those OS yet.

For this application to function, please install the following programs:
 - [Audiveris] (Require 64-bit OS and Intel Processor) [v5.1.0:0bf682689]
Preferably follow the installation instructions in Audiveris' wiki. You will need the following programs to run Audiveris.
     - [Java JDK version 8]
     - [Gradle]
     - [Tesseract OCR]
 - [AmazingMIDI] (v1.70)
 - [AnthemScore] (Optional, not free)

### TODO:
---

 - [ ] Improve simplicity in LED octave fabrication



[Audiveris]: <https://github.com/audiveris>
[Java JDK version 8]: <http://www.oracle.com/technetwork/java/javase/downloads/index.html>
[Gradle]: <https://gradle.org/>
[Tesseract OCR]: <https://github.com/tesseract-ocr/tesseract>
[AmazingMIDI]: <http://www.pluto.dti.ne.jp/~araki/amazingmidi/>
[AnthemScore]: <https://www.lunaverus.com/>
