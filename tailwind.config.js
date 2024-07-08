/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')
const plugin = require('tailwindcss/plugin')

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
      'trawirr-dark-yellow': '#FFC436',
      'trawirr-white': '#EEEEEE',

      'trawirr-green':{
        100: '#040D12',
        200: '#183D3D',
        300: '#5C8374',
        400: '#93B1A6'
      }
    },
    extend: {},
  },
  plugins: [
    plugin(function({ addVariant }) {
      addVariant('htmx-settling', ['&.htmx-settling', '.htmx-settling &'])
      addVariant('htmx-request',  ['&.htmx-request',  '.htmx-request &'])
      addVariant('htmx-swapping', ['&.htmx-swapping', '.htmx-swapping &'])
      addVariant('htmx-added',    ['&.htmx-added',    '.htmx-added &'])
    }),
  ],
}

