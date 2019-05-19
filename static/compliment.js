"use strict";

function giveCompliment(response){

    const niceWords = response;

    $('#compliment').html(niceWords);
}


function getCompliment(){

    $.get('/compliment', {compliment: "Yes"}, giveCompliment);

}


$("#give-compliment").on('click', getCompliment);

