var searchTerm = getUrlParams("query");

if (searchTerm.length > 0) {
  document.getElementById('search-box').setAttribute("value", searchTerm);

  // Initalize lunr with the fields it will be searching on. I've given title
  // a boost of 10 to indicate matches on this field are more important.
  var idx = lunr(function () {
    this.field('id');
    this.field('title', { boost: 10 });
    this.field('author');
    this.field('category');
    this.field('content');

    for (var key in window.store) { // Add the data to lunr
      this.add({
        'id': key,
        'title': window.store[key].title,
        'author': window.store[key].author,
        'category': window.store[key].category,
        'content': window.store[key].content
      });
    }
  });

  var results = idx.search(searchTerm); // Get lunr to perform a search
  displaySearchResults(results, window.store); // We'll write this in the next section
}

function displaySearchResults(results, store) {
  var searchResults = document.getElementById('search-results');

  if (results.length) { // Are there any results?
    var appendString = '';

    for (var i = 0; i < results.length; i++) {  // Iterate over the results
      var item = store[results[i].ref];
      appendString += '<a href="' + item.url + '" class="list-group-item list-group-item-action flex-column align-items-start">';
      appendString += '<div class="d-flex w-100 justify-content-between"><h3 class="mb-1">' + item.title + '</h3>';
      appendString += '<small>' + item.date + '</small></div>';
      appendString += '<p class="mb-1 mt-3">' + item.content.substring(0, 150) + '...</p>';
      if (item.author.length > 0) {
        appendString += '<small>' + item.author + '</small>';
      }
      appendString += '</a>';
    }

    searchResults.innerHTML = appendString;
  } else {
    searchResults.innerHTML = '<p class="lead">No results found for "' + searchTerm + '"</p>';
  }
}
