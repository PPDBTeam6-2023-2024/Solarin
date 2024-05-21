import React, {useState, Fragment, useContext} from 'react';
import {Box, List, ListItemButton, Popper} from "@mui/material";
import ArmyViewer from "./ArmyViewer";
import {UserInfoContext} from "../../Context/UserInfoContext";

function ArmyManageView({id, owner, anchorEl, toggleMoveMode, isMoveMode, onCityCreated}) {
    /**
     * This component visualizes the small menu when clicking on an army.
     * Using this menu you can open the army details and move your army
     * */
    const [userInfo, setUserInfo] = useContext(UserInfoContext);

    /*
    * Stores whether the details menu is opened or not
    * */
    const [detailsOpen, setDetailsOpen] = useState(false);

    return (
        <Fragment key={`army-viewer-${id}`}>
            <Popper open={true} anchorEl={anchorEl} placement='left-start'>
                <Box className="bg-black rounded-3xl">
                    <List>
                        {/*Visualize the button to move an army*/}
                        {owner === userInfo.id && <ListItemButton
                            onClick={() => toggleMoveMode(id)}>{isMoveMode(id) ? 'Cancel Move To' : 'Move To'}</ListItemButton>}
                        <ListItemButton onClick={() => setDetailsOpen(!detailsOpen)}>Details</ListItemButton>
                    </List>
                </Box>
            </Popper>
            <Popper open={detailsOpen} anchorEl={anchorEl} placement='right-start'>
                {/*Shows the army detail menu*/}
                <ArmyViewer armyId={id} is_owner={owner === userInfo.id} onCityCreated={onCityCreated} in_space={false}/>
            </Popper>
        </Fragment>
    );
}

export default ArmyManageView;