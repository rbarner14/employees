"use static";

function sendAlert(alertMsg){
    
    alert(alertMsg);

    $("#new-list").load("/api2/employee")

}


function addEmployee(evt){
    evt.preventDefault();

    // const formInputs = {
    //     "name": $("#name-field").val(), 
    //     "state": $("#state-field").val(),
    //     "dept_code": $("#dept-code-field").val() 
    // }

    const formValues = $("#employee-form").serialize();

    // $.post("/add_employee", formInputs, sendAlert)

    $.post("/add_employee", formValues, sendAlert)
}


$("#employee-form").on("submit", addEmployee)