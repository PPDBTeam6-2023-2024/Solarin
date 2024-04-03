import axios from "axios";
import army_example from "../../Images/troop_images/Soldier.png"

export const getArmies = async (socket) => {
  try {
    socket.onmessage = (event) => {
        let response = JSON.parse(event.data)
        return response.data.map(army => ({
            id: army.id,
            x: army.x,
            y: army.y,
            src: army_example,
            owner: army.owner,
            style: {
              position: 'absolute',
              left: `${army.x * 100}%`,
              top: `${army.y * 100}%`,
              transform: 'translate(-50%, -50%)',
              maxWidth: '10%',
              maxHeight: '10%',
              zIndex: 15,
              cursor: 'pointer'
            },
            onClick: () => {},
          }));
    }
  } catch (e) {
    console.error('Error getting armies:', e);
    return [];
  }
};
export const toggleArmyViewer = async (e, army, setActiveArmyViewers) => {
    const overlayRect = e.target.getBoundingClientRect();
    const position = {
        x: overlayRect.left + window.scrollX,
        y: overlayRect.top + window.scrollY
    };
    const to_position = {
        x: army.to_x + window.scrollX,
        y: army.to_y + window.scrollY
    }
    setActiveArmyViewers(prev => {
        const index = prev.findIndex(viewer => viewer.id === army.id);
        if (index >= 0) {
            // Remove viewer if already active
            return prev.filter(viewer => viewer.id !== army.id);
        } else {
            return [...prev, {id: army.id, owner: army.owner, position, to_position, anchorEl: e.target, detailsOpen: false}];
        }
    });
};
export const updateArmyPosition = async (armyId, newX, newY, setArmyImages, setUpdateTrigger) => {
    setArmyImages(currentArmyImages => currentArmyImages.map(army => {
        if (army.id === armyId) {
            return {...army, x: newX, y: newY};
        }
        return army;
    }));
    setUpdateTrigger(prev => !prev)
};
export const toggleArmyDetails = async (armyId, setActiveArmyViewers, activeArmyViewers) => {
    setActiveArmyViewers(activeArmyViewers.map((elem, i) => {
        if (elem.id == armyId) {
            elem.detailsOpen = !elem.detailsOpen
        }
        return elem
    }))
}    
