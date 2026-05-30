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


def _get_preferred_manga_title(
    manga: mangadex.series.Manga,
) -> str | None:
    # How the library handles titles (if not the underlying API; I didn't look)
    # is pretty annoying. The title and altTitles attributes are dictionaries of
    # language codes to title strings, and there are TWO attributes where you
    # might find the language code you prefer.
    all_titles = {}
    for alt_title in manga.altTitles:
        all_titles.update(alt_title)
    # Do the main title last so it takes precedence over altTitles if there are
    # duplicates, e.g. Konobi's romaji title is (2026-05-30) wrongly tagged as
    # `en`. This prioritizes matching what the user will likely see on-site.
    all_titles.update(manga.title)
    return (
        all_titles.get('ja-ro') or all_titles.get('en') or all_titles.get('ja')
    )


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
    parts.append(_get_preferred_manga_title(manga) or 'Unknown title')
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

    manga_title = _get_preferred_manga_title(manga) or 'Unknown title'

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
