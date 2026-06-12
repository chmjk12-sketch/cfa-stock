import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CFA Stock Discovery",
  description: "CFA Ontology-Driven Stock Analysis Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN" className="dark">
      <body className="bg-cfa-bg text-cfa-text min-h-screen">
        {children}
      </body>
    </html>
  );
}
