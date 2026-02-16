import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        neon: {
          red: "#ff006e",
          "red-light": "#ff4d8f",
          "red-dark": "#cc0058",
          pink: "#ff0080",
        },
        dark: {
          bg: "#0a0a0a",
          surface: "#1a1a1a",
          "surface-light": "#2a2a2a",
          border: "#333333",
        },
      },
      boxShadow: {
        "neon-red": "0 0 10px #ff006e, 0 0 20px #ff006e, 0 0 30px #ff006e",
        "neon-red-sm": "0 0 5px #ff006e, 0 0 10px #ff006e",
      },
      animation: {
        "pulse-neon": "pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
    },
  },
  plugins: [],
};
export default config;

