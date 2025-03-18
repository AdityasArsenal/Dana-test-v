"use client"

import { useState } from "react"

export default function StreamlitEmbed() {
  const [isLoading, setIsLoading] = useState(true)

  // In a real implementation, this would be the URL to your deployed Streamlit app
  const streamlitAppUrl = "http://localhost:8501"

  return (
    <div className="w-full h-[650px] bg-background relative rounded-lg overflow-hidden shadow-xl border border-border">
      {/* This would be replaced with an actual iframe to your deployed Streamlit app */}
      <iframe 
        src={streamlitAppUrl}
        width="100%"
        height="100%"
        frameBorder="0"
        allow="camera; microphone; autoplay; encrypted-media; fullscreen; display-capture"
        className={`transition-opacity duration-500 ${isLoading ? "opacity-0" : "opacity-100"}`}
        onLoad={() => setIsLoading(false)}
      />

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