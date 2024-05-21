export const toggleArmyViewer = async (e, army, setActiveArmyViewers) => {
    /**
     * Open an army menu
     * */
    const overlayRect = e.target.getBoundingClientRect();
    const position = {
        x: overlayRect.left + window.scrollX,
        y: overlayRect.top + window.scrollY
    };
    const toPosition = {
        x: army.to_x + window.scrollX,
        y: army.to_y + window.scrollY
    }
    setActiveArmyViewers(prev => {
        const index = prev.findIndex(viewer => viewer.id === army.id);
        if (index >= 0) {
            // Remove viewer if already active
            return prev.filter(viewer => viewer.id !== army.id);
        } else {
            return [...prev, {
                id: army.id, owner: army.owner, position,
                arrivalTime: army.arrivalTime, departureTime: army.departureTime,
                toPosition: toPosition, anchorEl: e.target
            }];
        }
    });
};

export const closeArmyViewer = (army, setActiveArmyViewers) => {
    /**
     * Close an army menu
     * */
    setActiveArmyViewers(prev => {
        const index = prev.findIndex(viewer => viewer.id === army.id);
        if (index >= 0) {
            // Remove viewer if already active
            return prev.filter(viewer => viewer.id !== army.id);
        }
    });

};