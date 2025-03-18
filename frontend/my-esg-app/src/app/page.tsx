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
          className="object-cover opacity-20"
          priority
        />
        <div className="absolute inset-0 bg-gradient-to-b from-background/80 to-background/95" />
      </div>

      <Navbar />

      <main className="flex-1 container mx-auto px-4 py-8">
        {/* Hero Section */}
        <section className="py-16 md:py-24 text-center max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-primary">ESG Consultant Companion</h1>
          <p className="mt-4 text-xl text-muted-foreground">short tag line</p>
          <p className="mt-6 text-lg text-center max-w-3xl mx-auto">
            Our tool provides quick, AI-powered guidance on ESG topics, offering actionable insights to improve
            sustainability strategies and support ESG compliance.
          </p>
          <div className="mt-8 flex justify-center gap-4">
            <Button size="lg">Get Started</Button>
            <Button size="lg" variant="outline">
              Learn More
            </Button>
          </div>
        </section>

        {/* Streamlit App Section */}
        <section className="py-8 md:py-16">
          <div className="bg-card rounded-lg shadow-lg overflow-hidden border border-border">
            <div className="p-4 bg-muted border-b border-border">
              <h2 className="text-2xl font-semibold">Chat with our ESG Consultant</h2>
              <p className="text-muted-foreground">Get instant AI-powered guidance on your ESG questions</p>
            </div>
            <StreamlitEmbed />
          </div>
        </section>
      </main>

      <Footer />
    </div>
  )
}

