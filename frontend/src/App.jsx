import { useEffect, useState } from "react";

import ReactMarkdown from "react-markdown";

import remarkMath from "remark-math";

import rehypeKatex from "rehype-katex";

import "katex/dist/katex.min.css";

import Auth from "./Auth";

import { supabase } from "./supabaseClient";

// ---------------------------------------------------
// BACKEND API URL
// ---------------------------------------------------

const API_BASE_URL =
  "https://chemeduai-backend.onrender.com"; 
function App() {

  // ---------------------------------------------------
  // SESSION STATE
  // ---------------------------------------------------

  const [session, setSession] = useState(null);

  // ---------------------------------------------------
  // CONTENT STATES
  // ---------------------------------------------------

  const [subject, setSubject] = useState("");

  const [chapter, setChapter] = useState("");

  const [topic, setTopic] = useState("");

  const [content, setContent] = useState("");

  const [loading, setLoading] = useState(false);

  const [tutorQuestion, setTutorQuestion] = useState("");

  const [tutorResponse, setTutorResponse] = useState("");

  const [chatMessages, setChatMessages] = useState([]);

  const [quizContent, setQuizContent] = useState("");

  const [interactiveQuiz, setInteractiveQuiz] = useState([]);

  const [quizAnswers, setQuizAnswers] = useState({});

  const [quizScore, setQuizScore] = useState(null);

  const [showQuizResults, setShowQuizResults] = useState(false);

  const [quizResults, setQuizResults] = useState([]);

  const [totalQuizzes, setTotalQuizzes] = useState(0);

  const [averageScore, setAverageScore] = useState(0);

  const [bestScore, setBestScore] = useState(0);
  
  const [strongTopics, setStrongTopics] = useState([]);

  const [weakTopics, setWeakTopics] = useState([]);

  const [recommendations, setRecommendations] = useState([]);

  const [studyPlan, setStudyPlan] = useState([]);

  


  // ---------------------------------------------------
  // HISTORY STATE
  // ---------------------------------------------------

  const [history, setHistory] = useState([]);

  // ---------------------------------------------------
  // SESSION CHECK
  // ---------------------------------------------------

  useEffect(() => {

    supabase.auth.getSession().then(({ data: { session } }) => {

      setSession(session);

      if (session) {
        fetchHistory(session);

        loadQuizProgress(session);
      }
    });

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {

      setSession(session);

      if (session) {
        fetchHistory(session);

        loadQuizProgress(session);
      }
    });

    return () => subscription.unsubscribe();

  }, []);

  // ---------------------------------------------------
  // FETCH HISTORY
  // ---------------------------------------------------

  const fetchHistory = async (currentSession = session) => {

    if (!currentSession) return;

    const { data, error } = await supabase
      .from("study_history")
      .select("*")
      .eq("user_id", currentSession.user.id)
      .order("created_at", { ascending: false });

    if (error) {

      console.log("History Fetch Error:", error.message);

    } else {

      setHistory(data);
    }
  };

  const loadQuizProgress = async (currentSession = session) => {

  if (!currentSession) return;

  try {

    const { data, error } = await supabase
      .from("quiz_results")
      .select("*")
      .eq("user_id", currentSession.user.id)
      .order("created_at", { ascending: false });

    if (error) {

      console.error(error);

      return;
    }

    setQuizResults(data || []);

    console.log("Quiz Results:", data);

    console.log("Records Count:", data.length);

    generateRecommendations(data || []);

    const total = data.length;

    setTotalQuizzes(total);

    if (total > 0) {

      const scores = data.map(
        item => (item.score / item.total_questions) * 100
      );

      const avg =
        scores.reduce((a, b) => a + b, 0) / scores.length;

      const best = Math.max(...scores);

      setAverageScore(avg.toFixed(1));

      setBestScore(best.toFixed(1));

    } else {

      setAverageScore(0);

      setBestScore(0);

    }

  } catch (err) {

    console.error(err);

  }
  
    
  function generateRecommendations(results) {

  const topicScores = {};

  results.forEach((item) => {

    const percentage =
      (item.score / item.total_questions) * 100;

    if (!topicScores[item.topic]) {

      topicScores[item.topic] = [];

    }

    topicScores[item.topic].push(
      percentage
    );

  });

  const strong = [];

  const weak = [];

  const recs = [];

  Object.keys(topicScores).forEach(
    (topic) => {

      const scores = topicScores[topic];

      const avg =
        scores.reduce(
          (a, b) => a + b,
          0
        ) / scores.length;

      if (avg >= 80) {

        strong.push(topic);

      } else if (avg < 60) {

        weak.push(topic);

        recs.push(
          `Revise topic: ${topic}`
        );

        recs.push(
          `Attempt numerical problems on ${topic}`
        );

        recs.push(
          `Ask AI Tutor questions on ${topic}`
        );

      }

    }
  );

  setStrongTopics(strong);

  setWeakTopics(weak);

  setRecommendations(recs);

  // ----------------------------------
  // GENERATE PERSONALIZED STUDY PLAN
  // ----------------------------------

  const plan = [];

  const days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
  ];

  weak.forEach((topic, index) => {

    plan.push({

      day: days[index % days.length],

      task1: `Revise ${topic}`,

      task2: `Attempt numerical problems on ${topic}`,

      task3: `Ask AI Tutor questions on ${topic}`,

    });

  });

  setStudyPlan(plan);

}

};

  // ---------------------------------------------------
  // SAVE GENERATED CONTENT
  // ---------------------------------------------------

  const saveToHistory = async (generatedContent, contentType) => {

    if (!session) return;

    const { error } = await supabase
      .from("study_history")
      .insert([
        {
          user_id: session.user.id,
          subject: subject,
          chapter: chapter,
          topic: topic,
          content: generatedContent,
          content_type: contentType,
        },
      ]);

    if (error) {

      console.log("Save Error:", error.message);

    } else {

      console.log("Saved to study history.");

      fetchHistory();
    }
  };

  // ---------------------------------------------------
  // OPEN HISTORY ITEM
  // ---------------------------------------------------

  const openHistoryItem = (item) => {

    setSubject(item.subject);

    setChapter(item.chapter);

    setTopic(item.topic);

    setContent(item.content);

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  // ---------------------------------------------------
  // DELETE HISTORY ITEM
  // ---------------------------------------------------

  // const deleteHistoryItem = async (id) => {

  //   const confirmDelete = window.confirm(
  //     "Are you sure you want to delete this study material?"
  //   );

  //   if (!confirmDelete) return;

  //   const { error } = await supabase
  //     .from("study_history")
  //     .delete()
  //     .eq("id", id);

  //   if (error) {

  //     alert("Delete failed.");

  //     console.log(error.message);

  //   } else {

  //     alert("Study material deleted successfully.");

  //     fetchHistory();
  //   }
  // };

  const deleteHistoryItem = async (id) => {

  console.log("DELETE ID:", id);

  const confirmDelete = window.confirm(
    "Are you sure you want to delete this study material?"
  );

  if (!confirmDelete) return;

  const { error } = await supabase
    .from("study_history")
    .delete()
    .eq("id", id);

  console.log("DELETE ERROR:", error);

  if (error) {

    alert("Delete failed.");

    console.log(error);

  } else {

    alert("Study material deleted successfully.");

    fetchHistory();
  }
};

  // ---------------------------------------------------
  // DOWNLOAD SAVED PDF
  // ---------------------------------------------------

  const downloadSavedPDF = async (item) => {

    try {

      const response = await fetch(
        
        `${API_BASE_URL}/download_saved_pdf`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            topic: item.topic,
            content: item.content,
          }),
        }
      );

      if (!response.ok) {

        throw new Error("PDF generation failed");
      }

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");

      a.href = url;

      a.download = `${item.topic}.pdf`;

      document.body.appendChild(a);

      a.click();

      a.remove();

      window.URL.revokeObjectURL(url);

    } catch (error) {

      console.error(error);

      alert("Saved PDF download failed.");
    }
  };

  // ---------------------------------------------------
  // LOGOUT
  // ---------------------------------------------------

  const logout = async () => {

    await supabase.auth.signOut();

    setSession(null);

    setHistory([]);
  };

  // ---------------------------------------------------
  // GENERATE TEACHING CONTENT
  // ---------------------------------------------------

  const generateContent = async () => {

    setLoading(true);

    try {

      const response = await fetch(
        
        `${API_BASE_URL}/generate`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            subject,
            chapter,
            topic,
          }),
        }
      );

      const data = await response.json();

      setContent(data.content);

      await saveToHistory(data.content, "Teaching Content");

    } catch (error) {

      setContent("Error generating teaching content.");
    }

    setLoading(false);
  };

  // ---------------------------------------------------
  // GENERATE NUMERICALS
  // ---------------------------------------------------

  const generateNumericals = async () => {

    setLoading(true);

    try {

      const response = await fetch(
        `${API_BASE_URL}/generate_numericals`,

        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            subject,
            chapter,
            topic,
          }),
        }
      );

      const data = await response.json();

      setContent(data.content);

      await saveToHistory(data.content, "Numerical Problems");

    } catch (error) {

      setContent("Error generating numericals.");
    }

    setLoading(false);
  };

  // ---------------------------------------------------
  // GENERATE EXAM QUESTIONS
  // ---------------------------------------------------

  const generateExamQuestions = async () => {

    setLoading(true);

    try {

      const response = await fetch(
        
        `${API_BASE_URL}/generate_exam_questions`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            subject,
            chapter,
            topic,
          }),
        }
      );

      const data = await response.json();

      setContent(data.content);

      await saveToHistory(data.content, "Exam Questions");

    } catch (error) {

      setContent("Error generating exam questions.");
    }

    setLoading(false);
  };

  // ---------------------------------------------------
  // GENERATE QUESTION PAPER
  // ---------------------------------------------------

  const generateQuestionPaper = async () => {

    setLoading(true);

    try {

      const response = await fetch(
        
        `${API_BASE_URL}/generate_question_paper`,
        
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            subject,
            chapter,
            topic,
          }),
        }
      );

      const data = await response.json();

      setContent(data.content);

      await saveToHistory(data.content, "Question Paper");

    } catch (error) {

      setContent("Error generating question paper.");
    }

    setLoading(false);
  };

  const askTutor = async () => {

    if (!session?.user?.id) {

      alert("Please login again.");

      return;
    }

    if (!tutorQuestion.trim()) {

      alert("Please enter a question.");

      return;
    }

  setLoading(true);

  try {

    const response = await fetch(
      
      `${API_BASE_URL}/ask_tutor`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: session.user.id,
          subject,
          chapter,
          topic,
          question: tutorQuestion,
        }),
        
      }
    );

    const data = await response.json();

    setTutorResponse(data.content);

    setChatMessages((prev) => [
    ...prev,

    {
    role: "user",
    content: tutorQuestion,
  },

  {
    role: "assistant",
    content: data.content,
  },
]);

