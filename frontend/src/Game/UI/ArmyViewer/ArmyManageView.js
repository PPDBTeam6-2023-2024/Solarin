import React, {useState, Fragment, useContext} from 'react';
import {Box, List, ListItemButton, Popper} from "@mui/material";
import ArmyViewer from "./ArmyViewer";
import {UserInfoContext} from "../../Context/UserInfoContext";

function ArmyManageView({id, owner, anchorEl, toggleMoveMode, isMoveMode, onCityCreated}) {
    const [userInfo, setUserInfo] = useContext(UserInfoContext);
    const [detailsOpen, setDetailsOpen] = useState(false);

    return (
        <Fragment key={`army-viewer-${id}`}>
            <Popper open={true} anchorEl={anchorEl} placement='left-start'>
                <Box className="bg-black rounded-3xl">
                    <List>
                        {owner === userInfo.id && <ListItemButton
                            onClick={() => toggleMoveMode(id)}>{isMoveMode(id) ? 'Cancel Move To' : 'Move To'}</ListItemButton>}
                        <ListItemButton onClick={() => setDetailsOpen(!detailsOpen)}>Details</ListItemButton>
                    </List>
                </Box>
            </Popper>
            <Popper open={detailsOpen} anchorEl={anchorEl} placement='right-start'>
                <ArmyViewer armyId={id} is_owner={owner === userInfo.id} onCityCreated={onCityCreated} in_space={false}/>
            </Popper>
        </Fragment>
    );
}

export default ArmyManageView;