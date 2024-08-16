# Task Management Application

This is a simple task management application built using Python and Tkinter.  
Goal is to be fully functional, calendar and database integration.
Also a heap map of ativities to track daily routine and gamify the process (separate version?)


## Features

- **Blank Window**: A basic window is set up using Tkinter.
- **Close Application**: A button to close/minimize the application.
- **Menu**: added a top menu to open an options window with some basic functionalities
- **Ovelay**: The application has the option to stay always on top
- **[BUGGED]** **Move and Resize**: The application has a module to move and resize 
- **[BUGGED]** **tOGGELE FULLSCREEN**: The application resize to the hole screen (not native full screen) and back to the original size - only works on first monitor
- **[TODO]** **DBCONNECTION**: placeholder
- **Calendar**: working calendar - library
- **Minimize to tray**: added a minimize to tray functionality instead of closing application on close menu
- **[MISSING]** **added groups and subtasks**: Added a basic group and tasks system. - remove task missing


## Known Bugs and TODO functions

- [BUG] Move and Resize + snap screen adaptation
- [BUG] Toggle fullscren on multiple screens
- [TODO] Db management and connection -> tasks and groups
- [TODO] Function to remove task.
- [TODO] start saving tasks

## Version Control

- **MAJOR** version changes (X.y.z) indicate incompatible API changes or significant updates.
- **MINOR** version changes (x.Y.z) indicate backward-compatible new features.
- **PATCH** version changes (x.y.Z) indicate backward-compatible bug fixes.

### Branching Strategy

The repository follows a structured Git branching strategy:

- **`main` branch**: This branch contains the latest stable release version. Only merge into `main` once the code has been fully tested and is ready for production.
- **`develop` branch**: This branch contains the most recent development version. It includes features and fixes that are still under testing and may not be stable.