$(document).ready(function(){
    $("#form").submit(function(e)
    {
        // fade out form then submit
        e.preventDefault();
        $(".container").fadeOut("slow", function()
        {
            $("#form").off("submit").submit();
        });
    });
    
    // fade in container and footer
    $(".container").fadeIn("slow");
    $(".footer").fadeIn("slow");
    
    // fade out and go to home page when back button is clicked
    $("#back-button").click(function(e)
    {
        // fade out footer and container then go to home page
        e.preventDefault();
        $(".footer").fadeOut("slow");
        $(".container").fadeOut("slow", function()
        {
            window.location = "/"
        });
        
    });
    
    // fade out and go to about page when "Learn More" is clicked
    $("#about").click(function(e)
    {
        // fade out footer and container then go to about page
        e.preventDefault();
        $(".footer").fadeOut("slow");
        $(".container").fadeOut("slow", function()
        {
            window.location = "/about"
        });
        
    });
});