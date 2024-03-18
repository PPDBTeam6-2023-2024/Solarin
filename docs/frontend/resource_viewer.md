# Resource Viewer

## Overview
A window where the owned amount and collection rate of different resources is visualized.
<br>![Resource Viewer Image](https://res.cloudinary.com/dmejmwxek/image/upload/v1710675560/resource_viewer.png)
## Technologies used
- ReactJS
- Material UI
- react-draggable
- JSON

## Description
The ResourceViewer component takes the following arguments (also known as props in react)
- className: the styling of the window container
- title: the title of the window
- resources: an object of form {"resource_acronym": {"collected": n, "producing": m}, ...}
- draggable: a boolean denoting if the window can be dragged by the mouse or not

Given these arguments the component will render a window that displays the information in an organized manner.

## Issues
None

## Additional Information
None
