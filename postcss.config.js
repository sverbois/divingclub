// Copy of https://github.com/plone/plonetheme.barceloneta/blob/master/postcss.config.js

"use strict";

module.exports = (ctx) => ({
  map: ctx.file.dirname.includes("examples")
    ? false
    : {
        inline: false,
        annotation: true,
        sourcesContent: true,
      },
  plugins: {
    autoprefixer: {
      cascade: false,
    },
  },
});
