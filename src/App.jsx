import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import axios from 'axios';
import React, { useRef } from 'react';
import { useEffect } from 'react';

import './App.css'

function App() {
  const [videoFile, setVideoFile] = useState(null);
  const [playvideo, setPlayVideo] = useState(null);
  const [transcription, setTranscription] = useState('');

  const handleFileChange = (event) => {
    setVideoFile(event.target.files[0]);
    setPlayVideo(URL.createObjectURL(event.target.files[0]));
    console.log(URL.createObjectURL(event.target.files[0]));
    
 
    console.log(event.target.files[0]);
  };

  const transcribeVideo = async () => {
    try {
      const formData = {'video_path' : videoFile.name};
      

      const response = await axios.post('http://127.0.0.1:5000/transcribe_video', formData);

      setTranscription(response.data);
    } catch (error) {
      console.error('Error transcribing video:', error);
    }
  };

  const [quizData, setQuizData] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedOption, setSelectedOption] = useState('');
  const [score, setScore] = useState(0);

  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/get_current_question');
        setQuizData(response.data[0]);
        console.log(response.data[0]);
        setCurrentQuestion(0);
        setSelectedOption('');
        setScore(0);
      } catch (error) {
        console.error('Failed to fetch quiz:', error);
      }
    };

    fetchQuiz();

    const interval = setInterval(() => {
      fetchQuiz();
    }, 60000); // Fetch quiz every 2 minutes

    return () => {
      clearInterval(interval);
    };
  }, []);

  const handleOptionSelect = (option) => {
    setSelectedOption(option);
  };

  const handleNextQuestion = () => {
    if (selectedOption === quizData[currentQuestion].answer) {
      setScore(score + 1);
    }
    setSelectedOption('');
    setCurrentQuestion(currentQuestion + 1);
  };


  const [notes, setnotes] = useState(null);

  const getnotes = () => {
    axios.get('http://127.0.0.1:5000/summarize_text_with_bullets')
      .then(response => setnotes(response.data))
      .catch(error => console.error('Error:', error));
  };

  const [flowchart, setflowchart] = useState(null);
  
  const getflowchart = () => {
    axios.get('http://127.0.0.1:5000/generate_flowchart')
      .then(response => setflowchart(response.data))
      .catch(error => console.error('Error:', error));
  };


  return (
    <div>

      <h1>Transcribe Video</h1>
      <input type="file" onChange={handleFileChange}/>
      <h2>Video Player</h2>
      <video src={playvideo} width="800" height="400" controls />
      <br />
      <button onClick={transcribeVideo}>Transcribe</button>
      {console.log(quizData)}
      {quizData.length > 0 && currentQuestion < quizData.length ? (
        <div>
          <h2>{quizData[currentQuestion].question}</h2>
          <ul>
            {quizData[currentQuestion].options.map((option, index) => (
              <li key={index}>
                <label>
                  <input
                    type="radio"
                    name="option"
                    value={option}
                    checked={selectedOption === option}
                    onChange={() => handleOptionSelect(option)}
                  />
                  {option}
                </label>
              </li>
            ))}
          </ul>
          <button onClick={handleNextQuestion} disabled={!selectedOption}>
            Next
          </button>
        </div>
      ) : (
        <div>
          <h2>Quiz Completed!</h2>
          <p>Your Score: {score}/{quizData.length}</p>
          <h3>Correct Answers:</h3>
          <ul>
            {quizData.map((question, index) => (
              <li key={index}>
                <strong>Question:</strong> {question.question}
                <br />
                <strong>Correct Answer:</strong> {question.answer}
              </li>
            ))}
          </ul>
        </div>
      )}
      <br />
      <button onClick={getnotes}>Get Notes</button>
      {notes && <pre>{JSON.stringify(notes, null, 2)}</pre>}

      <br />
      <br />
      <button onClick={getflowchart}>Get Flow Chart</button>
      {flowchart && <pre>{JSON.stringify(flowchart, null, 2)}</pre>}


    </div>
  );

}

export default App
