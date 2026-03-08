/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        sage: {
          50: '#f0f5f0',
          100: '#d9e8d9',
          200: '#b3d1b3',
          300: '#8dba8d',
          400: '#67a367',
          500: '#4a8c4a',
          600: '#3b703b',
          700: '#2c542c',
          800: '#1d381d',
          900: '#0e1c0e',
        }
      }
    },
  },
  plugins: [],
}
