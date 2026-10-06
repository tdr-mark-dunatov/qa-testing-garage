/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'racing-red': '#DC2626',
        'racing-black': '#0F172A',
        'pit-orange': '#F97316',
        'checkered': '#E5E7EB',
      },
      animation: {
        'speed-pulse': 'pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}
