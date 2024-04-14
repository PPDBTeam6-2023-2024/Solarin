import React, {useEffect, useState} from "react";
import {useSelector} from "react-redux";
import Tooltip from "@mui/material/Tooltip";
import resourcesJson from "../ResourceViewer/resources.json"
import "./ResourceFilter.css"
function ResourceFilter(props) {
    const resources = useSelector((state) => state.resources.resources)

    const [selectedFilter, setSelectedFilter] = props.filter;

    /*Support filtering for trading*/
    return (
      <div className="ResourceFilterTab">

          {Object.entries(resources).map((resource, index) =>
              <>

                  {resourcesJson[resource[0]] !== undefined &&
                      <>
                          {selectedFilter === resource[0] ?
                              <div className="ResourceFilterIcon" style={{"backgroundColor": "var(--tertiaryColor)"}}>
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

      </div>
    )
}

export default ResourceFilter