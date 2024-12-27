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
  plugins: [
    ({ addUtilities }) => {
      addUtilities({
        ".scrollbar-hide": {
          /* Firefox */
          "scrollbar-width": "none",
          /* IE */
          "-ms-overflow-style": "none",
          /* Webkit */
          "&::-webkit-scrollbar": {
            display: "none",
          },
        },
      });
    },
  ],
};
