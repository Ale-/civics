from django.conf import settings

def site_info_processor(request):
    """Injects into global context information about the site"""

    document_title       = settings.DOCUMENT_TITLE
    document_description = settings.DOCUMENT_DESCRIPTION

    return locals()

def debug_processor(request):
    """Injects debug flag into context"""

    debug    = settings.DEBUG
    debug_js = settings.DEBUG_JS
    print(debug_js)

    return locals()
