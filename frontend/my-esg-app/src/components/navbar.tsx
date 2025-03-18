import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-20 items-center justify-between">
        <div className="flex items-center gap-2">
          <Link href="/" className="flex items-center gap-2">
            <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary to-orange-400 flex items-center justify-center shadow-lg">
              <span className="font-bold text-white text-lg">E</span>
            </div>
            <span className="font-bold text-xl tracking-tight">
              <span className="gradient-text">ESG</span> Consultant
            </span>
          </Link>
        </div>
        <nav className="hidden md:flex items-center gap-8">
          <Link href="/" className="text-sm font-medium hover:text-primary transition-colors">
            Home
          </Link>
          <Link href="/services" className="text-sm font-medium hover:text-primary transition-colors">
            Services
          </Link>
          <Link href="/about" className="text-sm font-medium hover:text-primary transition-colors">
            About
          </Link>
          <Link href="/contact" className="text-sm font-medium hover:text-primary transition-colors">
            Contact
          </Link>
        </nav>
        <div className="flex items-center gap-4">
          <Button size="sm" variant="outline" className="hidden sm:inline-flex">Sign In</Button>
          <Button size="sm">Get Started</Button>
        </div>
      </div>
    </header>
  )
}

//Grok

// import Link from "next/link"
// import { Button } from "@/components/ui/button"

// export default function Navbar() {
//   return (
//     <header className="sticky top-0 z-50 w-full border-b border-gray-700 bg-gray-900/95 backdrop-blur supports-[backdrop-filter]:bg-gray-900/60">
//       <div className="container flex h-16 items-center justify-between">
//         <div className="flex items-center gap-2">
//           <Link href="/" className="font-semibold text-xl text-orange-500">
//             ESG Consultant
//           </Link>
//         </div>
//         <nav className="flex items-center gap-4 text-white">
//           <Link href="/" className="text-sm font-medium hover:text-orange-500">
//             Home
//           </Link>
//           <Link href="/contact" className="text-sm font-medium hover:text-orange-500">
//             Contact
//           </Link>
//           <Button size="sm">Sign In</Button>
//         </nav>
//       </div>
//     </header>
//   )
// }