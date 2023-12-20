const mediumToMarkdown = require('medium-to-markdown');
 
// Enter url here
mediumToMarkdown.convertFromUrl('https://towardsdatascience.com/scraping-flight-data-using-python-e71b97e859d3')
.then(function (markdown) {
  console.log(markdown); //=> Markdown content of medium post
});

//node medium-to-markdown.js >> file.md