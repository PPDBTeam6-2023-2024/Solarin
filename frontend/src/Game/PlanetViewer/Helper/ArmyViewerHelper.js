import army_example from "../../Images/troop_images/Soldier.png"

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
            return [...prev, {id: army.id, owner: army.owner, position,
                arrival_time: army.arrival_time, departure_time: army.departure_time,
                to_position, anchorEl: e.target}];
        }
    });
};

