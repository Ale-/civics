from civics.settings import DOCUMENT_TITLE, DOCUMENT_DESCRIPTION

def site_info_processor(request):
    """Injects into global context information about the site"""

    document_title       = DOCUMENT_TITLE
    document_description = DOCUMENT_DESCRIPTION

    return locals()
