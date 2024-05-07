
# Trading

## Overview
Explanation how trading works
## Technologies used
- pytest
- fastapi

## Description
Trading actions are done using a TradingWebsocket.
This is done by a websocket to be able to update the information changes live.
Using the endpoint 4 actions exist:
- get trades: retrieve the current trading information
- accept trade: accept someone else their trade offer
- cancel trade: cancel own trade offer
- create trade: creates a new trade offer

These actions are done by calling tradeAccess Methods

