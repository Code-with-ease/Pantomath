import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardActionArea from "@material-ui/core/CardActionArea";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import CardMedia from "@material-ui/core/CardMedia";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";

const useStyles = makeStyles({
  root: {
    maxWidth: 345,
    "margin-left": "30px"
  },
  media: {
    height: 140
  }
});

const PersonalityCard = ({ type }) => {
  const classes = useStyles();
  const information_type = {
    INTJ: "INTROVERT , "
  };

  return (
    <Card className={classes.root}>
      <CardContent>
        <Typography gutterBottom variant="h5" component="h2">
          {type}
        </Typography>
        <Typography variant="body2" color="textSecondary" component="p">
          {"The Person is identified to be " + "BLA BLA BLA"}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default PersonalityCard;
