var data = $.get(serializer);

function addData(){
    var row = "";
    row += "<tr><th>" + data.id + "</th><td>" + data.fields.tester +
    "</td><td>" + data.fields.created_at + "</td><td>" + data.fields.environment_id +
    "</td><td>" + data.fields.file + "</td></tr>";

    $(row).appendTo("#result");
}

setTimeout(addData, 4000);
