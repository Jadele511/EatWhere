"use strict";

let resultIndex = 0;
let resultYelp = [];
let long = 0;
let lat = 0;

$("#nextBtn").on("click", () => {
  resultIndex++;
  resultIndex %= 5;
  showRes();
});

function showRes() {
  $("#search-result>img").attr("src", `${resultYelp[resultIndex].image_url}`);
  $("#res-name").html(`${resultYelp[resultIndex].name}`);
  $("#rating").html(`${resultYelp[resultIndex].rating}`);
  $("#review-count").html(`${resultYelp[resultIndex].review_count} reviews `);
  $("#price").html(`${resultYelp[resultIndex].price}`);
  $("#categories").html(`${resultYelp[resultIndex].categories[0].title}`);
  $("#address").html(`${resultYelp[resultIndex].location.display_address}`);
  $("#res-details").attr("href", `${resultYelp[resultIndex].url}`);
  $("#res-details").attr("style", "display: block");
}

if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(processPosition);
} else {
  alert("Geolocation is not supported by this browser.");
}

function processPosition(position) {
  lat = position.coords.latitude;
  long = position.coords.longitude;
  getYelpRes();
}

function getYelpRes() {
  const formData = {
    location: $("#search-location").val(),
    categories: $("#search-categories").val(),
    price: $("#search-price").val(),
    sort_by: $("#search-sort-by").val(),
  };

  if (formData.location === "") {
    delete formData.location;
    formData.longitude = long;
    formData.latitude = lat;
  }

  $.get("/restaurants-search.json", formData, (res) => {
    // Display response from the server
    resultYelp = res.businesses;
    showRes();
    $("#nextBtn").attr("style", "display: block");
  });
}

function onChange(evt) {
  evt.preventDefault();
  getYelpRes();  
}


$("#search-location").on("change", onChange);
$("#search-categories").on("change", onChange);
$("#search-price").on("change", onChange);
$("#search-sort-by").on("change", onChange);
