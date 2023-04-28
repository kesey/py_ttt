$(document).ready(function() {
    $(window).scroll(function (event) { // keep menu on top
        var scroll = $(window).scrollTop();
        if (scroll > 145) {
            $(".nav_menu ul").css({
                "position": "fixed",
                "top": "0px",
                "background-color": "rgba(0, 0, 0, 0.75)",
                "border-style": "double",
                "border-color": "white",
                "border-radius": "5px",
                "z-index": "999"
            });
            $(".anchor").css("visibility", "visible");
        } else {
            $(".nav_menu ul").css({
                "position": "static",
                "background-color": "black",
                "border-style": "none"
            });
            $(".anchor").css("visibility", "hidden");
        }
    });

    $(function() { // highlight navigation menu depends on url
        // this will get the full URL at the address bar
        var url = window.location.href;
        url = url.split("?page")[0]; // usefull for pagination
        // passes on every "a" tag
        $(".nav_menu a").each(function() {
            // checks if its the same on the address bar
            if (url == (this.href)) {
                $(this).closest("li").addClass("active");
            } else {
                $(this).closest("li").removeClass("active");
            }
        });
    });

    $("img.zoom").on( "click", function() { // zoom image
        if ($(this).hasClass("zoom_in")) {
            $(this).removeClass("zoom_in");
            $(this).parent().addClass("col-4 right_align");
            $(this).parent().next().addClass("left_align");
            $(this).parent().next().removeClass("center");
        } else {
            $(this).addClass("zoom_in");
            $(this).parent().removeClass("col-4 right_align");
            $(this).parent().next().addClass("center");
            $(this).parent().next().removeClass("left_align");
        };
    });
});