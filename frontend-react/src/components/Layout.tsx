
import React from 'react';
import { Navigation } from './Navigation';
import { Footer } from './Footer';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout = ({ children }: LayoutProps) => {
  return (
    <div className="min-h-screen flex flex-col bg-background" role="document">
      <a 
        href="#main-content" 
        className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:p-4 focus:bg-background focus:text-foreground"
      >
        Skip to main content
      </a>
      <Navigation />
      <main id="main-content" className="flex-grow container mx-auto px-4 py-8 animate-fade-in">
        {children}
      </main>
      <Footer />
    </div>
  );
};
