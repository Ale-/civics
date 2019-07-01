/**
 *   SDG popup javascript
 */

/**
 *  Add event listeners when DOM is completely loaded
 *  equivalent to $(document).ready()
 */
document.addEventListener("DOMContentLoaded", function()
{
    var popup = document.querySelector('.ods-popup');
    var first_time = !(localStorage.getItem('sdg_popup_firsttime') == 'false');
    if(first_time){
        popup.classList.remove('hidden');
    }
    popup.addEventListener('click', i=>{
        popup.classList.add('hidden');
        localStorage.setItem('sdg_popup_firsttime', 'false')
    });
});
