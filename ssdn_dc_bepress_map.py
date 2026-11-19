import logging

from manatus import SourceResource

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.debug(f'Loaded {__name__} map')


def ssdn_dc_bepress_map(rec):
    sr = SourceResource()

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
    if rec.date not in (None, '', []):
        sr.date = {
            'begin': rec.date,
            'end': rec.date,
            'displayDate': rec.date
        }
    else:
        logger.info(f"No date - {rec.harvest_id}")

    # description / thumbnail
    #
    # Bepress DC maps the thumbnail URL to a dc:description field.
    # Checking against `https://digitalcommons` can redirect the URL
    # into the tn variable for hosted Bepress users.
    #
    tn = None

    try:
        description_list = []

        for desc in rec.description:
            if desc.startswith('https://digitalcommons'):
                tn = desc
            else:
                description_list.append(desc)

        if description_list:
            sr.description = description_list

    except TypeError:
        pass

    # format
    sr.format = rec.format

    # identifier
    try:
        for identifier in rec.identifier:
            if identifier.startswith('http'):
                sr.identifier = identifier
                break
    except TypeError:
        logger.warning(f"No identifier - {rec.harvest_id}")

    # language
    try:
        sr.language = [
            {'name': lang}
            for lang in rec.language
        ]
    except TypeError:
        logger.info(f"No language - {rec.harvest_id}")

    # place
    if rec.place:
        sr.spatial = [
            {'name': place}
            for place in rec.place
        ]

    # publisher
    sr.publisher = rec.publisher

    # rights
    try:
        rights_uris = [
            r for r in rec.rights
            if r and r.startswith('http')
        ]

        if rights_uris:
            sr.rights = [{
                '@id': rights_uris[0]
            }]
        else:
            logger.warning(
                f"No rights URI - {rec.harvest_id}"
            )

            if rec.rights:
                sr.rights = [{
                    'text': rec.rights[0]
                }]

    except TypeError:
        logger.error(f"No rights - {rec.harvest_id}")
        return None

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

    yield sr, tn
