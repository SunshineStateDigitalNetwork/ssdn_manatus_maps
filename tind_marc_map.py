
import logging
from manatus.source_resource import SourceResource

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.debug(f'Loaded {__name__} map')


def tind_marc_map(rec):
    sr = SourceResource()
    tn = None

    # identifier (required)
    if rec.is_shown_at:
        sr.identifier = rec.is_shown_at
    else:
        logger.error(f"No identifier - {rec.harvest_id}")
        return None

    # title (required)
    if rec.titles:
        sr.title = rec.titles
    else:
        logger.error(f"No title - {rec.harvest_id}")
        return None

    # contributor / creator
    if rec.creator:
        sr.creator = [{"name": n} for n in rec.creator]

    if rec.contributor:
        sr.contributor = [{"name": n} for n in rec.contributor]

    # date
    try:
        sr.date = {'begin': rec.date,
                   'end': rec.date,
                   'displayDate': rec.date}
    except TypeError:
        logger.info(f"No date - {rec.harvest_id}")

    # description
    if rec.description:
        sr.description = rec.description

    # format
    if rec.format:
        sr.format = [rec.format.lower()]

    # language
    if rec.language:
        # language may be string or list; normalize
        if isinstance(rec.language, (list, tuple)):
            sr.language = [{"name": l} for l in rec.language]
        else:
            sr.language = [{"name": rec.language}]

    # place (spatial)
    if rec.place:
        sr.spatial = [{"name": rec.place}]

    # publisher
    if rec.publisher:
        sr.publisher = [rec.publisher]

    # subjects
    if rec.subject:
        sr.subject = rec.subject

    # type (336 / Leader)
    if rec.type:
        sr.type = [rec.type.lower()]

    # rights (required)
    if rec.rights:
        if isinstance(rec.rights, str) and rec.rights.startswith("http"):
            sr.rights = [{"@id": rec.rights}]
        else:
            sr.rights = [{"text": rec.rights}]
    else:
        logger.error(f"No rights - {rec.harvest_id}")
        return None

    # thumbnail / preview
    if getattr(rec, "thumbnail", None):
        tn = rec.thumbnail

    yield sr, tn
