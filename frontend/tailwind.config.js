/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: "#0e1a1f",
          DEFAULT: "#14252C", // Deep Navy
        },
        slate: {
          dark: "#273C41",    // Dark Slate
          DEFAULT: "#45575B", // Slate
          light: "#5c7176",
        },
        gray: {
          muted: "#A3A39B",   // Muted Light Gray
        },
        cream: {
          DEFAULT: "#E6CAB3", // Warm Cream
          soft: "#f3e5d7",
          muted: "#d8b69b",
        },
        orange: {
          burnt: "#82401D",   // Burnt Orange Accent
          hover: "#994c23",
          soft: "#663318",
        },
      },
      fontFamily: {
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          "Inter",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "sans-serif",
        ],
        mono: ["JetBrains Mono", "SFMono-Regular", "Menlo", "monospace"],
      },
      borderRadius: {
        'sm': '8px',
        'md': '14px',
        'lg': '18px',
        'xl': '22px',
        '2xl': '26px',
      },
      boxShadow: {
        'card': '0 4px 20px -2px rgba(14, 26, 31, 0.6), 0 2px 6px -1px rgba(0, 0, 0, 0.4)',
        'panel': '0 10px 30px -4px rgba(10, 18, 22, 0.8), 0 4px 12px -2px rgba(0, 0, 0, 0.5)',
        'glow-orange': '0 0 25px rgba(130, 64, 29, 0.35)',
        'glow-cream': '0 0 20px rgba(230, 202, 179, 0.15)',
      },
    },
  },
  plugins: [],
}
