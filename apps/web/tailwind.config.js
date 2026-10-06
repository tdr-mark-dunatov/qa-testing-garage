/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'racing-red': '#DC0000',      // Ferrari Red
        'racing-red-dark': '#A00000',  // Dark Red
        'racing-red-light': '#FF4545', // Light Red
        'racing-black': '#1A1A1A',     // Racing Black
        'pit-orange': '#FF6B00',       // Safety Car Orange
        'checkered': '#F5F5F5',        // Checkered Flag White
        'track-gray': '#E5E5E5',       // Track Gray
        'carbon-fiber': '#2D2D2D',     // Carbon Fiber
      },
      animation: {
        'speed-pulse': 'pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}
