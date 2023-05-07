$(document).ready(function() {
    $(window).scroll(function (event) { // keep menu on top
        var scroll = $(window).scrollTop();
        if (scroll > 145) {
            $(".anchor").css("visibility", "visible");
            $(".copy_button, .paste_button, .save_button").css("visibility", "visible");
        } else {
            $(".anchor").css("visibility", "hidden");
            $(".copy_button, .paste_button, .save_button").css("visibility", "hidden");
        }
    });

    function color_tr(value, html_element) {
        var val = parseInt(value);
        switch(val){
            case 1:
                html_element.closest("tr").css("background", "rgba(255, 255, 117, 0.4)");
                break;
            case 2:
                html_element.closest("tr").css("background", "rgba(255, 51, 51, 0.3)");
                break;
            case 3:
                html_element.closest("tr").css("background", "rgba(131, 255, 131, 0.4)");
                break;
            case 4:
                html_element.closest("tr").css("background", "rgba(255, 153, 51, 0.4)");
                break;
            case 5:
                html_element.closest("tr").css("background", "rgba(255, 153, 255, 0.4)");
                break;
            default:
                html_element.closest("tr").css("background", "initial");
        };
    };

    $(".etat_exemplaire select").each(function() {
        var value = parseInt($(this).val());
        color_tr(value, $(this));
    });

    $(".etat_exemplaire select").change(function() {
        var value = parseInt($(this).val());
        color_tr(value, $(this));
    });

    $(".exemplaire_table tbody tr").focusin(function() {
        $(this).css("border", "2px solid #337ab7");
    });

    $(".exemplaire_table tbody tr").focusout(function() {
        $(this).css("border", "none");
    });

    let copyBuffer = new Array();

    $("#copyButt").click(function () {
        $("input[name=copy]").each(function() {
            if ($(this).is(":checked")) {
                $(this).closest(".exemplaire_tr")
                    .find("input:not(.numero_exemplaire):not([type=hidden]), select, textarea")
                    .each(function() {
                        var name = $(this).attr("name").split("-");
                        copyBuffer[name[name.length - 1]] = $(this).val();
                    });
                $(this).prop("checked", false);
            };
            $(this).attr({
                type: 'checkbox',
                name: 'paste'
            });
        });
    });

    $("#pasteButt").click(function () {
        $("input[name=paste]:checked").each(function() {
            $(this).closest(".exemplaire_tr")
                .find("input:not(.numero_exemplaire):not([type=hidden]), select, textarea")
                .each(function() {
                    var name = $(this).attr("name").split("-");
                    $(this).val(copyBuffer[name[name.length - 1]]);
                    if ($(this).parent().attr("class") === "etat_exemplaire") {
                        color_tr($(this).val(), $(this));
                    }
                });
            $(this).prop("checked", false);
        });
        $("input[name=paste]").each(function() {
            $("input[name=paste]").attr({
                type: 'radio',
                name: 'copy'
            });
        });
    });
});