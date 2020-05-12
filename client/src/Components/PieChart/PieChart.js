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
    // const chartInfo={
    //     title: "Users by device",
    // chartData: {
    //   datasets: [
    //     {
    //       hoverBorderColor: "#ffffff",
    //       data: [68.3, 24.2, 7.5],
    //       backgroundColor: [
    //         "rgba(0,123,255,0.9)",
    //         "rgba(0,123,255,0.5)",
    //         "rgba(0,123,255,0.3)"
    //       ]
    //     }
    //   ],
    //   labels: ["Desktop", "Tablet", "Mobile"]
    // }
    // }
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
  });

  return <canvas height="120" ref={canvasRef} className="pie_chart" />;
};

// UsersByDevice.propTypes = {
//   /**
//    * The component's title.
//    */
//   title: PropTypes.string,
//   /**
//    * The chart config object.
//    */
//   chartConfig: PropTypes.object,
//   /**
//    * The Chart.js options.
//    */
//   chartOptions: PropTypes.object,
//   /**
//    * The chart data.
//    */
//   chartData: PropTypes.object
// };

// UsersByDevice.defaultProps = {
//   title: "Users by device",
//   chartData: {
//     datasets: [
//       {
//         hoverBorderColor: "#ffffff",
//         data: [68.3, 24.2, 7.5],
//         backgroundColor: [
//           "rgba(0,123,255,0.9)",
//           "rgba(0,123,255,0.5)",
//           "rgba(0,123,255,0.3)"
//         ]
//       }
//     ],
//     labels: ["Desktop", "Tablet", "Mobile"]
//   }
// };

export default PieChart;
