$(window).on('load', function(){
    var data = {}; //

    setTimeout(getData, 14000)  // wait for task

    function getData(){
        $.getJSON('http://localhost:8000/response/', function(result){
            data = result;
            addData();
        });
    }
    function addData(){
        var row = "";
        if (data.test_status == 'PASSED'){
            row += "<tr class='table-success'><th scope='row'>" + data.id+ "</th><td>" + data.tester+ "</td><td>" +
            data.created_at + "</td><td>" + data.environment_id + "</td><td>" + data.file +
            "</td><td>" + data.test_log + "</td><td>" + data.test_status + "</td></tr>";
        } else if (data.test_status == 'FAILED'){
            row += "<tr class='table-danger'><th scope='row'>" + data.id+ "</th><td>" + data.tester+ "</td><td>" +
            data.created_at + "</td><td>" + data.environment_id + "</td><td>" + data.file +
            "</td><td>" + data.test_log + "</td><td>" + data.test_status + "</td></tr>";
        } else if (data.test_status == 'PENDING'){
            row += "<tr class='table-warning'><th scope='row'>" + data.id+ "</th><td>" + data.tester+ "</td><td>" +
            data.created_at + "</td><td>" + data.environment_id + "</td><td>" + data.file +
            "</td><td>" + data.test_log + "</td><td>" + data.test_status + "</td></tr>";
        }
        $(row).appendTo("#itemTable tbody");
    }
});