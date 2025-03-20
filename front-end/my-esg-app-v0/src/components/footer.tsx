import Link from "next/link"

export default function Footer() {
  return (
    <footer className="border-t border-border/40 bg-secondary/5 w-full">
      <div className="container mx-auto px-4 py-12 grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-full bg-gradient-to-br from-primary to-orange-400 flex items-center justify-center shadow-md">
              <span className="font-bold text-white text-sm">E</span>
            </div>
            <span className="font-bold text-lg">
              <span className="gradient-text">ESG</span> Consultant
            </span>
          </div>
          <p className="text-sm text-muted-foreground max-w-xs">
            Providing AI-powered ESG guidance to help organizations build sustainable futures.
          </p>
        </div>
        
        <div className="space-y-4">
          <h4 className="font-medium text-base">Services</h4>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li><Link href="#" className="hover:text-primary transition-colors">ESG Strategy</Link></li>
            <li><Link href="#" className="hover:text-primary transition-colors">Sustainability Reporting</Link></li>
            <li><Link href="#" className="hover:text-primary transition-colors">Impact Assessment</Link></li>
            <li><Link href="#" className="hover:text-primary transition-colors">Regulatory Compliance</Link></li>
          </ul>
        </div>
        
        <div className="space-y-4">
          <h4 className="font-medium text-base">Company</h4>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li><Link href="#" className="hover:text-primary transition-colors">About Us</Link></li>
            <li><Link href="#" className="hover:text-primary transition-colors">Our Team</Link></li>
            <li><Link href="#" className="hover:text-primary transition-colors">Blog</Link></li>
            <li><Link href="#" className="hover:text-primary transition-colors">Contact</Link></li>
          </ul>
        </div>
        
        <div className="space-y-4">
          <h4 className="font-medium text-base">Legal</h4>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li><Link href="/privacy" className="hover:text-primary transition-colors">Privacy Policy</Link></li>
            <li><Link href="/terms" className="hover:text-primary transition-colors">Terms of Service</Link></li>
            <li><Link href="/cookies" className="hover:text-primary transition-colors">Cookie Policy</Link></li>
          </ul>
        </div>
      </div>
      
      <div className="container mx-auto px-4 py-6 border-t border-border/40 flex flex-col md:flex-row justify-between items-center gap-4">
        <div className="text-sm text-muted-foreground">© 2025 ESG Consultant Companion. All rights reserved.</div>
        <div className="flex items-center gap-4">
          <Link href="#" className="text-muted-foreground hover:text-primary transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect width="4" height="12" x="2" y="9"></rect><circle cx="4" cy="4" r="2"></circle></svg>
          </Link>
          <Link href="#" className="text-muted-foreground hover:text-primary transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"></path></svg>
          </Link>
          <Link href="#" className="text-muted-foreground hover:text-primary transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"></line></svg>
          </Link>
        </div>
      </div>
    </footer>
  )
}


//Grok

// import Link from "next/link"

// export default function Footer() {
//   return (
//     <footer className="border-t border-gray-700 bg-gray-900">
//       <div className="container py-8 flex flex-col md:flex-row justify-between items-center gap-4 text-gray-300">
//         <div>© 2025 ESG Consultant Companion</div>
//         <div className="flex gap-6">
//           <Link href="/privacy" className="hover:text-orange-500">
//             Privacy Policy
//           </Link>
//           <Link href="/terms" className="hover:text-orange-500">
//             Terms of Service
//           </Link>
//           <Link href="/contact" className="hover:text-orange-500">
//             Contact
//           </Link>
//         </div>
//       </div>
//     </footer>
//   )
// }