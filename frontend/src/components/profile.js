import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Drawer } from '@material-ui/core';
import { useHistory } from "react-router-dom";

const useStyles = makeStyles(theme => ({
  list: {
    marginTop: theme.spacing(2),
  },
}));

function Profile() {
  const classes = useStyles();

  return (
    <div>
      profile page
    </div>
  )
}

export default Profile;