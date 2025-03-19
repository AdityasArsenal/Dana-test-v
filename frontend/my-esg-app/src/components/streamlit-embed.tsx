"use client"

import { useState, useEffect } from "react"

export default function StreamlitEmbed() {
  const [isLoading, setIsLoading] = useState(true)
  const [streamlitUrl, setStreamlitUrl] = useState("")

  // Initialize the Streamlit URL after component mounts
  useEffect(() => {
    // Set the URL after a short delay to ensure component is fully mounted
    const timer = setTimeout(() => {
      setStreamlitUrl(process.env.NEXT_PUBLIC_STREAMLIT_URL || "http://localhost:8501")
      // Force a rerender after setting the URL
      setIsLoading(true)
      
      // Give some time for iframe to start loading
      setTimeout(() => {
        setIsLoading(false)
      }, 500)
    }, 100)
    
    return () => clearTimeout(timer)
  }, [])

  // Handle iframe load event
  const handleIframeLoad = () => {
    setIsLoading(false)
  }

  return (
    <div className="w-full h-[650px] bg-background relative rounded-lg overflow-hidden shadow-xl border border-border">
      {streamlitUrl && (
        <iframe 
          src={streamlitUrl}
          width="100%"
          height="100%"
          frameBorder="0"
          allow="camera; microphone; autoplay; encrypted-media; fullscreen; display-capture"
          className={`transition-opacity duration-500 ${isLoading ? "opacity-0" : "opacity-100"}`}
          onLoad={handleIframeLoad}
        />
      )}

      {isLoading && (
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-card">
          <div className="mb-4 w-16 h-16 relative">
            <div className="absolute w-full h-full border-4 border-primary/30 rounded-full"></div>
            <div className="absolute w-full h-full border-t-4 border-primary rounded-full animate-spin"></div>
          </div>
          <div className="text-muted-foreground">Loading ESG Consultant...</div>
        </div>
      )}
    </div>
  )
}

// "use client"

// import { useState, useEffect } from "react"

// export default function StreamlitEmbed() {
//   const [isLoading, setIsLoading] = useState(true)
//   const [streamlitUrl, setStreamlitUrl] = useState("")

//   // Predefined questions
//   const questions = [
//     "What are the key sustainability initiatives undertaken by HPCL and IOCL?",
//     "How do HPCL and IOCL approach carbon emissions reduction in their sustainability reports?",
//     "What ESG risks are highlighted in the BRSR reports of HPCL and IOCL?",
//     "How does the water consumption strategy of HPCL compare to that of IOCL?",
//     "What are the social responsibility initiatives mentioned in the XBSR reports of HPCL and IOCL?"
//   ]

//   // Initialize the Streamlit URL after component mounts
//   useEffect(() => {
//     // Set the URL after a short delay to ensure component is fully mounted
//     const timer = setTimeout(() => {
//       setStreamlitUrl("http://localhost:8501/")
      
//       // Give some time for iframe to start loading
//       setTimeout(() => {
//         setIsLoading(false)
//       }, 500)
//     }, 100)
    
//     return () => clearTimeout(timer)
//   }, [])

//   // Handle iframe load event
//   const handleIframeLoad = () => {
//     setIsLoading(false)
//   }

//   // Function to send a question to the Streamlit app
//   const sendQuestion = (question: string) => {
//     // Using postMessage to communicate with the iframe
//     // This is the safe cross-origin way to communicate
//     const iframe = document.querySelector('iframe');
//     if (iframe && iframe.contentWindow) {
//       iframe.contentWindow.postMessage({
//         type: "streamlit:message",
//         question: question
//       }, "*");
//     }
//   }

//   return (
//     <div className="space-y-6">
//       {/* Question suggestions */}
//       <div className="bg-card/50 backdrop-blur-sm rounded-lg p-6 border border-border shadow-sm">
//         <h3 className="text-lg font-medium mb-4">Suggested Questions</h3>
//         <div className="space-y-3">
//           {questions.map((question, index) => (
//             <button
//               key={index}
//               onClick={() => sendQuestion(question)}
//               className="w-full text-left p-3 rounded-md bg-muted hover:bg-primary/10 hover:text-primary transition-colors text-sm border border-border/50 hover:border-primary/30"
//             >
//               {question}
//             </button>
//           ))}
//         </div>
//       </div>
      
//       {/* Streamlit embed */}
//       <div className="w-full h-[650px] bg-background relative rounded-lg overflow-hidden shadow-xl border border-border">
//         {streamlitUrl && (
//           <iframe 
//             src={streamlitUrl}
//             width="100%"
//             height="100%"
//             frameBorder="0"
//             allow="camera; microphone; autoplay; encrypted-media; fullscreen; display-capture"
//             className={`transition-opacity duration-500 ${isLoading ? "opacity-0" : "opacity-100"}`}
//             onLoad={handleIframeLoad}
//           />
//         )}

//         {isLoading && (
//           <div className="absolute inset-0 flex flex-col items-center justify-center bg-card">
//             <div className="mb-4 w-16 h-16 relative">
//               <div className="absolute w-full h-full border-4 border-primary/30 rounded-full"></div>
//               <div className="absolute w-full h-full border-t-4 border-primary rounded-full animate-spin"></div>
//             </div>
//             <div className="text-muted-foreground">Loading ESG Consultant...</div>
//           </div>
//         )}
//       </div>
//     </div>
//   )
// }

//Grok

// "use client"

// import { useState } from "react"

// export default function StreamlitEmbed() {
//   const [isLoading, setIsLoading] = useState(true)

//   // In a real implementation, this would be the URL to your deployed Streamlit app
//   const streamlitAppUrl = "http://localhost:8501"

//   return (
//     <div className="w-full h-[600px] bg-gray-800 relative">
//       <iframe 
//         src={streamlitAppUrl}
//         width="100%"
//         height="100%"
//         frameBorder="0"
//         allow="camera; microphone; autoplay; encrypted-media; fullscreen; display-capture"
//         className={isLoading ? "opacity-0" : "opacity-100 transition-opacity duration-300"}
//         onLoad={() => setIsLoading(false)}
//       />

//       {isLoading && (
//         <div className="absolute inset-0 flex items-center justify-center bg-gray-800">
//           <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
//         </div>
//       )}
//     </div>
//   )
// }