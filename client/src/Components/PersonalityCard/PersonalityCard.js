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
    maxWidth: 445,
    "margin-left": "30px"
  },
  media: {
    height: 140
  }
});

const PersonalityCard = ({ type }) => {
  const classes = useStyles();

  function get_full_form(type) {
    var ans = "";
    for (var i = 0; i < 4; i++) {
      var text = type[i];

      switch (text) {
        case "I":
          ans = ans + "INTROVERT";
          break;
        case "E":
          ans = ans + "EXTROVERT";
          break;
        case "N":
          ans = ans + "INTUTIVE";
          break;
        case "S":
          ans = ans + "SENSING";
          break;
        case "T":
          ans = ans + "THINKING";
          break;
        case "J":
          ans = ans + "JUDGING";
          break;
        case "F":
          ans = ans + "FEELING";
          break;
        case "P":
          ans = ans + "PERCEIVING";
          break;

        default:
          ans = ans + "";
          break;
      }
      ans = ans + " ";
    }
    return ans;
  }
  return (
    <Card className={classes.root}>
      <CardContent>
        <Typography gutterBottom variant="h5" component="h2">
          {type}
        </Typography>
        <Typography variant="body2" color="textSecondary" component="p">
          {get_full_form(type)}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default PersonalityCard;
