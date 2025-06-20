import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({
  apiKey: import.meta.env.VITE_GEMINI_API_KEY,
});


// Initialize a conversation history
let conversationHistory = [];

async function run(prompt) {
  // Add the current user message to the conversation history
  conversationHistory.push(`User: ${prompt}`);
  
  const response = await ai.models.generateContent({
    model: "gemini-2.0-flash",
    contents: conversationHistory.join('\n'), // Include the full conversation history
    config: {
      systemInstruction: "You are a helpful AI Medical Assistant. Your job is to ask follow-up questions one at a time to gather the patient's symptoms." +
"Wait for the patient's response before asking the next question. Do not ask multiple questions together." +
"Do not decide or mention any medical specialist. Do not include any tags or hidden signals." +
"Once you are confident you have collected all symptoms, say: 'I have thoroughly examined your symptoms. Now you can click on disconnect.'",
    },
  });
  
  // Log the response for debugging
  console.log(response);

  // Extract the generated text from the response
  const generatedText = response?.candidates?.[0]?.content?.parts?.[0]?.text || "No response available";
  
  // Add the agent's response to the conversation history
  conversationHistory.push(`Agent: ${generatedText}`);
  
  return generatedText;
}

export default run;
