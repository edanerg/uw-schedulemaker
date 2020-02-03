import React from 'react';
import { AppBar,
         Toolbar,
         IconButton,
         Typography, 
         Button} from '@material-ui/core';
import MenuIcon from '@material-ui/icons/Menu';
import { Link } from 'react-router-dom';


function Bar(props) {
    const onLogout = () => {
        if (props.user) {
            props.setUser(null);
            props.setCoursesTaken(null);
        }
    }

    return (
        <AppBar position="static">
            <Toolbar style={{display: "flex", flexDirection: "row", justifyContent: "space-between", alignItems: "center"}}>
                <div style={{display: "flex", flexDirection: "row", justifyContent: "start", alignItems: "center"}}>
                    <IconButton
                        onClick={() => props.setSidebarOpen(!props.sidebarOpen)}
                        edge="start"
                        color="inherit"
                        aria-label="open drawer">
                        <MenuIcon />
                    </IconButton>
                    <Link to="/" style={{ textDecoration: 'none', color: "black"}}>
                        <Typography variant="h6" noWrap>
                            UWScheduling
                        </Typography>
                    </Link>
                </div>
                {!props.user ?
                <Link to="/login" style={{ textDecoration: 'none', color: "black"}}>
                    <Button>
                        Log In
                    </Button>
                </Link>
                :
                <div style={{display: "flex", flexDirection: "row", alignItems: "center"}}>
                    <Typography variant="h6" noWrap style={{marginRight: "20px"}}>
                        Welcome, {props.user.username}
                    </Typography>
                    <Link to="." style={{ textDecoration: 'none', color: "black"}} onClick={onLogout}>
                        <Button>
                            Log Out
                        </Button>
                    </Link>
                </div>
                }
            </Toolbar>
        </AppBar>
    )
}

export default Bar;