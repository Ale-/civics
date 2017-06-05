'use strict'

/**
 *  JS Asset needed to run video-loader widgets
 */

+(function(){
    var widgets = document.querySelectorAll('div.field__widget--video');
    widgets.forEach(function(widget){
        var input       = widget.querySelector('input');
        var placeholder = widget.querySelector('.placeholder');
        if(input.value){
            html = createIframe(input.value, placeholder.dataset.width, placeholder.dataset.height);
            widget.querySelector('.placeholder').innerHTML = html;
        }
        widget.querySelector('.video-widget__submit').addEventListener('click', function(){
            html = createIframe(input.value, placeholder.dataset.width, placeholder.dataset.height);
            widget.querySelector('.placeholder').innerHTML = html;
        });
    });
})();
