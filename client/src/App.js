import React, { useEffect, useState } from "react";
import TwitterForm from "./Components/TwitterForm/TwitterForm.js";
import icon from "./icons/pantomath_icon.png";
import Result from "./Components/Result/Result.js";

import "./App.css";

const endpoint = "http://localhost:8000";
const App = () => {
  const [formData, setFormData] = useState({
    username: "",
    tweets: false,
    replies: false
  });

  function getTwitterFromData(data) {
    setFormData(data);
  }
  return formData.username == "" ? (
    <div className="App_outer">
      <div className="icon_div">
        <img className="pantomath_icon" src={icon} alt="Logo" />
      </div>
      <div className="app_twitter_form">
        <TwitterForm submit_func={getTwitterFromData} />
      </div>
    </div>
  ) : (
    <div className="App_outer">
      <div className="icon_div">
        <img className="pantomath_icon" src={icon} alt="Logo" />
      </div>
      <div className="app_twitter_form">
        <TwitterForm submit_func={getTwitterFromData} />
      </div>
      <div className="result_area">
        <Result endpoint={endpoint} data={formData} />
      </div>
      </div>
  );
};

export default App;
