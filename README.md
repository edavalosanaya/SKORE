<p align="center">
  <img src="https://user-images.githubusercontent.com/40870026/52389912-6e27bf80-2a5b-11e9-8bc6-0109e2915dbd.png" width="20%" height="20%">
</p>

---
<div class="left">
<iframe width="560" height="315" src="https://www.youtube.com/embed/AYdyRPIo4ZA" frameborder="0" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

(Development is still on-going, project is expected to be complete by April 2019)

This repository contains the source files for SKORE, Smart Keyboard Operated By Robotic Educator. The goal in the project is to provide an easy method to learn any song in the piano. The project utilizes both Python 3.6.6 and an Arduino to direct an modular LED bar, that goes above the piano keys, to indicate the user of the upcoming notes. The project requires an Arduino, Windows 10 (highly recommended with an Intel Processor), access to a 3D printer, and (for now) access to a PBC printer.

### Current Working Prototype

Here is a .gif displaying the project. It is still in development, but the project is coming together and working well.

<p align="center">
  <img src="https://user-images.githubusercontent.com/40870026/53314624-065bdc00-3885-11e9-80bb-1b8787e5b48d.gif" width="1000">
</p>

Here is how the SKORE GUI looks like:

<p align="center">
  <img src="https://user-images.githubusercontent.com/40870026/53346936-a80f1780-38dd-11e9-83c2-e49c639eac90.png" width="1000">
</p>

And here is how the SKORE hardware looks like:

<p align="center">
  <img src="https://user-images.githubusercontent.com/40870026/53346900-962d7480-38dd-11e9-9e50-750a85609bdb.jpg" width="1000">
</p>

### How It Works

The project utilizes a LED bar to assist the user in learning a song. The LED bar is controlled by an Arduino. Then through serial communication, Python coordinates the Arduino to follow the ON/OFF note events contained within the MIDI file. Through multiple file conversions, an mp3 and pdf can be converted to a MIDI file that can be interpreted to realize the tutoring feature of SKORE. Ultimately, the quality of the file conversion depends on the original quality and simplicity of the input file. Here's an general view of the SKORE system.


<p align="center">
  <img src="https://user-images.githubusercontent.com/40870026/53306561-38a11580-3854-11e9-8917-dcc01f097d9b.PNG" width="700">
</p>

For further information of the project, look into the Wiki of this project.
