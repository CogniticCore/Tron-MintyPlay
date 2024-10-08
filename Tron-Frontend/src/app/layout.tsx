import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { TronLinkProvider } from "@/components/contexts/tronlink-context";
import { CartProvider } from "@/components/contexts/cart-context";
import { ToastProvider } from "@/components/ui/toast";
import { GameProductsProvider } from "@/components/contexts/developer-game-products-context";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "MintyPlay",
  description: "Buy and play blockchain games with TRX.",
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
        <GameProductsProvider>
          <TronLinkProvider>
            <ToastProvider>
              <CartProvider>{children}</CartProvider>
            </ToastProvider>
          </TronLinkProvider>
        </GameProductsProvider>
      </body>
    </html>
  );
}
