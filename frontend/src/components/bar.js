import React, { Component } from 'react';
import { AppBar,
         Toolbar,
         IconButton,
         Typography, 
         Button} from '@material-ui/core';
import MenuIcon from '@material-ui/icons/Menu';
import { Link, BrowserRouter as Router } from 'react-router-dom';


class Bar extends Component {
    /* 
    TODO: 1. get rid of ugly inline style
          2. consider adding a searching bar to search course name
          3. consider adding a side bar
     */
    onLogout = () => {
        if (this.props.user) {
            this.props.setUser(null);
        }
    }

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
                        <Link to="/" style={{ textDecoration: 'none', color: "black"}}>
                            <Typography variant="h6" noWrap>
                                UWScheduling
                            </Typography>
                        </Link>
                    </div>
                    {!this.props.user ?
                    <Link to="/login" style={{ textDecoration: 'none', color: "black"}}>
                        <Button>
                            Log In
                        </Button>
                    </Link>
                    :
                    <div style={{display: "flex", flexDirection: "row", alignItems: "center"}}>
                        <Typography variant="h6" noWrap style={{marginRight: "20px"}}>
                            Welcome, {this.props.user.username}
                        </Typography>
                        <Link to="." style={{ textDecoration: 'none', color: "black"}} onClick={this.onLogout}>
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
}

export default Bar;