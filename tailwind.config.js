/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './Q-Airline/frontend/src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        san: ['Poppins', 'san-serif']
      },
    },
  },
  plugins: [],
}

