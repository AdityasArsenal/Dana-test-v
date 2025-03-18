import Link from "next/link"

export default function Footer() {
  return (
    <footer className="border-t border-border/40 bg-background">
      <div className="container py-8 flex flex-col md:flex-row justify-between items-center gap-4">
        <div className="text-sm text-muted-foreground">© 2025 ESG Consultant Companion</div>
        <div className="flex gap-6">
          <Link href="/privacy" className="text-sm text-muted-foreground hover:text-primary">
            Privacy Policy
          </Link>
          <Link href="/terms" className="text-sm text-muted-foreground hover:text-primary">
            Terms of Service
          </Link>
          <Link href="/contact" className="text-sm text-muted-foreground hover:text-primary">
            Contact
          </Link>
        </div>
      </div>
    </footer>
  )
}



