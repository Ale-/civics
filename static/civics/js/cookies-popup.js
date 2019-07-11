/**
 *   Cookies popup javascript
 */

/**
 *  Add event listeners when DOM is completely loaded
 *  equivalent to $(document).ready()
 */
document.addEventListener("DOMContentLoaded", function()
{
    var consent = localStorage.getItem('cookie-consent') == 'true';

    if(!consent){
        var popup_template = document.querySelector('#cookies-popup');
        var popup_content  = document.importNode(popup_template.content, true);
        document.body.appendChild(popup_content);
        document.querySelector('#cookie-consent').addEventListener('click', dismiss);
    }

    function dismiss(){
        // Store consent in local storage
        localStorage.setItem('cookie-consent', 'true');
        // Remove popup
        var popup = document.querySelector('.cookies-popup');
        document.body.removeChild(popup);
        // Add piwik
        _paq.push(['trackPageView']);
        _paq.push(['enableLinkTracking']);
        (function() {
          var u="//analytics.wwb.cc/";
          _paq.push(['setTrackerUrl', u+'piwik.php']);
          _paq.push(['setSiteId', '3']);
          var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
          g.type='text/javascript'; g.async=true; g.defer=true; g.src=u+'piwik.js'; s.parentNode.insertBefore(g,s);
        })();
    }
});
