import React, {useContext, useEffect, useState} from "react";
import {useSelector} from "react-redux";
import Tooltip from "@mui/material/Tooltip";
import resourcesJson from "../ResourceViewer/resources.json"
import "./ResourceFilter.css"
import {openAddTradeContext} from "./openAddTradeContext";
function ResourceFilter(props) {
    const resources = useSelector((state) => state.resources.resources)

    const [selectedFilter, setSelectedFilter] = props.filter;

    /*Get access to the open Add Trade state, to be able to add the button add trade to the resource filter*/
    const [openAddTrade, setOpenAddTrade] = useContext(openAddTradeContext);

    /*Support filtering for trading*/
    return (
      <div className="ResourceFilterTab">

          {Object.entries(resources).map((resource, index) =>
              <>

                  {resourcesJson[resource[0]] !== undefined &&
                      <>
                          {selectedFilter === resource[0] ?
                              <div className="ResourceFilterIcon" style={{"backgroundColor": "var(--tertiaryColor)"}} onClick={() =>{setSelectedFilter("")}}>
                                  <img src={(`/images/resources/${resourcesJson[resource[0]]["icon"]}`)}
                                       alt={resource[0]} draggable={false}/>
                              </div>:
                              <div className="ResourceFilterIcon" onClick={() =>{setSelectedFilter(resource[0]);}}>
                                  <img src={(`/images/resources/${resourcesJson[resource[0]]["icon"]}`)}
                                       alt={resource[0]} draggable={false}/>
                              </div>
                          }
                      </>
                  }
              </>
          )}

          {openAddTrade ?
          <div className="ResourceFilterIcon" style={{"backgroundImage": "linear-gradient(5deg, var(--tertiaryColor), var(--secundaryColor))"}} onClick={() =>{setOpenAddTrade(!openAddTrade)}}>
              <div className="ResourceFilterAddTradeCross"></div>
          </div>
              :
          <div className="ResourceFilterIcon" onClick={() =>{setOpenAddTrade(!openAddTrade)}}>
              <div className="ResourceFilterAddTradeCross" style={{"width": "100%", "height": "100%"}}></div>
          </div>
          }


      </div>
    )
}

export default ResourceFilter