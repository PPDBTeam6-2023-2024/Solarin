# Hidden Windows Viewer

## Overview
A window that showcases other windows that are currently hidden.

## Technologies used
- MaterialUI
- React
- Redux

## Description
Redux is used to manage a state that is an array of currently hidden windows.
Components wrapped with WindowUI can then be hideable by adding in it the prop "hideState" and the name of the window by passing the prop "windowName". 
The WindowUI listens to the hideState to either hide the window (and add it to the hidden windows viewer) or remove it and make it visible again. 
## Issues

## Additional Information
