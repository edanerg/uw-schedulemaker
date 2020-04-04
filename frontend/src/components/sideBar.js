import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Drawer,
         List,
         ListItem,
         Typography,
         ListSubheader
        } from '@material-ui/core';
import { useHistory } from "react-router-dom";

const useStyles = makeStyles(theme => ({
  list: {
    marginTop: theme.spacing(2),
  },
}));

function SideBar({ open, setOpen }: props) {
  const classes = useStyles();
  const history = useHistory();

  function handleRouteChange(route) {
    history.push(`/${route}`);
    setOpen(false);
  }

  return (
    <Drawer open={open} onClose={() => setOpen(false)}>
      <List className={classes.list} subheader={<ListSubheader>Menu</ListSubheader>}>
        <ListItem button onClick={() => handleRouteChange('')}>
          <Typography variant="h6">
              Main page
          </Typography>
        </ListItem>
        <ListItem button onClick={() => handleRouteChange('class')}>
          <Typography variant="h6">
              View Classes
          </Typography>
        </ListItem>
        <ListItem button onClick={() => handleRouteChange('courses')}>
          <Typography variant="h6">
              View Courses
          </Typography>
        </ListItem>
        <ListItem button onClick={() => handleRouteChange('instructor')}>
          <Typography variant="h6">
              Search Classes by Instructor
          </Typography>
        </ListItem>
        <ListItem button onClick={() => handleRouteChange('profile')}>
          <Typography variant="h6">
              Profile
          </Typography>
        </ListItem>
      </List>
    </Drawer>
  )
}

export default SideBar;