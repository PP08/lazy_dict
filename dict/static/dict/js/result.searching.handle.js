/**
 * Created by PhucPhuong on 08/10/2016.
 */
// Submit post on submit

$('#scrollable-dropdown-menu').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!") // sanity check
    search();
});


// AJAX for posting
function search() {
    console.log("create post is working!") // sanity check
    $.ajax({
        url : "/dict/search/", // the endpoint
        type : "GET", // http method
        data : { the_post : $('#search-text').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()}, // data sent with the post request

        // handle a successful response
        success : function(json) {

                console.log(json); // log the returned json to the console
                $("#test").prepend("<li><strong>" + json.definition + "</span></li>");
                console.log("success"); // another sanity check
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
};