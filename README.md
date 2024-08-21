# Task Management Application (v0.0.5)

This is a simple task management application built using Python and Pyside6.  
Goal is to be fully functional, calendar and database integration plus a map of tasks completed over time.  
A heap map of ativities to track daily routine and gamify the process (separate version?)  


## Features

- **Dragable tasks**: dragable tasks inside a group (should let tasks be moved between diferent groups?)
- **resizzeable groups**: now we can resize groups :) 
- **structure list**: added a new folder to put structure used in a reduced testing version so its easier to implement on other functions  
- **[INPROGRESS]** **List of groups**: how should i name this? basic functionality and custom frame added, options adjusted but havent been properly implemented  
- **rename groups**: rename the group (this should not be added for tasks since they are the end point but maybe in a future release?  
- **groups and subtasks**: working flawless groups and subtasks, adds and swaps (v3) - Missing subtasks swap, bind the move group only on its title?  
- **[TODO]** **DBCONNECTION**: placeholder  
- **save settingss**: save and load settings on close/open application  
- **Help**: created help info on menu  
- **added groups and subtasks**: Added a basic group and tasks system.  
- **Calendar**: working calendar - library  
- **Minimize to tray**: added a minimize to tray functionality instead of closing application on close menu  
- **Toggle fullscreen**: The application resize to the hole screen (not native full screen) and back to the original size - only works on first monitor  
- **Ovelay**: The application has the option to stay always on top  
- **Move and Resize**: The application has a module to move and resize  
- **Menu**: added a top menu to open an options window with some basic functionalities  
- **Close Application**: A button to close/minimize the application.  
- **Blank Window**: A basic window is set up using Pyside6.  


## Known Bugs and TODO functions

- [TESTING] removed group to clear the uid?  
- [TODO] resize widget too? save the height of frames? 
- [TODO-DIF REVISION] implement an executable and add on big flag versions (0.0.5 or 1.0.0 ?)  
- [TODO] Db management and connection -> tasks and groups  
- [WIP] review code and reorganize the functions  
- [TODO] start recreating the interface with custom icons  
- [TODO-DIF REVISION] define the minimum size and aspect ratio for the tasks  


## Version Control

- **MAJOR** version changes (X.y.z) indicate incompatible API changes or significant updates.
- **MINOR** version changes (x.Y.z) indicate backward-compatible new features.
- **PATCH** version changes (x.y.Z) indicate backward-compatible bug fixes.


### Branching Strategy

The repository follows a structured Git branching strategy:

- **`main` branch**: This branch contains the latest stable release version. Only merge into `main` once the code has been fully tested and is ready for production.
- **`develop` branch**: This branch contains the most recent development version. It includes features and fixes that are still under testing and may not be stable.