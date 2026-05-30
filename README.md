# sopel-mangadex

A MangaDex plugin for Sopel IRC bots

## Installing

Releases are hosted on PyPI, so after installing Sopel, all you need is `pip`:

```shell
$ pip install sopel-mangadex
```

## Using

`sopel-mangadex` automatically shows information about `mangadex.org` links in
recognized formats:

* Series: `https://mangadex.org/title/<UUID>[/<optional_slug>]`\
  e.g. `https://mangadex.org/title/de900fd3-c94c-4148-bbcb-ca56eaeb57a4/spice-and-wolf`
* Chapter: `https://mangadex.org/chapter/<UUID>[/<optional_page_number>`\
  e.g. `https://mangadex.org/chapter/3fed674e-663f-44d2-bc99-6145600fd46a/7`

### Output examples

#### Series page

```
<Sopel> [MangaDex] Ookami to Koushinryou | Content: 🟢
        | 💯 Completed | Monsters, Animals, Romance, Adventure,
        Fantasy, Slice of Life, Supernatural, Adaptation | Synopsis:
        With his carthorse as his only companion, the young merchant
        Kraft Lawrence slowly wends his way through dusty back roads
        in search of profitable trade. But this monotony screeches to
        a halt when, one night, he encounters a harvest goddess in
        the guise of a beautiful […]
```

#### Chapter link

```
<Sopel> [MangaDex] (unknown title) | Chapter 1, page 7 of Kono Bijutsubu
        ni wa Mondai ga Aru!`
```

This particular chapter doesn't have a title of its own.

### Series title language precedence

This plugin prioritizes romaji (`ja-ro`) titles, then English (`en`), then
finally falls back on Japanese (`ja`). If none of those translations exist, you
will see "Unknown title".

Note that some series may have incorrect language tags that make this logic
appear to break. For example, at time of writing, _Kono Bijutsubu ni wa Mondai
ga Aru!_ from the sample chapter link output above has its romaji title tagged
as `en` instead of `ja-ro`. These cases need to be fixed on the MangaDex side;
trying to detect them in `sopel-mangadex` would be too fiddly.

Chapters only have one (optional) title string, in the language of that
translation.
