import React, { createContext, useRef, useState } from "react";
import run from "../gemini";
import { useNavigate } from "react-router-dom";

export const datacontext = createContext();

function UserContext({ children }) {
    const isListening = useRef(false);
    const recognitionRef = useRef(null);
    const [messages, setMessages] = useState([]);
    const [status, setStatus] = useState("Idle");
    const navigate = useNavigate();

    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

    function speak(text) {
        if (isListening.current && recognitionRef.current) {
            recognitionRef.current.stop();
            setStatus("Speaking");
        }

        const text_speak = new SpeechSynthesisUtterance(text);
        text_speak.volume = 1;
        text_speak.rate = 1;
        text_speak.pitch = 1;
        text_speak.lang = "en-GB";

        text_speak.onend = () => {
            if (isListening.current && recognitionRef.current) {
                recognitionRef.current.start();
                setStatus("Listening");
            } else {
                setStatus("Idle");
            }
        };

        window.speechSynthesis.speak(text_speak);
    }

    async function aiResponse(prompt) {
        setMessages(prev => [...prev, { sender: "Patient", text: prompt }]);

        const text = await run(prompt);
        let cleanedText = text.replace(/^Agent:\s*/i, "").trim();

        setMessages(prev => [...prev, { sender: "Assistant", text: cleanedText }]);
        speak(cleanedText);
    }

    if (!recognitionRef.current) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = "en-US";

        recognition.onstart = () => {
            setStatus("Listening");
            console.log("Recognition started");
        };

        recognition.onresult = (e) => {
            const currentIndex = e.resultIndex;
            const transcript = e.results[currentIndex][0].transcript;
            console.log("Patient said:", transcript);
            aiResponse(transcript);
        };

        recognition.onend = () => {
            console.log("Recognition ended");
            if (isListening.current) {
                recognition.start();
            } else {
                setStatus("Idle");
            }
        };

        recognition.onerror = (e) => {
            console.error("Recognition error:", e.error);
            setStatus("Idle");
        };

        recognitionRef.current = recognition;
    }

    function connect() {
        isListening.current = true;
        recognitionRef.current.start();
        console.log("Mic started");
    }

    async function disconnect() {
        isListening.current = false;
        recognitionRef.current.stop();
        window.speechSynthesis.cancel();
        setStatus("Idle");
        console.log("Mic stopped");

        console.log("Full Conversation:");
        messages.forEach((msg, index) => {
            console.log(`${index + 1}. ${msg.sender}: ${msg.text}`);
        });

        const patientMessages = messages
            .filter(msg => msg.sender === "Patient")
            .map(msg => msg.text)
            .join(" ");

        const symptomPhrases = patientMessages
            .split(/[.?!]/)
            .map(s => s.trim())
            .filter(Boolean);

        console.log("Extracted Phrases:", symptomPhrases);

        try {
            console.log("Sending phrases to LangGraph:", symptomPhrases);
            const response = await fetch(`${BACKEND_URL}/run_langgraph`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ phrases: symptomPhrases }),
            });

            const data = await response.json();
            console.log("Received LangGraph response:", data);
            navigate("/recommendation", { state: data });

        } catch (error) {
            console.error("Error during LangGraph execution:", error);
        }
    }

    const value = {
        connect,
        disconnect,
        messages,
        status,
    };

    return (
        <datacontext.Provider value={value}>
            {children}
        </datacontext.Provider>
    );
}

export default UserContext;
