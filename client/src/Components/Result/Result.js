import React, { useEffect, useState } from "react";
import Axios from "axios";
import CircularProgress from "@material-ui/core/CircularProgress";
import "./Result.css";
import PieChart from "../PieChart/PieChart.js";
import PersonalityCard from "../PersonalityCard/PersonalityCard.js";
import DataTable from "../Table/Table.js";

const Result = ({ endpoint, data }) => {
  const [fetched_data, setFetchedData] = useState({
    hatespeechCount: -1,
    personality: "",
    tweets: []
  });
  const [hateSpeechTweets, setHateSpeechTweets] = useState([]);
  console.log("Ress ", fetched_data, hateSpeechTweets);
  useEffect(() => {
    async function getTwitterAnalysis(data) {
      console.log("Twitter Data fetching for", data);
      if (data.username) {
        console.log("Started Fetchinng... ");
        const url =
          endpoint +
          "/checkuser" +
          "?username=" +
          data.username +
          "&tweets=" +
          data.tweets +
          "&replies=" +
          data.replies;
        console.log(url);
        const val = await Axios.get(url);
        setFetchedData(val["data"]);
      } else console.log("");
    }

    getTwitterAnalysis(data);
  }, [data]);

  return fetched_data.hatespeechCount == -1 ? (
    <div className="result_outer">
      <div className="loading">
        <center>
          <CircularProgress />
          <span className="loading_info">Fetching Information .....</span>
        </center>
      </div>
    </div>
  ) : (
    <div className="result_outer">
      <div className="result_info">
        <div className="result_hate_speech">
          <div className="pie_chart_div">
            <PieChart
              total_hate_speech={fetched_data.hatespeechCount}
              total_tweets={fetched_data.tweets.length}
            />
          </div>
          <div className="hate_speech_info_div">
            <span>
              {"HateSpeech Tweets Found :" + fetched_data.hatespeechCount}
            </span>
            <span>
              {"Total Tweets Analysed : " + fetched_data.tweets.length}
            </span>
          </div>
        </div>
        <div className="result_personality">
          <div className="personality_card">
            <PersonalityCard type={fetched_data.personality} />
          </div>
        </div>
      </div>

      <div className="hate_speech_table_div">
        <DataTable data={fetched_data.tweets} />
      </div>
    </div>
  );
};

export default Result;
