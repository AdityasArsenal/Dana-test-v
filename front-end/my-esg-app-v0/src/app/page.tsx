import Image from "next/image"
import { Button } from "@/components/ui/button"
import StreamlitEmbed from "@/components/streamlit-embed"
import Navbar from "@/components/navbar"
import Footer from "@/components/footer"

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <div className="fixed inset-0 -z-10">
        <Image
          src="/placeholder.svg?height=1080&width=1920"
          alt="Background texture"
          fill
          className="object-cover opacity-5"
          priority
        />
        <div className="absolute inset-0 bg-gradient-to-b from-background/95 to-background" />
      </div>

      <Navbar />

      <main className="flex-1 container mx-auto px-4 py-8">
        {/* Hero Section */}
        <section className="py-20 md:py-28 text-center md:text-left md:flex md:items-center md:justify-between max-w-6xl mx-auto">
          <div className="md:max-w-2xl space-y-5">
            <div className="inline-block px-3 py-1 bg-primary/5 text-primary rounded-full font-medium text-sm mb-3">
              AI-Powered ESG Guidance
            </div>
            <h1 className="text-3xl md:text-5xl font-bold tracking-tight">
              Your Intelligent <span className="gradient-text">ESG Consultant</span> Companion
            </h1>
            <p className="text-lg text-muted-foreground max-w-xl mx-auto md:mx-0">
              Transform your sustainability strategy with AI-powered insights tailored to your organization's needs
            </p>
            <div className="flex flex-col sm:flex-row justify-center md:justify-start gap-3 pt-3">
              <Button size="md" className="shadow-primary/10 shadow-lg">
                Start Consulting
              </Button>
              <Button size="md" variant="outline">
                View Demo
              </Button>
            </div>
          </div>
          <div className="hidden md:block relative h-64 w-64 mt-8 md:mt-0">
            <div className="absolute inset-0 bg-gradient-to-r from-primary to-orange-400 rounded-full opacity-10 blur-3xl"></div>
            <div className="relative z-10 flex items-center justify-center h-full">
              <div className="rounded-3xl overflow-hidden border border-primary/10 shadow-xl">
                <svg width="250" height="250" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="40" fill="url(#grad)" />
                  <path d="M35,35 Q50,20 65,35 Q80,50 65,65 Q50,80 35,65 Q20,50 35,35" fill="#ffffff" fillOpacity="0.2" />
                  <text x="50" y="55" textAnchor="middle" fill="white" fontWeight="bold" fontSize="12">ESG</text>
                  <defs>
                    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#ff5722" />
                      <stop offset="100%" stopColor="#ff9800" />
                    </linearGradient>
                  </defs>
                </svg>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-16 max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-2xl font-bold mb-3">Why Choose Our ESG Consultant?</h2>
            <p className="text-muted-foreground max-w-xl mx-auto text-sm">
              Our platform offers comprehensive guidance on environmental, social and governance aspects of your business.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-card/30 backdrop-blur-sm rounded-lg p-5 border-[0.5px] border-border/30 shadow-sm hover:shadow-md transition-shadow">
              <div className="h-10 w-10 rounded-full bg-primary/5 flex items-center justify-center mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="text-primary">
                  <path d="M7 20h10"></path><path d="M10 20c5.5-2.5.8-6.4 3-10"></path>
                  <path d="M9.5 9.4c1.1.8 1.8 2.2 2 3.7"></path><path d="M14.1 6.5c.9 1.8 1.9 5.5-2.1 8.5"></path>
                </svg>
              </div>
              <h3 className="text-lg font-medium mb-2">Environmental Analysis</h3>
              <p className="text-muted-foreground text-sm">
                Get data-driven insights on carbon footprint, resource efficiency, and environmental impact metrics.
              </p>
            </div>
            
            <div className="bg-card/30 backdrop-blur-sm rounded-lg p-5 border-[0.5px] border-border/30 shadow-sm hover:shadow-md transition-shadow">
              <div className="h-10 w-10 rounded-full bg-primary/5 flex items-center justify-center mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="text-primary">
                  <path d="M18 20a6 6 0 0 0-12 0"></path><circle cx="12" cy="10" r="4"></circle>
                  <circle cx="18" cy="9" r="1"></circle><circle cx="6" cy="9" r="1"></circle>
                </svg>
              </div>
              <h3 className="text-lg font-medium mb-2">Social Responsibility</h3>
              <p className="text-muted-foreground text-sm">
                Guidance on workplace practices, community engagement, and diversity & inclusion initiatives.
              </p>
            </div>
            
            <div className="bg-card/30 backdrop-blur-sm rounded-lg p-5 border-[0.5px] border-border/30 shadow-sm hover:shadow-md transition-shadow">
              <div className="h-10 w-10 rounded-full bg-primary/5 flex items-center justify-center mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="text-primary">
                  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                </svg>
              </div>
              <h3 className="text-lg font-medium mb-2">Governance Excellence</h3>
              <p className="text-muted-foreground text-sm">
                Expert advice on organizational structure, ethics, compliance, and risk management frameworks.
              </p>
            </div>
          </div>
        </section>

        {/* Streamlit App Section */}
        <section className="py-12 max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold mb-3">Try Our ESG Consultant Now</h2>
            <p className="text-muted-foreground max-w-xl mx-auto text-sm">
              Get instant AI-powered guidance on your ESG questions and receive actionable insights in real-time.
            </p>
          </div>
          <StreamlitEmbed />
        </section>
        
        {/* CTA Section */}
        <section className="py-12 max-w-5xl mx-auto">
          <div className="bg-gradient-to-r from-primary/10 to-orange-400/10 rounded-xl p-6 md:p-8 text-center relative overflow-hidden">
            <div className="absolute inset-0 bg-card/20 backdrop-blur-sm"></div>
            <div className="relative z-10">
              <h2 className="text-2xl font-bold mb-3">Ready to Transform Your ESG Strategy?</h2>
              <p className="text-base mb-6 max-w-lg mx-auto">
                Join organizations using our AI consultant
              </p>
              <div className="flex flex-col sm:flex-row justify-center gap-3">
                <Button size="md" className="shadow-primary/10 shadow-lg">Get Started</Button>
                <Button size="md" variant="secondary">Schedule Demo</Button>
              </div>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  )
}

