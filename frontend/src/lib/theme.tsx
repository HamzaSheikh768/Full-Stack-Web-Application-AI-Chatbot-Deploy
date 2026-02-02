'use client';

import { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'dark' | 'light';

type ThemeContextType = {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  systemTheme: 'dark' | 'light' | null;
};

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('dark'); // Default to dark as per design spec
  const [systemTheme, setSystemTheme] = useState<'dark' | 'light' | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Check for saved theme in localStorage
    const savedTheme = localStorage.getItem('theme') as Theme | null;

    // Detect system preference
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const detectedSystemTheme = mediaQuery.matches ? 'dark' : 'light';
    setSystemTheme(detectedSystemTheme);

    // Determine initial theme
    const initialTheme = savedTheme || detectedSystemTheme;

    setTheme(initialTheme);
    setMounted(true);

    // Listen for system theme changes
    const handleSystemThemeChange = (e: MediaQueryListEvent) => {
      const newSystemTheme = e.matches ? 'dark' : 'light';
      setSystemTheme(newSystemTheme);

      // If user hasn't set a preference, update to match system
      if (!localStorage.getItem('theme')) {
        setTheme(newSystemTheme);
      }
    };

    mediaQuery.addEventListener('change', handleSystemThemeChange);

    return () => {
      mediaQuery.removeEventListener('change', handleSystemThemeChange);
    };
  }, []); // Empty dependency array since mediaQuery is recreated each time

  useEffect(() => {
    if (!mounted) return;

    // Apply theme to document
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
      document.documentElement.style.colorScheme = 'dark';
    } else {
      document.documentElement.classList.remove('dark');
      document.documentElement.style.colorScheme = 'light';
    }

    // Save to localStorage
    localStorage.setItem('theme', theme);
  }, [theme, mounted]);

  const value = {
    theme,
    setTheme,
    systemTheme,
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}