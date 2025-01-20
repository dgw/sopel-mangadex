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


@plugin.url(r'https://mangadex.org/chapter/(?P<uuid>[0-9a-f-]+)(?:/(?P<page>[0-9]+))?')
@plugin.output_prefix(OUTPUT_PREFIX)
def manga_chapter_link(bot, trigger):
    client = mangadex.series.Chapter()

    try:
        chapter = client.get_chapter_by_id(trigger.group('uuid'))
    except md_errors.ApiError:
        bot.reply('Error fetching chapter information')
        return

    client = mangadex.series.Manga()
    try:
        manga = client.get_manga_by_id(chapter.manga_id)
    except md_errors.ApiError:
        bot.reply('Error fetching manga information for chapter')
        return

    chapter_number = chapter.chapter
    if chapter_number.is_integer():
        chapter_number = int(chapter_number)

    manga_title = manga.title.get('en', manga.title.get('ja', 'Unknown title'))

    parts = []
    parts.append(
        getattr(chapter, 'title', '(unknown title)') or '(unknown title)'
    )
    if page := trigger.group('page'):
        parts.append(f'Chapter {chapter_number}, page {page} of {manga_title}')
    else:
        parts.append(f'Chapter {chapter_number} of {manga_title}')

    bot.say(
        ' | '.join(part for part in parts if part),  # skip empty strings,
        truncation=' […]',
    )
