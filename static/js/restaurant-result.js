"use strict";

$('#search-form').on('submit', (evt) => {
  evt.preventDefault();

  // Get user input from a form
  const formData = {
    location: $('#search-location').val(),
    categories: $('#search-categories').val(),
    price: $('#search-price').val(),
    open_now: $('#search-open_now').val(),
    sort_by: $('#search-sort_by').val()
  };
    // const formData = $('#search-form').serialize()

  // Send formData to the server (becomes a query string)
  $.get('/restaurants-search.json', formData, (res) => {
    // Display response from the server
    $('#search-result').append(`<h2>${res.businesses[0].name}</h2>`)
    $('#search-result').append(`<p>${res.businesses[0].rating}</p>`)
    $('#search-result').append(`<p>${res.businesses[0].review_count} reviews </p>`)
    $('#search-result').append(`<p>${res.businesses[0].location.address1} reviews </p>`)
    // $('#search-result').append(`<img src=${res.businesses[0].image_url} reviews>`)
    $('#search-result').append(`<form action=${res.businesses[0].url}><input type="submit" value="Restaurant details on Yelp" /></form>`)
  });
});
