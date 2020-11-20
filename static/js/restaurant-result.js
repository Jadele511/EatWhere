"use strict";

let resultIndex = 0;
let resultYelp = [];
let long = 0;
let lat = 0;


function showRes(biz) {
  $("#search-result>img").attr("src", `${biz.image_url}`);
  $("#res-name").html(`${biz.name}`);
  $("#rating").html(`${biz.rating}`);
  $("#review-count").html(`${biz.review_count} reviews `);
  $("#price").html(`${biz.price}`);
  $("#categories").html(`${biz.categories}`);
  $("#address").html(`${biz.address}`);
  $("#res-details").attr("href", `${biz.url}`);
  $("#res-details").attr("style", "display: block");
}

function showResList() {
  let biz = resultYelp[resultIndex];
  showRes(biz);  
  let color = biz.liked ? "darkblue" : "gray"  
  $("#thumbs-up").attr("style", "display: inline; color:" + color);  
  $("#resultBtn").attr("style", "display: inline;")
}

$("#nextBtn").on("click", () => {
  resultIndex++;
  resultIndex %= 5;
  showResList();
});

$("#thumbs-up").on("click", () => {
  let biz = resultYelp[resultIndex];
  $.get(`/like/${biz.id}`, (res) => {
    let color = res.liked ? "darkblue" : "gray"  
    $("#thumbs-up").attr("style", "display: inline; color:" + color); 
  })
});

$("#resultBtn").on("click", () => {
  // $("#search-result").attr("style", "display: none");
  // $("#search-form").attr("style", "display: none");
  $.get('/vote-result.json', (res) => {
    $("#thumbs-up").attr("style", "display: none ");  
    $("#resultBtn").attr("style", "display: none");
    $("#nextBtn").attr("style", "display: none");
    let biz = res;
    $("#vote-result").attr("style", "display: block");
    showRes(biz);
  })  
})


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
    showResList();
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
