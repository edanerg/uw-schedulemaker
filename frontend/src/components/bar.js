import React, { Component } from 'react';
import { AppBar,
         Toolbar,
         IconButton,
         Typography } from '@material-ui/core';
import MenuIcon from '@material-ui/icons/Menu';


class Bar extends Component {
    /* 
    TODO: 1. get rid of ugly inline style
          2. consider adding a searching bar to search course name
          3. consider adding a side bar
     */
    render() {
        return (
            <AppBar position="static">
                <Toolbar style={{display: "flex", flexDirection: "row", justifyContent: "space-between", alignItems: "center"}}>
                    <div style={{display: "flex", flexDirection: "row", justifyContent: "start", alignItems: "center"}}>
                        <IconButton
                            edge="start"
                            color="inherit"
                            aria-label="open drawer">
                            <MenuIcon />
                        </IconButton>
                        <Typography variant="h6" noWrap>
                            UWScheduling
                        </Typography>
                    </div>
                </Toolbar>
            </AppBar>
        )
    }
}

export default Bar;