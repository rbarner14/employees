"use strict";

function showEmployeeJSON(response){
    alert(`Employees in database: ${Object.keys(response)}`)
}

function handleLinkClick(evt){
    evt.preventDefault()

    $.get("/employees_in_db.json", showEmployeeJSON) 
}


// $("#all-employees-link").on('click', handleLinkClick)
$(".employee-alert").on('click', handleLinkClick)