/**
 * Created by PhucPhuong on 08/10/2016.
 */
// Submit post on submit

// for set cursor on input when the page is loaded
$('input[name=searchInput]').focus();

$('#scrollable-dropdown-menu').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!");// sanity check
    search();
});


// AJAX for posting
function search() {
    $.ajax({
        url : "dict/search/", // the endpoint
        type : "POST", // http method
        data : { query : $('#search-text').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()}, // data sent with the post request

        // handle a successful response
        success : function(data) {

            // window.scrollTo(0, 0);

            $('body').animate({
                scrollTop:  -1000
            }, 1000);

            $('.typeahead').typeahead('close');

            // $('#button').removeClass('hidden');// show button

            console.log(data); // log the returned json to the console
            var table = document.getElementById('inflected-table');

            if(data.wdefinition){
                var definition = document.getElementById('definition');
                var definition_template = Handlebars.compile(document.getElementById('definition-template').innerHTML);
                definition.innerHTML = definition_template(data);
                console.log("have a definition");


                if(data.search_query.toString().split(' ').length > 1){
                    console.log("more than a word");
                    $('#button').addClass('hidden');
                    // TODO: handle exception when search query more than a word..
                    table.innerHTML = "<div class='container'><i>the word(s) have no inflected form..</i></div>"
                }
                else{
                    $('#button').removeClass('hidden');
                    if (data.classifier == 'NOUN' || data.classifier == 'NPRO' ){

                        var noun_template = Handlebars.compile(document.getElementById('noun-template').innerHTML);

                        table.innerHTML = noun_template(data);

                        console.log("success"); // another sanity check
                    } else if(data.classifier == 'ADJF'){

                        var adj_template = Handlebars.compile(document.getElementById('adj-template').innerHTML);
                        table.innerHTML = adj_template(data);

                    } else if(data.classifier == 'NUMR'){

                        var num_template = Handlebars.compile(document.getElementById('num-template').innerHTML);
                        table.innerHTML = num_template(data);

                    } else if(data.classifier == 'INFN' || data.classifier == 'VERB'){

                        var verb_template = Handlebars.compile(document.getElementById('verb-template').innerHTML);
                        table.innerHTML = verb_template(data)

                    } else {
                        console.log("neither noun nor adj!"); // another sanity check
                        table.innerHTML = "<div class='container'><i>the word(s) have no inflected form..</i></div>"
                    }


                    // TODO: when the word is adj and verb..
                    // create new template for verb,
                    //
                }

            } else {
                $('#button').addClass('hidden');
                var definition = document.getElementById('definition');
                var definition_template = Handlebars.compile(document.getElementById('definition-template').innerHTML);
                definition.innerHTML = definition_template(data);
            }
        },

            // handle a non-successful response
        error : function(xhr, errmsg, err) {
                console.log("error");
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    "<a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
};