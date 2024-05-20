import React from "react";
/*
calculate position based on source- and target position and how much time has elapsed
* */
export const lerp = ({sourcePosition, targetPosition, arrivalTime, departureTime}) => {
        let date = new Date()
        date.setHours(date.getHours() - 2)

        const elapsedTime = date - departureTime
        const totalTime = arrivalTime - departureTime
        const percentComplete = (elapsedTime < totalTime) ? elapsedTime / totalTime : 1;
        const currentX = sourcePosition.x + (targetPosition.x - sourcePosition.x) * percentComplete
        const currentY = sourcePosition.y + (targetPosition.y - sourcePosition.y) * percentComplete
        return {x: currentX, y: currentY}
}