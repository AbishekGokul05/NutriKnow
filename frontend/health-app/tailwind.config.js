/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#2563eb",
        secondary: "#1e40af",
      },
      animation: {
        'zoom': 'zoom 2.5s ease-in-out',
      },
      keyframes: {
        zoom: {
          '0%': { transform: 'scale(0.5)', opacity: '0' },
          '50%': { transform: 'scale(1.1)' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        }
      },
      transitionDuration: {
        '2000': '2000ms',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
} 