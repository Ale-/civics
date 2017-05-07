/**
 *    Creates a thumbnail from a html file input using HTML5 File API
 */

+(function(){
    widgets = document.querySelectorAll('div.field__widget--picture-preview');
    widgets.forEach( function(widget)
    {
        var input = widget.querySelector('input');
        input.addEventListener(
            'change',
            function(e) {
                var placeholder = widget.querySelector('.placeholder');
                if (input.files && input.files[0])
                {
                  var reader = new FileReader();
                    reader.onload = function(e) {
                        placeholder.innerHTML = "<img src='" + e.target.result + "' />";
                    }
                    reader.readAsDataURL(input.files[0]);
                }
            },
        false);
    });
})();
