import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "../globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ESG Consultant Companion | AI-Powered ESG Guidance",
  description: "Transform your organization's sustainability strategy with our AI-powered ESG consultant providing actionable insights and guidance.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}


//Grok

// import type { Metadata } from "next";
// import { Inter, Roboto_Mono } from "next/font/google"; // Use Inter and Roboto_Mono
// import "../globals.css";

// const inter = Inter({
//   variable: "--font-inter",
//   subsets: ["latin"],
// });

// const robotoMono = Roboto_Mono({
//   variable: "--font-roboto-mono",
//   subsets: ["latin"],
// });

// export const metadata: Metadata = {
//   title: "ESG Consultant Companion",
//   description: "Your AI-powered ESG advisor providing actionable insights.",
// };

// export default function RootLayout({
//   children,
// }: Readonly<{
//   children: React.ReactNode;
// }>) {
//   return (
//     <html lang="en">
//       <body
//         className={`${inter.variable} ${robotoMono.variable} antialiased`}
//       >
//         {children}
//       </body>
//     </html>
//   );
// }