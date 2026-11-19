import logging
import re

from manatus import SourceResource

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.debug(f'Loaded {__name__} map')


def martin_county_dc_map(rec):
    sr = SourceResource()

    item_hash = None

    # contributor
    if rec.contributor:
        sr.contributor = [
            {'name': contributor}
            for contributor in rec.contributor
        ]

    # creator
    if rec.creator:
        sr.creator = [
            {'name': creator}
            for creator in rec.creator
        ]

    # date
    try:
        sr.date = {
            'begin': rec.date[0],
            'end': rec.date[0],
            'displayDate': rec.date[0]
        }
    except TypeError:
        logger.info(f"No date - {rec.harvest_id}")

    # description
    sr.description = rec.description

    # format
    sr.format = rec.format

    # identifier
    try:
        for identifier in rec.identifier:
            if identifier.startswith(
                'https://www.martindigitalhistory.org/items'
            ):
                sr.identifier = identifier

            elif identifier.startswith(
                'https://www.martindigitalhistory.org/files/original'
            ):
                item_hash = identifier.split('/')[5]

    except TypeError:
        logger.error(f"No identifier - {rec.harvest_id}")

    # language
    try:
        sr.language = [
            {'name': lang}
            for lang in rec.language
        ]
    except TypeError:
        logger.info(f"No language - {rec.harvest_id}")

    # spatial
    if rec.place:
        sr.spatial = [
            {'name': place}
            for place in rec.place
        ]

    # publisher
    sr.publisher = rec.publisher

    # rights
    try:
        rights_text = " ".join(rec.rights)

        rights_match = re.search(
            r'https?://rightsstatements\.org/vocab/[A-Za-z\-]+/[0-9.]+/?',
            rights_text
        )

        if rights_match:
            sr.rights = [{
                '@id': rights_match.group(0)
            }]
        else:
            logger.warning(
                f"No rights URI - {rec.harvest_id}"
            )
            sr.rights = [{
                'text': rights_text
            }]

    except TypeError:
        logger.warning(
            f"No rights element - {rec.harvest_id}"
        )

    # subject
    if rec.subject:
        sr.subject = [
            {'name': subject}
            for subject in rec.subject
        ]

    # title
    sr.title = rec.title

    # type
    sr.type = rec.type

    # thumbnail
    try:
        if item_hash:
            tn = (
                "https://www.martindigitalhistory.org/files/thumbnails/"
                f"{item_hash.split('.')[0]}.jpg"
            )
        else:
            tn = None

    except UnboundLocalError:
        tn = None

    yield sr, tn