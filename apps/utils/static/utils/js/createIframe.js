'use strict'

/**
 *   create_iframe
 *   Returns the iframe code needed to render a video hosted in Vimeo or YouTube
 *   @ param url  Absolute url of the resource to be embedded
 */

 function createIframe(url, width, height)
 {
     var uri      = url.split('://')[1];
     var service  = uri.split('/')[0];
     if( url ){
         switch(service) {
               case 'vimeo.com':
               var resource = uri.split('/')[1];
               return '<iframe src="https://player.vimeo.com/video/' + resource + '" width="' + width + '" height="' + height + '" \
                       frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>';
               break;

               case 'www.youtube.com':
               var resource = uri.split('?v=')[1];
               return '<iframe src="https://www.youtube.com/embed/' + resource + '" width="' + width + '" height="' + height + '" \
                       frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>';
               break;
         }
     }
     return null;
 }
