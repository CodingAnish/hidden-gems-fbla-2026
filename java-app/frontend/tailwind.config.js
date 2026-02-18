/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#2563EB",
          hover: "#1e40af",
          light: "#dbeafe",
        },
        surface: {
          DEFAULT: "#ffffff",
          hover: "#f8fafc",
        },
      },
      fontFamily: {
        sans: ["DM Sans", "system-ui", "sans-serif"],
      },
      maxWidth: {
        content: "480px",
      },
    },
  },
  plugins: [],
};
