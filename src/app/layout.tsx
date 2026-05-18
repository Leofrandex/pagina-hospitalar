import type { Metadata } from "next";
import { Syncopate } from "next/font/google";
import "./globals.css";

const syncopate = Syncopate({
  variable: "--font-syncopate",
  weight: ["400", "700"],
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Hospitalar Venezuela | Unimos tecnología y vida",
  description: "Equipamiento médico de clase mundial y soluciones tecnológicas para la salud.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="es"
      className={`${syncopate.variable} h-full antialiased`}
      style={{
        "--font-myriad": "'Myriad Pro Light', 'Myriad Pro', 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
      } as React.CSSProperties}
    >
      <body className="font-sans min-h-full flex flex-col">{children}</body>
    </html>
  );
}