//Grok

// import Image from "next/image"
// import { Button } from "@/components/ui/button"
// import StreamlitEmbed from "@/components/streamlit-embed"
// import Navbar from "@/components/navbar"
// import Footer from "@/components/footer"

// export default function Home() {
//   return (
//     <div className="min-h-screen flex flex-col">
//       <div className="fixed inset-0 -z-10">
//         <Image
//           src="/placeholder.svg?height=1080&width=1920"
//           alt="Background texture"
//           fill
//           className="object-cover"
//           priority
//         />
//         <div className="absolute inset-0 bg-black/60" />
//       </div>

//       <Navbar />

//       <main className="flex-1 container mx-auto px-4 py-8">
//         {/* Hero Section */}
//         <section className="py-16 md:py-24 text-center max-w-4xl mx-auto">
//           <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-white">ESG Consultant Companion</h1>
//           <p className="mt-4 text-xl text-gray-300">Your AI-powered ESG advisor</p>
//           <p className="mt-6 text-lg text-gray-200 max-w-3xl mx-auto">
//             Our tool provides quick, AI-powered guidance on ESG topics, offering actionable insights to improve
//             sustainability strategies and support ESG compliance.
//           </p>
//           <div className="mt-8 flex justify-center gap-4">
//             <Button size="lg">Get Started</Button>
//             <Button size="lg" variant="outline">
//               Learn More
//             </Button>
//           </div>
//         </section>

//         {/* Streamlit App Section */}
//         <section className="py-8 md:py-16">
//           <div className="bg-gray-800 rounded-lg shadow-lg overflow-hidden border border-gray-700">
//             <div className="p-4 bg-gray-700 border-b border-gray-600">
//               <h2 className="text-2xl font-semibold text-white">Chat with our ESG Consultant</h2>
//               <p className="text-gray-300">Get instant AI-powered guidance on your ESG questions</p>
//             </div>
//             <StreamlitEmbed />
//           </div>
//         </section>
//       </main>

//       <Footer />
//     </div>
//   )
// }