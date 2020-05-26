import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Input from "@material-ui/core/Input";
import InputLabel from "@material-ui/core/InputLabel";
import InputAdornment from "@material-ui/core/InputAdornment";
import FormControl from "@material-ui/core/FormControl";
import TextField from "@material-ui/core/TextField";
import Grid from "@material-ui/core/Grid";
import AccountCircle from "@material-ui/icons/AccountCircle";
import { func } from "prop-types";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import Icon from "@material-ui/core/Icon";
import SaveIcon from "@material-ui/icons/Save";
import Button from "@material-ui/core/Button";

import "./TwitterForm.css";
import { stat } from "fs";
const useStyles = makeStyles(theme => ({
  margin: {
    margin: theme.spacing(1)
  }
}));

const TwitterForm = ({ submit_func }) => {
  const classes = useStyles();
  const [state, setState] = React.useState({
    tweets: true,
    retweets: false
  });

  console.log(state);
  function handleCheckChange(event) {
    setState({ ...state, [event.target.name]: event.target.checked });
  }

  function HandleFormSubmit(e) {
    e.preventDefault();
    var data = {};
    data["username"] = e.target[0].value;
    data["tweets"] = state.tweets;
    data["retweets"] = state.retweets;
    submit_func(data);
  }
  return (
    <div>
      <form className="form_main" onSubmit={HandleFormSubmit}>
        <div className="form_search_bar">
          <Grid container spacing={1} alignItems="flex-end">
            <Grid item>
              <AccountCircle />
            </Grid>
            <Grid item>
              <TextField id="input-with-icon-grid" label="Twitter Handle" />
            </Grid>
          </Grid>
        </div>
        <div className="form_check_boxes">
          <FormControlLabel
            control={
              <Checkbox
                checked={state.tweets}
                onChange={handleCheckChange}
                name="tweets"
                color="primary"
              />
            }
            label="Tweets"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={state.retweets}
                onChange={handleCheckChange}
                name="retweets"
                color="primary"
              />
            }
            label="Retweets"
          />
        </div>
        <Button
          type="submit"
          className={"submit_bttn"}
          variant="contained"
          color="primary"
        >
          Search
        </Button>
        {/* <input type="submit" value="submit" /> */}
      </form>
    </div>
  );
};

export default TwitterForm;
