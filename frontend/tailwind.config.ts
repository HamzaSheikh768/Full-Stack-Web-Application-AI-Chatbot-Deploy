import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: 'class', // Enable dark mode with class strategy
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Poppins"', '"Inter"', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'],
      },
      colors: {
        // Dark mode defaults (pure black background)
        dark: {
          bg: "#000000", // Pure black as specified in design
          'text-primary': "#E5E7EB", // Light gray text
          'text-secondary': "#9CA3AF", // Secondary text
          accent: "#1E3A8A", // Dark blue accent
          hover: "#2563EB", // Hover color
          border: "#1F2937", // Border color
        },
        // Light mode
        light: {
          bg: "#FFFFFF", // White background
          'text-primary': "#111827", // Dark text
          'text-secondary': "#4B5563", // Secondary text
          accent: "#1E40AF", // Blue accent
          hover: "#3B82F6", // Hover color
          border: "#D1D5DB", // Border color
        },
        // Keep existing colors for compatibility
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        glass: {
          bg: "rgba(255, 255, 255, 0.05)",
          fg: "rgba(255, 255, 255, 0.85)",
          border: "rgba(255, 255, 255, 0.1)",
        },
      },
      // Add custom animations as specified
      animation: {
        'fade-in-up': 'fadeInUp 400ms ease-out',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'scale-glow': 'scaleGlow 200ms ease-in-out',
        'grid-move': 'gridMove 20s linear infinite',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 0 0px rgba(37, 99, 235, 0.3)' },
          '100%': { boxShadow: '0 0 0 6px rgba(37, 99, 235, 0)' },
        },
        scaleGlow: {
          '0%': { transform: 'scale(1)', boxShadow: '0 0 0 0 rgba(37, 99, 235, 0)' },
          '50%': { transform: 'scale(1.02)', boxShadow: '0 0 10px 2px rgba(37, 99, 235, 0.3)' },
          '100%': { transform: 'scale(1)', boxShadow: '0 0 0 0 rgba(37, 99, 235, 0)' },
        },
        gridMove: {
          '0%': { transform: 'translate(0, 0)' },
          '100%': { transform: 'translate(20px, 20px)' },
        },
      },
      borderRadius: {
        xl: '1rem',     // 16px for cards
        lg: '0.75rem',  // 12px for buttons
        '12px': '12px',
        '16px': '16px',
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic": "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
        // Animated grid background for landing page
        "grid-pattern": "linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)",
      },
      spacing: {
        '16': '1rem',
        '24': '1.5rem',
        '80': '5rem',
      },
      backdropBlur: {
        xs: "2px",
        md: "4px",
        lg: "8px",
      },
      boxShadow: {
        glass: "0 8px 32px 0 rgba(31, 38, 135, 0.37)",
        'lg-glow': "0 10px 25px -3px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(37, 99, 235, 0.3)",
      },
    },
  },
  plugins: [],
};
export default config;