import React, { useEffect } from "react";
import PropTypes from "prop-types";
import {
  Row,
  Col,
  FormSelect,
  Card,
  CardHeader,
  CardBody,
  CardFooter
} from "shards-react";

// import Chart from "../../utils/chart";
import Chart from "./utils/chart.js";

const PieChart = ({ total_hate_speech, total_tweets }) => {
  console.log("hello pie", total_hate_speech, total_tweets);
  const canvasRef = React.createRef();
  const title = "Hello";

  useEffect(() => {
    const chartConfig = {
      type: "pie",
      data: {
        datasets: [
          {
            hoverBorderColor: "#ffffff",
            data: [total_hate_speech, total_tweets],
            backgroundColor: ["rgba(0,123,255,0.9)", "rgba(0,123,255,0.5)"]
          }
        ],
        labels: ["Hate Speech", "Tweets"]
      },
      options: {
        legend: {
          position: "bottom",
          labels: {
            padding: 25,
            boxWidth: 20
          }
        },
        cutoutPercentage: 0,
        tooltips: {
          custom: false,
          mode: "index",
          position: "nearest"
        }
      }
    };

    new Chart(canvasRef.current, chartConfig);
  }, [total_hate_speech, total_tweets]);

  return <canvas height="120" ref={canvasRef} className="pie_chart" />;
};

export default PieChart;
