"use strict";

let resultIndex = 0;
let resultYelp = [];
let userLong = 0;
let userLat = 0;
let map;
let resMarker;


function initMap() {
  map = new google.maps.Map(document.getElementById("google-map"), {
    zoom: 14,
    center: {lat: 0, lng: 0}
  });
}

function restaurantMarker(biz) {
  const myLatLng = { lat: biz.lat, lng: biz.long };  
  resMarker = new google.maps.Marker({
    position: myLatLng,
    map,
    title: "Restaurant Location",
  });
  map.setCenter(myLatLng);
  $("#google-map").attr("style", "visibility:visible");
}


function showRes() {
  let biz = resultYelp[resultIndex];
  restaurantMarker(biz);
  $("#search-result").attr("style", "visibility:visible");
  $("#search-result>img").attr("src", `${biz.image_url}`);
  $("#res-name").html(`${biz.name}`);
  $("#rating").html(`${biz.rating}`);
  $("#review-count").html(`${biz.review_count} reviews `);
  $("#price").html(`${biz.price}`);
  $("#categories").html(`${biz.categories}`);
  $("#address").html(`${biz.address}`);
  $("#res-details").attr("href", `${biz.url}`);
  let color = biz.liked ? "darkblue" : "gray";
  $("#thumbs-up").attr("style", "display: inline; color:" + color);
  $("#resultBtn").attr("style", "display: inline;");
}


$("#nextBtn").on("click", () => {
  resultIndex++;
  resultIndex %= 5;
  resMarker.setMap(null);
  showRes();
});

$("#thumbs-up").on("click", () => {
  let biz = resultYelp[resultIndex];
  $.get(`/like/${biz.id}`, (res) => {
    let color = res.liked ? "darkblue" : "gray";
    $("#thumbs-up").attr("style", "display: inline; color:" + color);
  });
});

$("#resultBtn").on("click", () => {

  $.get("/vote-result.json", (res) => {
    $("#thumbs-up").attr("style", "visibility:hidden ");
    $("#resultBtn").attr("style", "visibility:hidden");
    $("#nextBtn").attr("style", "visibility:hidden");
    let biz = res;
    $("#vote-result").attr("style", "visibility:visible");
    showRes();
  });
});

if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(processPosition);
} else {
  alert("Geolocation is not supported by this browser.");
}

function processPosition(position) {
  userLat = position.coords.latitude;
  userLong = position.coords.longitude;
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
    formData.longitude = userLong;
    formData.latitude = userLat;
  }

  $.get("/restaurants-search.json", formData, (res) => {
    // Display response from the server
    resultYelp = res.businesses;
    showRes();
  });
}

function onChange(evt) {
  evt.preventDefault();
  getYelpRes();
  resMarker.setMap(null);
}

$("#search-location").on("change", onChange);
$("#search-categories").on("change", onChange);
$("#search-price").on("change", onChange);
$("#search-sort-by").on("change", onChange);
