import React, { Component } from 'react';
import Card from '@material-ui/core/Card';
import Link from '@material-ui/core/Link';
import Button from '@material-ui/core/Button';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import axios from 'axios';
import serverURL from '../config';
import { useHistory } from "react-router-dom";

class Login extends Component {

    state = {
        action: "Log In",
        username: null,
        usernameInvalid: false,
        helperText: null
    }

    onToggleAction = () => {
        if (this.state.action == "Log In") {
            this.setState({
                action: "Sign Up"
            })
        } else {
            this.setState({
                action: "Log In"
            })
        }
    }

    onExecuteAction = () => {
        if (this.state.action == "Log In") {
            axios.post(`${serverURL}/user`, {
                action: "login",
                username: this.state.username
            })
            .then(res => {
                const newUser = res.data.user;
                if (newUser) {
                    this.props.setUser(res.data.user);
                    axios.get(`${serverURL}/coursesTaken`, {params: {username: this.state.username}})
                    .then(res => {
                        this.props.setCourses(res.data.courses);
                    })
                } else {
                    this.setState({
                        usernameInvalid: true,
                        helperText: "The username does not exist"
                    })
                }
            })
            .catch(e => console.log(e))
        } else if (!this.state.usernameInvalid) {
            axios.post(`${serverURL}/user`, {
                action: "signup",
                username: this.state.username
            })
            .catch(e => console.log(e))
        }
    }

    onUsernameChange = e => {
        const newUsername = e.target.value;
        this.setState({
            username: newUsername,
            usernameInvalid: false,
            helperText: null
        })
        if (this.state.action == "Sign Up"){
            this.setState({
                usernameInvalid: newUsername.length > 30,
                helperText: newUsername.length > 30 ? "At most 30 characters" : null
            })
        }
        console.log(newUsername);
    }

    render() {
        return (
            <div style={{display: "flex", justifyContent: "center", textAlign: "center", marginTop: "20%"}}>
                <Card style={{width: "500px"}} raised>
                    <CardContent style={{display: "flex", flexDirection: "column", alignItems: "center", margin: "30px"}}>
                        <Typography variant="h3" color="textPrimary" style={{marginBottom: "20px"}}>
                            {this.state.action}
                        </Typography>
                        <Typography variant="h5" color="textSecondary" style={{marginBottom: "20px"}}>
                            Welcome to UWSchedule
                        </Typography>
                        <TextField id="user-name" label="Username" style={{marginBottom: "30px", width: "100%"}} onChange={this.onUsernameChange}
                        error={this.state.usernameInvalid} helperText={this.state.helperText}
                        />
                        {/* <TextField id="password" label="Password" style={{marginBottom: "30px", width: "100%"}}/> */}
                        <CardActions>
                            <Button variant="contained" color="primary" onClick={this.onExecuteAction}>{this.state.action}</Button>
                        </CardActions>
                        <Typography variant="h6" color="textSecondary">
                            <Link onClick={this.onToggleAction} component="button" variant="h6">
                                or {this.state.action == "Log In"? "sign up" : "log in"}
                            </Link>
                        </Typography>
                    </CardContent>
                </Card>
            </div>
        )
    }
}

export default Login;