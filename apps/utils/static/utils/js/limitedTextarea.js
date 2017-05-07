/**
 *    Creates a thumbnail from a html file input using HTML5 File API
 */

+(function()
{
    widgets = document.querySelectorAll('.field__widget--limited-textarea');
    widgets.forEach( function(widget) {
        var input = widget.querySelector('textarea');
        // Initial value for forms with errors
        var chars = input.value.length;
        widget.querySelector('.textarea-count').innerHTML = chars;
        // Watch over user input
        input.addEventListener(
            'keyup',
            function(e) {
                chars = input.value.length;
                widget.querySelector('.textarea-count').innerHTML = chars;
            },
        false);
    });
})();
