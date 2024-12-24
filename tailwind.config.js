/** @type {import('tailwindcss').Config} */
export default {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  content: [],
  theme: {
    fontFamily: {
      'serif': ["Ringside Regular SSm A", "Ringside Regular SSm B", "system-ui", "sans-serif"],
    },
    extend: {
      colors:
      {
        'primary': '#212121',
      },
    },
  },
  plugins: [],
}

