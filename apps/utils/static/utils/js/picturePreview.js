/**
 *    Creates a thumbnail from a html file input using HTML5 File API
 */

+(function(){
    widgets = document.querySelectorAll('div.field__widget--picture-preview');
    widgets.forEach( function(widget)
    {
        var placeholder = widget.querySelector('.placeholder');
        var input = widget.querySelector('input[type=file]');
        var image = placeholder.getAttribute('data-image');
        if(image){
              placeholder.innerHTML = "<img src='" + image + "' />";
        }
        input.addEventListener(
            'change',
            function(e) {
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
