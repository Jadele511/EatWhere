"use strict";

let resultIndex = 0;
let resultYelp = []

$('#next').on('click', () => {
  resultIndex++;
  resultIndex %= 5;
  showRes();
})

function showRes(){
    $('#search-result>img').attr('src', `${resultYelp[resultIndex].image_url}`)
    $('#res-name').html(`${resultYelp[resultIndex].name}`)
    $('#rating').html(`${resultYelp[resultIndex].rating}`)
    $('#review-count').html(`${resultYelp[resultIndex].review_count} reviews `)
    $('#price').html(`${resultYelp[resultIndex].price}`)
    $('#categories').html(`${resultYelp[resultIndex].categories[0].title}`)
    $('#address').html(`${resultYelp[resultIndex].location.display_address}`)
    $('#res-details').attr('action', `${resultYelp[resultIndex].url}`)
    $('#res-details>input').attr('type', 'submit')
}


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
    resultYelp = res.businesses; 
    showRes();
  });
});



