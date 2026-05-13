
import logging
from manatus.source_resource import SourceResource

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.debug(f'Loaded {__name__} map')


def tind_marc_map(rec):
    sr = SourceResource()
    tn = None

    # Identifier (required)
    print(rec.harvest_id) # test
    sr.identifier = rec.harvest_id

    # Title (required)
    if rec.title:
        sr.title = rec.title
    else:
        logger.error(f"Rejected (no title): {rec.harvest_id}")
        return None

    # Contributor / Creator
    if rec.creator:
        sr.creator = [{"name": n} for n in rec.creator]

    if rec.contributor:
        sr.contributor = [{"name": n} for n in rec.contributor]

    # Date
    if rec.date:
        sr.date = [{"displayDate": rec.date}]

    # Description
    if rec.description:
        sr.description = rec.description

    # Format
    if rec.format:
        sr.format = rec.format

    # Language
    if rec.language:
        # language may be string or list; normalize
        if isinstance(rec.language, (list, tuple)):
            sr.language = [{"name": l} for l in rec.language]
        else:
            sr.language = [{"name": rec.language}]

    # Place (spatial)
    if rec.place:
        sr.spatial = [{"name": rec.place}]

    # Publisher
    if rec.publisher:
        sr.publisher = rec.publisher

    # Subjects
    if rec.subject:
        sr.subject = rec.subject

    # Type (336 / Leader)
    if rec.type:
        sr.type = rec.type

    # Rights (required)
    if rec.rights:
        if isinstance(rec.rights, str) and rec.rights.startswith("http"):
            sr.rights = [{"@id": rec.rights}]
        else:
            sr.rights = [{"text": rec.rights}]
    else:
        logger.error(f"Rejected (no rights): {rec.harvest_id}")
        return None

    # isShownAt (required landing page)
    if getattr(rec, "shown_at", None):
        sr.isShownAt = rec.shown_at
    else:
        logger.error(f"Rejected (no landing page): {rec.harvest_id}")
        return None

    # Thumbnail / preview
    if getattr(rec, "thumbnail", None):
        tn = rec.thumbnail

    # Provider info (SSDN fixed)
    sr.provider = {"name": "Sunshine State Digital Network"}

    if getattr(rec, "data_provider", None):
        sr.dataProvider = {"name": rec.data_provider}

    print(sr.data) # test
    #temp testing
    assert "identifier" in sr.data
    assert "rights" in sr.data
    assert "isShownAt" in sr.data

    yield sr, tn
