# FSC File Generator

1. Introduction
2. Requirements/Installation
3. Current Functionality

---

## Introduction

The FSC File Generator (FFG) is a small Python program with a Tkinter GUI. This program allows users to convert `.dax` files into `.fsc` files compatible with the MicroNav Simulator format. Especially useful for CWP and FDP systems, this program extracts all flightplans from a `.dax` file and generates the FDP scripts necessary for correlation on the Harris-Orthogon/MicroNav CWP. In the current version of BEST, each flightplan requires 7 scripts with `REG` and `CODE` scripts.

If you are running a stimulated environment, for instance with Leonardo CWPs, the `REG` and `CODE` values will have to be unique in order for the correlation to work correctly.

---

## Requirements/Installation

In the current version, you will need to ensure you have `tkinter` installed within your Python environment. I am currently using this library to create a simple GUI. I am planning to release a package with a `.exe` file. I am planning to create a web version of this application soon.

---

## Current Functionality

In its current version, this program can browse to the location of a `.dax` file. Once the user has selected said file, the program will open it and iterate over each line, extracting any and all callsigns from it. Once this process has been completed, the program will then generate the 7 scripts per callsign and writing it to a `.fsc` file with the same name as the `.dax` file. Depending on the size of the `.dax` file, the processing time may vary. During testing, files with around 300 flights took `1 second` to complete.
