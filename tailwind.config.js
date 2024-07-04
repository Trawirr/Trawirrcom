/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')

module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    colors: {
      black: '#000000',
      sky: colors.sky,
      gray: colors.gray,
      red: colors.red,
      purple: colors.purple,

      'main_color': {
        100: '#2D3250',
        200: '#424769',
        300: '#7077A1', 
      },
      'secondary_color': '#F6B17A',

      'trawirr-gray': {
        100: '#222831',
        200: '#393E46'
      },
      'trawirr-yellow': '#FFD369',
      'trawirr-white': '#EEEEEE'
    },
    extend: {},
  },
  plugins: [],
}

