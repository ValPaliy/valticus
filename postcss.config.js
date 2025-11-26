const purgecss = require("@fullhuman/postcss-purgecss");

module.exports = {
  plugins: [
    purgecss({
      content: [
        "./layouts/**/*.html",
        "./themes/valticus/layouts/**/*.html",
        "./content/**/*.md",
        "./archetypes/**/*.md",
      ],
      defaultExtractor: (content) => content.match(/[A-Za-z0-9-_:/]+/g) || [],
      safelist: [
        "no-js",
        "js",
        "active",
        "is-active",
        "open",
        "closed",
        "menu--open",
        /^lang-/, // keep language classes
        /^toc-/, // keep toc classes
      ],
    }),
    require("autoprefixer"),
  ],
};
