"use client"

import { useState } from "react"

export default function StreamlitEmbed() {
  const [isLoading, setIsLoading] = useState(true)

  // In a real implementation, this would be the URL to your deployed Streamlit app
  const streamlitAppUrl = "http://localhost:8501"

  // For the purpose of this demo, we'll create a placeholder that simulates
  // the Streamlit chat interface described in the requirements

  return (
    <div className="w-full h-[600px] bg-background relative">
      {/* This would be replaced with an actual iframe to your deployed Streamlit app */}
      <iframe 
        src={streamlitAppUrl}
        width="100%"
        height="100%"
        frameBorder="0"
        allow="camera; microphone; autoplay; encrypted-media; fullscreen; display-capture"
        className={isLoading ? "opacity-0" : "opacity-100 transition-opacity duration-300"}
        onLoad={() => setIsLoading(false)}
      />

      {/* <div className="p-6 h-full flex flex-col">
        <div className="text-2xl font-bold mb-4">AI Chat Interface</div>

        <div className="flex-1 overflow-y-auto mb-4 space-y-4 border border-border rounded-md p-4 bg-card/50">
          <div className="flex items-start gap-3">
            <div className="bg-primary text-primary-foreground rounded-full w-8 h-8 flex items-center justify-center text-sm">
              AI
            </div>
            <div className="bg-muted p-3 rounded-lg max-w-[80%]">
              <p>Hello! I'm your ESG Consultant Companion. How can I help you with your ESG strategy today?</p>
            </div>
          </div>

          <div className="flex items-start gap-3 justify-end">
            <div className="bg-primary p-3 rounded-lg max-w-[80%] text-primary-foreground">
              <p>What are the key metrics for measuring environmental impact?</p>
            </div>
            <div className="bg-secondary text-secondary-foreground rounded-full w-8 h-8 flex items-center justify-center text-sm">
              You
            </div>
          </div>

          <div className="flex items-start gap-3">
            <div className="bg-primary text-primary-foreground rounded-full w-8 h-8 flex items-center justify-center text-sm">
              AI
            </div>
            <div className="bg-muted p-3 rounded-lg max-w-[80%]">
              <p>Great question! Key environmental impact metrics include:</p>
              <ul className="list-disc pl-5 mt-2">
                <li>Carbon footprint (Scope 1, 2, and 3 emissions)</li>
                <li>Energy consumption and renewable energy usage</li>
                <li>Water usage and efficiency</li>
                <li>Waste generation and recycling rates</li>
                <li>Resource efficiency and circular economy metrics</li>
              </ul>
              <p className="mt-2">
                Would you like me to elaborate on any specific metric or suggest how to implement measurement systems
                for these?
              </p>
            </div>
          </div>
        </div>

        <div className="relative">
          <input
            type="text"
            placeholder="Enter your message here"
            className="w-full p-3 pr-12 rounded-md border border-input bg-background"
          />
          <button className="absolute right-3 top-1/2 -translate-y-1/2 text-primary">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="lucide lucide-send"
            >
              <path d="m22 2-7 20-4-9-9-4Z" />
              <path d="M22 2 11 13" />
            </svg>
          </button>
        </div>
      </div> */}

      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-background">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      )}
    </div>
  )
}

