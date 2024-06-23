/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')

module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    colors: {
      black: '#000000',
      sky: colors.sky,
      gray: colors.gray
    },
    extend: {},
  },
  plugins: [],
}

