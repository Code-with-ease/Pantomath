import React, { useEffect, useState } from "react";
import { withStyles, makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";

const StyledTableCell = withStyles(theme => ({
  head: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white
  },
  body: {
    fontSize: 14
  }
}))(TableCell);

const StyledTableRow = withStyles(theme => ({
  root: {
    "&:nth-of-type(odd)": {
      backgroundColor: theme.palette.action.hover
    }
  }
}))(TableRow);

const useStyles = makeStyles({
  table: {
    width: "100%"
  }
});

const DataTable = ({ data }) => {
  const classes = useStyles();

  const [tdata, setTdata] = useState([]);
  useState(() => {
    var hate_speech_arr = [];
    if (data.length) {
      data.forEach(obj => {
        console.log(obj);
        if (obj.isHateSpeech == 1) hate_speech_arr.push(obj.text);
      });
      setTdata(hate_speech_arr);
    }
  }, [data]);

  return tdata.length ? (
    <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="customized table">
        <TableHead>
          <TableRow>
            <StyledTableCell align="right">{"Sno"}</StyledTableCell>
            <StyledTableCell align="right">
              {"Potential Hate Speech Tweet"}
            </StyledTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {tdata.map((row, idx) => (
            <StyledTableRow key={idx}>
              <StyledTableCell align="right">{idx}</StyledTableCell>
              <StyledTableCell align="right">{row}</StyledTableCell>
            </StyledTableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  ) : (
    ""
  );
};

export default DataTable;
