const purgecss = require('@fullhuman/postcss-purgecss')({

  // Specify the paths to all of the template files in your project
  content: [
    '../stealthx/templates/**/*.html',
    // etc.
  ],

  // Include any special characters you're using in this regular expression
  defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || []
})

const IN_PRODUCTION = process.env.NODE_ENV === "production";

module.exports = {
  plugins: [
    require("postcss-import"),
    require("tailwindcss")("tailwind.config.js"),
    require("postcss-nested"),
    require("postcss-custom-properties"),
    IN_PRODUCTION && require('@fullhuman/postcss-purgecss')({

      // Specify the paths to all of the template files in your project
      content: [
        './stealthx/templates/**/*.html',
        // etc.
      ],

      // Include any special characters you're using in this regular expression
      defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || []
    }),
    require('autoprefixer'),
  ]
}