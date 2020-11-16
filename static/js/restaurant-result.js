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
    $('#search-result>img').attr('src', `${res.businesses[0].image_url}`)
    $('#res-name').html(`${res.businesses[0].name}`)
    $('#rating').html(`${res.businesses[0].rating}`)
    $('#review-count').html(`${res.businesses[0].review_count} reviews `)
    $('#price').html(`${res.businesses[0].price}`)
    $('#categories').html(`${res.businesses[0].categories[0].title}`)
    $('#address').html(`${res.businesses[0].location.display_address}`)
    $('#res-details').attr('action', `${res.businesses[0].url}`)
    $('#res-details>input').attr('type', 'submit')

  });
});
