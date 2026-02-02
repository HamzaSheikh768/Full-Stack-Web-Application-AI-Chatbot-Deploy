import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

interface AppLayoutProps {
  children: ReactNode;
  className?: string;
  hideNavbar?: boolean;
}

export const AppLayout = ({ children, className = '', hideNavbar = false }: AppLayoutProps) => {
  return (
    <div className={cn("min-h-screen bg-background text-foreground", className)}>
      {!hideNavbar && (
        <header className="sticky top-0 z-50 bg-white/80 dark:bg-dark-bg/80 backdrop-blur-md border-b border-border">
          {/* This would typically contain the Navbar component */}
        </header>
      )}
      <main className="pb-12 pt-4 md:pt-6 lg:pt-8">
        {children}
      </main>
      <footer className="py-6 border-t border-border">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>TASKAPP • Smart Task Management • Powered by AI</p>
        </div>
      </footer>
    </div>
  );
};