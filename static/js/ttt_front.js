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
        } else {
            $(".nav_menu ul").css({
                "position": "static",
                "background-color": "black",
                "border-style": "none"
            });
        }
    });
});