"""sopel-mangadex

A MangaDex plugin for Sopel IRC bots
"""
from __future__ import annotations

import mangadex
from mangadex import errors as md_errors

from sopel import plugin


OUTPUT_PREFIX = '[MangaDex] '
RATING_VALUES = {
    'safe': '🟢',
    'suggestive': '🟡',
    'erotica': '🔴',
    'pornographic': '🔞',
}
STATUS_VALUES = {
    'ongoing': '🖨️ Ongoing',
    'completed': '💯 Completed',
    'hiatus': '⏳ Hiatus',
    'cancelled': '🚫 Cancelled',
}


@plugin.url(r'https://mangadex.org/title/(?P<uuid>[0-9a-f-]+)(?:/(?P<slug>[0-9a-z-]+))?')
@plugin.output_prefix(OUTPUT_PREFIX)
def manga_title_link(bot, trigger):
    client = mangadex.series.Manga()

    try:
        manga = client.get_manga_by_id(trigger.group('uuid'))
    except md_errors.ApiError:
        bot.reply('Error fetching manga information')
        return

    parts = []
    parts.append(manga.title.get('en', manga.title.get('ja', 'Unknown title')))
    parts.append(f'Content: {RATING_VALUES[manga.contentRating]}')
    parts.append(STATUS_VALUES[manga.status])
    parts.append(', '.join(tag.name.get('en') for tag in manga.tags))
    parts.append(
        'Synopsis: ' + manga.description.get(
            'en', manga.description.get(
                'ja', '(no description available)'
            )
        )
    )

    bot.say(
        ' | '.join(part for part in parts if part),  # skip empty strings
        truncation=' […]',
    )
