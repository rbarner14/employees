"use static";

function sendAlert(alertMsg){
    
    alert(alertMsg);

}


function addEmployee(evt){
    evt.preventDefault();

    const formInputs = {
        "name": $("#name-field").val(), 
        "state": $("#state-field").val(),
        "dept_code": $("#dept-code-field").val() 
    }

    $.post("/add_employee", formInputs, sendAlert)
}


$("#employee-form").on("submit", addEmployee)