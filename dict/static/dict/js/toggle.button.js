/**
 * Created by PhucPhuong on 10/10/2016.
 */


$( function() {
    // run the currently selected effect
    function runEffect() {
        // Run the effect
        $( "#effect" ).slideToggle("fast");
    };

    // Set effect from select menu value
    $( "#button" ).on( "click", function() {

        var position = $("#button").position()


        $('html,body').animate({
            scrollTop:  position.top - $("#show-button").height() * 2 - $("#nav").height()
        }, 1000);

        runEffect();
    });
} );