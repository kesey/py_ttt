$(document).ready(function() {
    $(window).scroll(function (event) { // keep menu on top
        var scroll = $(window).scrollTop();
        if (scroll > 145) {
            $(".anchor").css("visibility", "visible");
            $(".save_list_exemplaire").css("visibility", "visible");
        } else {
            $(".anchor").css("visibility", "hidden");
            $(".save_list_exemplaire").css("visibility", "hidden");
        }
    });
});