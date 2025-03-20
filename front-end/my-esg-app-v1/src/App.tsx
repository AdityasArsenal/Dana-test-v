import React from 'react';
import { Brain, Database, LineChart, Search, Users, Bot, ArrowRight, Building2, ChevronRight, Github, Twitter, Linkedin, Mail } from 'lucide-react';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed w-full bg-white/80 backdrop-blur-sm z-50 border-b border-gray-100">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <Brain className="w-8 h-8 text-emerald-600" />
              <span className="text-xl font-bold">ESG<span className="text-emerald-600">ai</span></span>
            </div>
            <div className="hidden md:flex items-center gap-8">
              <a href="#vision" className="text-gray-600 hover:text-gray-900 transition">Our Vision</a>
              <a href="#agents" className="text-gray-600 hover:text-gray-900 transition">Research</a>
              <a href="#demo" className="text-gray-600 hover:text-gray-900 transition">Demo</a>
              <button className="bg-emerald-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-emerald-700 transition duration-300 transform hover:scale-105">
                Support Our Research
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative bg-gradient-to-r from-emerald-50 to-teal-50 pt-24">
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1557426272-fc759fdf7a8d?auto=format&fit=crop&q=80')] bg-cover bg-center opacity-5"></div>
        <div className="container mx-auto px-4 py-20 md:py-32">
          <div className="max-w-4xl mx-auto text-center relative">
            <div className="inline-block mb-4 px-4 py-1 bg-emerald-100 rounded-full text-emerald-800 text-sm font-medium animate-fade-in">
              Research Project
            </div>
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6 tracking-tight leading-tight">
              Reimagining ESG Analysis<br />Through <span className="text-emerald-600 relative">AI Innovation
                <span className="absolute bottom-0 left-0 w-full h-1 bg-emerald-600/30 transform -skew-x-12"></span>
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-700 mb-12 leading-relaxed">
              We're a team of AI researchers exploring the potential of multi-agent systems to revolutionize ESG data analysis in India
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <button className="bg-emerald-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-emerald-700 transition duration-300 transform hover:scale-105 flex items-center justify-center gap-2 shadow-lg shadow-emerald-200">
                Join Our Vision <ArrowRight className="w-5 h-5" />
              </button>
              <a href="#demo" className="bg-white text-gray-800 px-8 py-4 rounded-xl font-semibold hover:bg-gray-50 transition duration-300 transform hover:scale-105 flex items-center justify-center gap-2 border border-gray-200">
                Try Demo <ChevronRight className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-b from-transparent to-white"></div>
      </div>

      {/* Vision Section */}
      <div id="vision" className="py-24 bg-white scroll-mt-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-6 relative inline-block">
                Our Research Vision
                <span className="absolute bottom-0 left-0 w-full h-1 bg-emerald-600/30 transform -skew-x-12"></span>
              </h2>
              <p className="text-gray-600 text-lg leading-relaxed">
                We believe that AI can transform how organizations understand and analyze ESG data. Our research focuses on developing intelligent systems that can process and analyze complex ESG reports from India's top 1000 listed companies, making this valuable information more accessible and actionable.
              </p>
            </div>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-gray-50 p-8 rounded-2xl hover:shadow-lg transition duration-300 transform hover:-translate-y-1">
                <h3 className="text-2xl font-semibold mb-4">The Challenge</h3>
                <p className="text-gray-600 leading-relaxed">
                  ESG reporting in India is evolving rapidly with BRSR mandates, creating vast amounts of unstructured data. Traditional analysis methods struggle to keep pace with this complexity and scale.
                </p>
              </div>
              <div className="bg-emerald-50 p-8 rounded-2xl hover:shadow-lg transition duration-300 transform hover:-translate-y-1">
                <h3 className="text-2xl font-semibold mb-4">Our Approach</h3>
                <p className="text-gray-600 leading-relaxed">
                  We're developing an experimental multi-agent AI system that can understand, analyze, and derive insights from ESG reports, making this information accessible to stakeholders.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Research Progress */}
      <div className="py-12 bg-white relative scroll-mt-16">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
            <div className="text-center transform hover:scale-105 transition duration-300">
              <div className="text-4xl font-bold text-emerald-600 mb-2">1000+</div>
              <div className="text-gray-600">Companies in Dataset</div>
            </div>
            <div className="text-center transform hover:scale-105 transition duration-300">
              <div className="text-4xl font-bold text-emerald-600 mb-2">3</div>
              <div className="text-gray-600">AI Agents Developed</div>
            </div>
            <div className="text-center transform hover:scale-105 transition duration-300">
              <div className="text-4xl font-bold text-emerald-600 mb-2">MVP</div>
              <div className="text-gray-600">Development Stage</div>
            </div>
            <div className="text-center transform hover:scale-105 transition duration-300">
              <div className="text-4xl font-bold text-emerald-600 mb-2">85%</div>
              <div className="text-gray-600">Query Accuracy</div>
            </div>
          </div>
        </div>
      </div>

      {/* AI Agents Section */}
      <div id="agents" className="py-24 bg-gray-50 scroll-mt-16">
        <div className="container mx-auto px-4">
          <div className="max-w-xl mx-auto text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4 relative inline-block">
              Our Research Breakthrough
              <span className="absolute bottom-0 left-0 w-full h-1 bg-emerald-600/30 transform -skew-x-12"></span>
            </h2>
            <p className="text-gray-600 text-lg">
              We've developed three specialized AI agents that work together to analyze complex ESG data
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100 hover:shadow-2xl transition duration-300 transform hover:-translate-y-1">
              <div className="w-16 h-16 bg-blue-100 rounded-xl flex items-center justify-center mb-6">
                <Users className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-2xl font-semibold mb-4">Manager Agent</h3>
              <p className="text-gray-600 leading-relaxed">
                Our experimental agent that breaks down complex queries into manageable components, understanding context and nuances in ESG terminology.
              </p>
            </div>
            <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100 hover:shadow-2xl transition duration-300 transform hover:-translate-y-1">
              <div className="w-16 h-16 bg-emerald-100 rounded-xl flex items-center justify-center mb-6">
                <Bot className="w-8 h-8 text-emerald-600" />
              </div>
              <h3 className="text-2xl font-semibold mb-4">Worker Agent</h3>
              <p className="text-gray-600 leading-relaxed">
                A specialized agent designed to efficiently process and analyze information from our database of ESG reports and financial data.
              </p>
            </div>
            <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100 hover:shadow-2xl transition duration-300 transform hover:-translate-y-1">
              <div className="w-16 h-16 bg-purple-100 rounded-xl flex items-center justify-center mb-6">
                <Brain className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="text-2xl font-semibold mb-4">Director Agent</h3>
              <p className="text-gray-600 leading-relaxed">
                Our synthesis agent that combines insights to generate comprehensive ESG analysis, currently being trained on industry standards.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Current Capabilities */}
      <div id="features" className="py-24 bg-white scroll-mt-16">
        <div className="container mx-auto px-4">
          <div className="max-w-xl mx-auto text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4 relative inline-block">
              Current Research Scope
              <span className="absolute bottom-0 left-0 w-full h-1 bg-emerald-600/30 transform -skew-x-12"></span>
            </h2>
            <p className="text-gray-600 text-lg">
              Our MVP focuses on analyzing key ESG data sources
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-6xl mx-auto">
            <div className="bg-white p-6 rounded-xl border border-gray-200 hover:border-emerald-200 transition duration-300 transform hover:-translate-y-1">
              <div className="w-12 h-12 bg-emerald-100 rounded-full flex items-center justify-center mb-4">
                <Building2 className="w-6 h-6 text-emerald-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Research Dataset</h3>
              <p className="text-gray-600">
                Access to reports from India's top 1000 listed companies for comprehensive analysis.
              </p>
            </div>
            <div className="bg-white p-6 rounded-xl border border-gray-200 hover:border-emerald-200 transition duration-300 transform hover:-translate-y-1">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                <Database className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">BRSR Analysis</h3>
              <p className="text-gray-600">
                Experimental processing of Business Responsibility and Sustainability Reports.
              </p>
            </div>
            <div className="bg-white p-6 rounded-xl border border-gray-200 hover:border-emerald-200 transition duration-300 transform hover:-translate-y-1">
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                <LineChart className="w-6 h-6 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">XBRL Integration</h3>
              <p className="text-gray-600">
                Testing automated analysis of standardized XBRL reporting formats.
              </p>
            </div>
            <div className="bg-white p-6 rounded-xl border border-gray-200 hover:border-emerald-200 transition duration-300 transform hover:-translate-y-1">
              <div className="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mb-4">
                <Search className="w-6 h-6 text-orange-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Prototype Queries</h3>
              <p className="text-gray-600">
                Early-stage development of comparative analysis capabilities.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Example Query Section - UPDATED DEMO SECTION */}
      <div id="demo" className="py-24 bg-gray-50 scroll-mt-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4 relative inline-block">
                Try Our ESG Analysis AI
                <span className="absolute bottom-0 left-0 w-full h-1 bg-emerald-600/30 transform -skew-x-12"></span>
              </h2>
              <p className="text-gray-600 text-lg">
                Experience our prototype AI system that can analyze and compare ESG reports from Indian companies
              </p>
            </div>
            
            {/* Chat Interface */}
            <ChatInterface />
            
            <div className="mt-8 bg-emerald-50 p-6 rounded-xl border border-emerald-100">
              <h3 className="text-xl font-semibold mb-3 text-emerald-800">Suggested Queries</h3>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="bg-white p-4 rounded-lg border border-emerald-100 hover:border-emerald-300 transition cursor-pointer">
                  "What are the key ESG metrics reported by Reliance Industries?"
                </div>
                <div className="bg-white p-4 rounded-lg border border-emerald-100 hover:border-emerald-300 transition cursor-pointer">
                  "Compare the carbon emission reduction targets of Tata Steel and JSW Steel"
                </div>
                <div className="bg-white p-4 rounded-lg border border-emerald-100 hover:border-emerald-300 transition cursor-pointer">
                  "What materiality assessment process does HDFC Bank follow?"
                </div>
                <div className="bg-white p-4 rounded-lg border border-emerald-100 hover:border-emerald-300 transition cursor-pointer">
                  "Summarize Infosys's approach to diversity and inclusion"
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-24 bg-emerald-900">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Join Us in Shaping the Future of ESG Analysis
            </h2>
            <p className="text-emerald-100 text-lg mb-12">
              We're seeking visionary partners and collaborators who share our belief in the transformative potential of AI in ESG analysis
            </p>
            <button className="bg-white text-emerald-900 px-8 py-4 rounded-xl font-semibold hover:bg-emerald-50 transition duration-300 transform hover:scale-105">
              Support Our Research
            </button>
          </div>
        </div>
      </div>

      {/* Enhanced Footer */}
      <footer className="bg-gray-900 pt-16 pb-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
            {/* Brand Column */}
            <div className="space-y-6">
              <div className="flex items-center gap-2">
                <Brain className="w-8 h-8 text-emerald-500" />
                <span className="text-xl font-bold text-white">ESG<span className="text-emerald-500">ai</span></span>
              </div>
              <p className="text-gray-400 leading-relaxed">
                Exploring the future of ESG analysis through innovative AI research and multi-agent systems.
              </p>
              <div className="flex items-center gap-4">
                <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300 transform hover:scale-110">
                  <Github className="w-5 h-5" />
                </a>
                <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300 transform hover:scale-110">
                  <Twitter className="w-5 h-5" />
                </a>
                <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300 transform hover:scale-110">
                  <Linkedin className="w-5 h-5" />
                </a>
                <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300 transform hover:scale-110">
                  <Mail className="w-5 h-5" />
                </a>
              </div>
            </div>

            {/* Research Column */}
            <div>
              <h3 className="text-white font-semibold mb-4">Research</h3>
              <ul className="space-y-3">
                <li>
                  <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300">Research Paper</a>
                </li>
                <li>
                  <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300">Methodology</a>
                </li>
                <li>
                  <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300">Technical Documentation</a>
                </li>
                <li>
                  <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300">Publications</a>
                </li>
              </ul>
            </div>

            {/* Team Column */}
            <div>
              <h3 className="text-white font-semibold mb-4">Team</h3>
              <ul className="space-y-3">
                <li>
                  <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300">About Us</a>
                </li>
                <li>
                  <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300">Research Team</a>
                </li>
                <li>
                  <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300">Advisors</a>
                </li>
                <li>
                  <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300">Join Us</a>
                </li>
              </ul>
            </div>

            {/* Contact Column */}
            <div>
              <h3 className="text-white font-semibold mb-4">Contact</h3>
              <ul className="space-y-3">
                <li>
                  <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300">Get in Touch</a>
                </li>
                <li>
                  <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300">Research Collaboration</a>
                </li>
                <li>
                  <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300">Support the Project</a>
                </li>
                <li>
                  <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300">Media Inquiries</a>
                </li>
              </ul>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="pt-8 border-t border-gray-800">
            <div className="flex flex-col md:flex-row justify-between items-center gap-4">
              <p className="text-gray-400">© 2024 ESGai Research Project. All rights reserved.</p>
              <div className="flex gap-6">
                <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300 text-sm">Privacy Policy</a>
                <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300 text-sm">Terms of Use</a>
                <a href="#" className="text-gray-400 hover:text-emerald-500 transition duration-300 text-sm">Cookie Policy</a>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;