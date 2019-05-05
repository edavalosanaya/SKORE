<p align="center">
  <img src="https://user-images.githubusercontent.com/40870026/52389912-6e27bf80-2a5b-11e9-8bc6-0109e2915dbd.png" width="30%" height="30%">
</p>

---

<p align="center">
  <img src="https://user-images.githubusercontent.com/40870026/57198224-f839d400-6f35-11e9-8ad8-8afecb4a9b1c.PNG" width="1000">
</p>

This repository contains the source files for SKORE, Smart Keyboard Operated By Robotic Educator. These source files include both the hardware CAD files and the software source code. The goal in the project is to provide an easy method to learn any song in the piano. The project utilizes both **Python 3.6.6** and an Arduino to direct an modular LED bar, that goes above the piano keys, to indicate the user of the upcoming notes. The project requires an Arduino, Windows 10 (highly recommended with an Intel Processor), access to a 3D printer, and (for now) access to a PBC printer.

#### Note

SKORE now has a Windows executable **(.exe)** available in GitHub. If you would like to run SKORE and meet the computer requirements to run the application, you can find the executable within the releases page of the GitHub repository.

### Current Working Prototype

Here is a .gif displaying the project. It is still in development, but the project is coming together and working well.

<p align="center">
  <img src="https://user-images.githubusercontent.com/40870026/53314624-065bdc00-3885-11e9-80bb-1b8787e5b48d.gif" width="1000">
</p>

Here is how the SKORE GUI looks like:

<p align="center">
  <img src="https://user-images.githubusercontent.com/40870026/57198244-1ef80a80-6f36-11e9-854a-b07a71d2574e.PNG" width="1000">
</p>

And here is how the SKORE hardware looks like:

<p align="center">
  <img src="https://user-images.githubusercontent.com/40870026/57198162-3c78a480-6f35-11e9-93d0-0815f8c28c3e.png" width="1000">
</p>

### How It Works

The project utilizes a LED bar to assist the user in learning a song. The LED bar is controlled by an Arduino. Then through serial communication, Python coordinates the Arduino to follow the ON/OFF note events contained within the MIDI file. Through multiple file conversions, an MP3 and PDF can be converted to a MIDI file that can be interpreted to realize the tutoring feature of SKORE. Ultimately, the quality of the file conversion depends on the original quality and simplicity of the input file. Here's an general view of the SKORE system.


<p align="center">
  <img src="https://user-images.githubusercontent.com/40870026/57198131-f8859f80-6f34-11e9-91dc-2094f0240098.PNG" width="700">
</p>

For further information of the project, look into the Wiki of this GitHub repository.
