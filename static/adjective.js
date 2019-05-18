"use strict";

function handleGetAdjectives(response){
    // id is adjective, hence the "#".
    $('#adjective').text(response); 
}

// simple usage of $.get that takes in the parameters url and a callback
// function which we have specified above
$.get("/adjective", handleGetAdjectives) 