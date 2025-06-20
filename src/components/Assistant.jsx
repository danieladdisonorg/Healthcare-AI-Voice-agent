import { useState, useRef, useContext } from "react";
import "./Assistant.css";
import RecordRTC from "recordrtc";
import va from "../assets/assistant.jpg"
import { datacontext } from "../context/UserContext";

export default function Assistant() {
  //let {recognition}=useContext(datacontext)
  const {connect, disconnect, messages}=useContext(datacontext)
  
  

  return (
    <div className="assistant-wrapper">
      <div className="left-panel">
        <div className="assistant-header">🩺 AI Medical Assistant</div>
        
        <div className="assistant-chat">
          <img
            src={va}
            alt="Medical Assistant"
            className="assistant-image"
          />
        </div>

        <div className="assistant-footer">
          <button onClick={connect} className="btn-connect">Connect</button>
          <button onClick={disconnect} className="btn-disconnect">Disconnect</button>
        </div>
      </div>

      {/* Message Section */}
      <div className="right-panel">
        <div className="messages-container">
          {messages.length > 0 ? (
            messages.map((message, index) => (
              <div key={index} className={`message ${message.sender.toLowerCase()}`}>
                <strong>{message.sender}: </strong>
                <span>{message.text}</span>
              </div>
            ))
          ) : (
            <p>No messages yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}
