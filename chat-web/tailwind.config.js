/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        "primary-main": "#9BB4C6",
        "primary-sub": "#FBD418",
      },
    },
  },
  plugins: [],
};
