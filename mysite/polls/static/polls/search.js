function search() {
    $.ajax({
        url: "/polls/search/response/",
        method: "GET",
        data: { keywords: $("#search").val() }, 
        success: function(data) {
            console.log("data: " + data);
            console.log("data.hits: " + data.hits);
            for (var i = 0; i < data.hits.length; i++) {
                console.log(data.hits[i]);
                $("#results").append("<p>" + data.hits[i] + "</p>");
            }
        }
    });
}

