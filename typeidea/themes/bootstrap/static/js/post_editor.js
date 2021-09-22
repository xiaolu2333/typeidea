$(document).ready(function () {
    (function ($) {
        var $content_md = $("div[class~='field-content_md']");
        var $content_ck = $("div[class~='field-content_ck']");
        var $is_md = $('#id_is_md'); //id="id_is_md"
        $is_md.css("background-color", "#7ee0c9");
        var switch_editor = function (is_md) {
            if (is_md) {
                $content_md.show();
                $content_ck.hide();
            } else {
                $content_md.hide();
                $content_ck.show();
            }
        }
        // switch_editor($is_md.is(':checked'));
        $is_md.on('click', function () {
            switch_editor($(this).is(':checked'));
        });
    })(django.jQuery);
});