await saveToHistory(
  data.content,
  "AI Tutor Response"
);

setTutorQuestion("");

  } catch (error) {

    console.error(error);

    setTutorResponse(
      "Error communicating with AI Tutor."
    );
  }

  setLoading(false);
};

const clearTutorChat = async () => {

  try {

    await fetch(
      
      `${API_BASE_URL}/clear_tutor_chat`,
      
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: session.user.id,
        }),
      }
    );

    setChatMessages([]);

    setTutorQuestion("");

    setTutorResponse("");

  } catch (error) {

    console.error(error);

    alert("Unable to clear tutor memory.");
  }
};

const generateQuiz = async () => {

  if (!subject || !chapter || !topic) {

    alert(
      "Please enter Subject, Chapter and Topic."
    );

    return;
  }

  setLoading(true);

  try {

    const response = await fetch(
      
      `${API_BASE_URL}/generate_quiz`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          subject,
          chapter,
          topic,
          num_questions: 10,
        }),
      }
    );

    const data = await response.json();

    setQuizContent(data.content);

  } catch (error) {

    console.error(error);

    alert("Quiz generation failed.");

  } finally {

    setLoading(false);
  }
};

const generateInteractiveQuiz = async () => {

  if (!subject || !chapter || !topic) {

    alert(
      "Please enter Subject, Chapter and Topic."
    );

    return;
  }

  setLoading(true);

  try {

    const response = await fetch(
      
      `${API_BASE_URL}/generate_interactive_quiz`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          subject,
          chapter,
          topic,
          num_questions: 10,
        }),
      }
    );

    const data = await response.json();

    setInteractiveQuiz(data);

    setQuizAnswers({});

    setQuizScore(null);

    setShowQuizResults(false);

  } catch (error) {

    console.error(error);

    alert(
      "Interactive Quiz generation failed."
    );

  } finally {

    setLoading(false);
  }
};
// ---------------------------------------------------
  // DOWNLOAD PDF
  // ---------------------------------------------------

  const downloadPDF = async () => {

    try {

      const response = await fetch(
        
        `${API_BASE_URL}/export/pdf`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            subject,
            chapter,
            topic,
          }),
        }
      );

      if (!response.ok) {

        throw new Error("PDF download failed");
      }

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");

      a.href = url;

      a.download = "study_material.pdf";

      document.body.appendChild(a);

      a.click();

      a.remove();

      window.URL.revokeObjectURL(url);

    } catch (error) {

      console.error(error);

      alert("PDF download failed.");
    }
  };

  // ---------------------------------------------------
  // DOWNLOAD PPT
  // ---------------------------------------------------

  const downloadPPT = async () => {

    try {

      const response = await fetch(
        
        `${API_BASE_URL}/export/ppt`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            subject,
            chapter,
            topic,
          }),
        }
      );

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");

      a.href = url;

      a.download = "lecture_slides.pptx";

      document.body.appendChild(a);

      a.click();

      a.remove();

      window.URL.revokeObjectURL(url);

    } catch (error) {

      alert("PPT download failed.");
    }
  };

  // ---------------------------------------------------
  // VIEW DIAGRAM
  // ---------------------------------------------------

  const viewDiagram = async () => {

    try {

      const response = await fetch(
        
        `${API_BASE_URL}/diagram`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            subject,
            chapter,
            topic,
          }),
        }
      );

      const blob = await response.blob();

      const imageUrl = URL.createObjectURL(blob);

      window.open(imageUrl, "_blank");

    } catch (error) {

      alert("Diagram generation failed.");
    }
  };

  // ---------------------------------------------------
  // SOLVE NUMERICAL
  // ---------------------------------------------------

  const solveNumerical = async () => {

    try {

      const response = await fetch(
        
        `${API_BASE_URL}/solve`,
      );

      const data = await response.json();

      setContent(data.solution);

    } catch (error) {

      setContent("Error solving numerical.");
    }
  };

  const submitQuiz = async () => {

  let score = 0;

  interactiveQuiz.forEach((question, index) => {

    if (
      quizAnswers[index] === question.answer
    ) {
      score++;
    }

  });

  setQuizScore(score);

  setShowQuizResults(true);

  try {

    const { error } = await supabase
      .from("quiz_results")
      .insert([
        {
          user_id: session.user.id,
          subject: subject,
          chapter: chapter,
          topic: topic,
          score: score,
          total_questions: interactiveQuiz.length,
        },
      ]);

    if (error) {

      console.error(error);

      alert(
        "Quiz score could not be saved."
      );

    }

  } catch (err) {

    console.error(err);

  }

};


  // ---------------------------------------------------
  // SHOW LOGIN PAGE
  // ---------------------------------------------------

  if (!session) {

    return <Auth setSession={setSession} />;
  }

  // ---------------------------------------------------
  // MAIN UI
  // ---------------------------------------------------

  return (

    <div className="min-h-screen bg-gray-100 p-6">

      {/* HEADER */}

      <div className="bg-blue-700 text-white p-5 rounded-lg shadow-lg mb-6 flex justify-between items-center">

        <div>

          <h1 className="text-3xl font-bold">
            ChemEduAI Platform
          </h1>

          <p className="mt-2">
            AI Engineering Education Platform
          </p>

        </div>

        <div className="text-right">

          <p className="mb-2 text-sm">
            {session.user.email}
          </p>

          <button
            onClick={logout}
            className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded"
          >
            Logout
          </button>

        </div>

      </div>

      {/* INPUTS */}

      <div className="bg-white p-6 rounded-lg shadow-md mb-6">

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

          <input
            type="text"
            placeholder="Subject"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            className="border p-3 rounded"
          />

          <input
            type="text"
            placeholder="Chapter"
            value={chapter}
            onChange={(e) => setChapter(e.target.value)}
            className="border p-3 rounded"
          />

          <input
            type="text"
            placeholder="Topic"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            className="border p-3 rounded"
          />

        </div>

        {/* BUTTONS */}

        <div className="flex flex-wrap gap-4 mt-6">

          <button
            onClick={generateContent}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          >
            Generate Teaching Content
          </button>

          <button
            onClick={generateNumericals}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
          >
            Generate Numerical Problems
          </button>

          <button
            onClick={generateExamQuestions}
            className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded"
          >
            Generate Exam Questions
          </button>

          <button
            onClick={generateQuestionPaper}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded"
          >
            Generate Question Paper
          </button>

          <button
            onClick={generateQuiz}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded"
          >
            Generate Quiz
          </button>

          <button
            onClick={generateInteractiveQuiz}
            className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded"
          >
            Interactive Quiz
          </button>  

          

          <button
            onClick={downloadPDF}
            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded"
          >
            Download PDF
          </button>

          <button
            onClick={downloadPPT}
            className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded"
          >
            Download PPT
          </button>

          <button
            onClick={viewDiagram}
            className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded"
          >
            View Diagram
          </button>

          <button
            onClick={solveNumerical}
            className="bg-gray-700 hover:bg-gray-800 text-white px-4 py-2 rounded"
          >
            Solve Numerical
          </button>

        </div>

      </div>

      {/* GENERATED CONTENT */}

      <div className="bg-white p-6 rounded-lg shadow-md mb-6">

        <h2 className="text-2xl font-bold mb-4">
          Generated Academic Content
        </h2>

        {loading ? (

          <p className="text-blue-600 font-semibold">
            Generating...
          </p>

        ) : (

          <div className="prose max-w-none">

            <ReactMarkdown
              remarkPlugins={[remarkMath]}
              rehypePlugins={[rehypeKatex]}
            >
              {content}
            </ReactMarkdown>

          </div>

        )}

      </div>

      <div className="bg-white p-6 rounded-lg shadow-md mb-6">

  <h2 className="text-2xl font-bold mb-4">
    Ask AI Tutor
  </h2>

  <textarea
    value={tutorQuestion}
    onChange={(e) => setTutorQuestion(e.target.value)}
    placeholder="Ask a question about the current topic..."
    className="w-full border p-3 rounded mb-4"
    rows={4}
  />

  <button
    onClick={askTutor}
    className="bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 rounded"
  >
    Ask Tutor
  </button>

  <button
  onClick={clearTutorChat}
  className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded ml-2"
>
  Clear Chat
</button>

  
  {chatMessages.length > 0 && (

  <div className="mt-8">

    <h3 className="text-xl font-semibold mb-4">
      Tutor Conversation
    </h3>

    <div
      className="border rounded-lg p-4 bg-gray-50"
      style={{
        maxHeight: "500px",
        overflowY: "auto",
      }}
    >

      {chatMessages.map((msg, index) => (

        <div
          key={index}
          className={`mb-4 p-4 rounded-lg ${
            msg.role === "user"
              ? "bg-blue-100"
              : "bg-green-100"
          }`}
        >

          <strong>

            {msg.role === "user"
              ? "Student"
              : "AI Tutor"}

          </strong>

          <div className="mt-2">

            <ReactMarkdown
              remarkPlugins={[remarkMath]}
              rehypePlugins={[rehypeKatex]}
            >
              {msg.content}
            </ReactMarkdown>

          </div>

        </div>

      ))}

    </div>

  </div>

)}

</div>

{quizContent && (

  <div className="bg-white p-6 rounded-lg shadow-md mb-6">

    <h2 className="text-2xl font-bold mb-4">
      Quiz Questions
    </h2>

    <div className="prose max-w-none">

      <ReactMarkdown
        remarkPlugins={[remarkMath]}
        rehypePlugins={[rehypeKatex]}
      >
        {quizContent}
      </ReactMarkdown>

    </div>

  </div>

)}

{interactiveQuiz.length > 0 && (

  <div className="bg-white p-6 rounded-lg shadow-md mb-6">

    <h2 className="text-2xl font-bold mb-4">
      Interactive Quiz
    </h2>

    {interactiveQuiz.map((q, index) => (

      <div
        key={index}
        className="mb-8 border-b pb-6"
      >

        <h3 className="font-semibold mb-4">

          Q{index + 1}. {q.question}

        </h3>

        {q.options.map((option, optionIndex) => (

          <label
            key={optionIndex}
            className="block mb-2"
          >

            <input
              type="radio"
              name={`question-${index}`}
              value={option}
              disabled={showQuizResults}
              checked={
                quizAnswers[index] === option
              }
              onChange={() =>
                setQuizAnswers({
                  ...quizAnswers,
                  [index]: option,
                })
              }
              className="mr-2"
            />

            {option}

          </label>

        ))}
        
    {showQuizResults && (

  <div className="mt-4 p-4 bg-gray-100 rounded">

    <p>

      <strong>Your Answer:</strong>{" "}

      {quizAnswers[index] || "Not Answered"}

    </p>

    {quizAnswers[index] === q.answer ? (

      <p className="text-green-600 font-semibold mt-2">
        ✅ Correct
      </p>

    ) : (

      <p className="text-red-600 font-semibold mt-2">
        ❌ Incorrect
      </p>

    )}

    <p className="mt-2">

      <strong>Correct Answer:</strong>{" "}

      {q.answer}

    </p>

    <div className="mt-3">

      <strong>Explanation:</strong>

      <div className="mt-2">

        <ReactMarkdown
          remarkPlugins={[remarkMath]}
          rehypePlugins={[rehypeKatex]}
        >
          {q.explanation}
        </ReactMarkdown>

      </div>

    </div>

  </div>

)}    

        

      </div>

    ))}

    <button
      onClick={submitQuiz}
      className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
    >
      Submit Quiz
    </button>

  </div>

)}

{quizScore !== null && (

  <div className="bg-green-100 p-6 rounded-lg mb-6">

    <h2 className="text-2xl font-bold">

      Score: {quizScore} / {interactiveQuiz.length}

    </h2>

  </div>

)}

<div className="bg-white p-6 rounded-lg shadow-md mb-6">

  <h2 className="text-2xl font-bold mb-4">
    Student Progress Dashboard
  </h2>

  <div className="grid grid-cols-3 gap-4 mb-6">

    <div className="bg-blue-100 p-4 rounded">

      <h3 className="font-semibold">
        Total Quizzes
      </h3>

      <p className="text-2xl">
        {totalQuizzes}
      </p>

    </div>

    <div className="bg-green-100 p-4 rounded">

      <h3 className="font-semibold">
        Average Score
      </h3>

      <p className="text-2xl">
        {averageScore}%
      </p>

    </div>

    <div className="bg-yellow-100 p-4 rounded">

      <h3 className="font-semibold">
        Best Score
      </h3>

      <p className="text-2xl">
        {bestScore}%
      </p>

    </div>

  </div>

</div>    

<div className="bg-white p-6 rounded-lg shadow-md mb-6">

  <h2 className="text-xl font-bold mb-4">
    Recent Quiz Attempts (Latest 10)
  </h2>

  {quizResults.slice(0, 10).map(
    (quiz) => (

      <div
        key={quiz.id}
        className="border-b py-3"
      >

        <p>

          <strong>
            {quiz.topic}
          </strong>

        </p>

        <p>

          Score:

          {" "}

          {quiz.score}

          /

          {quiz.total_questions}

        </p>

        <p className="text-sm text-gray-500">

          {new Date(
            quiz.created_at
          ).toLocaleString()}

        </p>

      </div>

    )
  )}

  <div className="bg-white p-6 rounded-lg shadow-md mb-6">

  <h2 className="text-2xl font-bold mb-4">
    AI Learning Recommendations
  </h2>

  <h3 className="font-semibold mb-2">
    Strong Topics
  </h3>

  <ul className="list-disc ml-6 mb-4">

    {strongTopics.map((topic, index) => (

      <li key={index}>
        {topic}
      </li>

    ))}

  </ul>

  <h3 className="font-semibold mb-2">
    Weak Topics
  </h3>

  <ul className="list-disc ml-6 mb-4">

    {weakTopics.map((topic, index) => (

      <li key={index}>
        {topic}
      </li>

    ))}

  </ul>

  <h3 className="font-semibold mb-2">
    Recommended Actions
  </h3>

  <ul className="list-disc ml-6">

    {recommendations.map((item, index) => (

      <li key={index}>
        {item}
      </li>

    ))}

  </ul>

</div>

</div>

<div className="bg-white p-6 rounded-lg shadow-md mb-6">

  <h2 className="text-2xl font-bold mb-4">
    Personalized Study Planner
  </h2>

  {studyPlan.length === 0 ? (

    <p>
      Complete more quizzes to generate a study plan.
    </p>

  ) : (

    studyPlan.map((item, index) => (

      <div
        key={index}
        className="mb-4 p-4 border rounded"
      >

        <h3 className="font-semibold text-lg">

          {item.day}

        </h3>

        <ul className="list-disc ml-6 mt-2">

          <li>{item.task1}</li>

          <li>{item.task2}</li>

          <li>{item.task3}</li>

        </ul>

      </div>

    ))

  )}

</div>


      {/* STUDY HISTORY */}

      <div className="bg-white p-6 rounded-lg shadow-md">

        <h2 className="text-2xl font-bold mb-4">
          Saved Study History
        </h2>

        {history.length === 0 ? (

          <p>No saved study history found.</p>

        ) : (

          <div className="space-y-4">

            {history.map((item) => (

              <div
                key={item.id}
                className="border rounded p-4 bg-gray-50"
              >

                <div className="flex justify-between items-center mb-2">

                  <h3 className="text-lg font-semibold">
                    {item.topic}
                  </h3>

                  <span className="text-sm text-gray-600">
                    {new Date(item.created_at).toLocaleString()}
                  </span>

                </div>

                <p className="text-sm text-blue-700 font-medium mb-2">
                  {item.content_type}
                </p>

                <p className="text-gray-700 mb-4">
                  Subject: {item.subject} | Chapter: {item.chapter}
                </p>

                {/* HISTORY ACTION BUTTONS */}

                <div className="flex flex-wrap gap-3">

                  <button
                    onClick={() => openHistoryItem(item)}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                  >
                    Open
                  </button>

                  <button
                    onClick={() => downloadSavedPDF(item)}
                    className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
                  >
                    Download PDF
                  </button>

                  <button
                    onClick={() => deleteHistoryItem(item.id)}
                    className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded"
                  >
                    Delete
                  </button>

                </div>

              </div>

            ))}

          </div>

        )}

      </div>

    </div>
  );
}

export default App;