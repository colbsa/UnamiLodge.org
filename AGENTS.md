# AGENTS.md

This file provides guidance to coding agents when working with this repository.

## What this is

A [Jekyll](https://jekyllrb.com/) static site for **Unami Lodge, One** (Order of the Arrow, Cradle of Liberty Council). Content is almost entirely Markdown pages + YAML data; there is no application backend. Most edits are content changes (posts, page copy, data records), not code.

- Production: https://unamilodge.org
- Development/staging: https://dev.unamilodge.org

## Common commands

Local development is easiest via the Docker image (avoids installing Ruby + the `vips`/`imagemagick` native deps that `jekyll_picture_tag` needs):

```sh
docker build --platform linux/amd64 --build-arg JEKYLL_BASEURL=/ -t jekyll .
docker run --rm -v ${PWD}:/srv/jekyll -p 4000:4000 jekyll serve --host 0.0.0.0
```

Serves at http://127.0.0.1:4000. Rebuild the image after changing `Gemfile`/`Gemfile.lock`. The explicit `linux/amd64` platform avoids an Apple Silicon Alpine/protobuf native extension failure, and `JEKYLL_BASEURL=/` prevents the final Dockerfile build step from invoking `jekyll build -b` with an empty value.

> Note: `dockerfile` ends with two `COPY . /srv/jekyll` + `jekyll build` lines used by the DigitalOcean App Platform build. The README notes those two lines should be deleted for a local build but **never committed** deleted.

Native (if Ruby + Bundler + libvips/imagemagick are installed):

```sh
bundle install
bundle exec jekyll serve   # or: bundle exec jekyll build
```

Production/server Bundler installs should exclude the local test group:

```sh
bundle config set without test
bundle install
```

Set `bundle config set without test` once on each server as a persistent local Bundler
setting. Do not put that command in the deploy workflows; deploys use `script_stop: true`,
so a missing `bundle` executable would abort before `git pull`.

Use Ruby 3.x for local work. The current `jekyll_picture_tag` dependency does not support Ruby 4. On Homebrew macOS, `ruby@3.4` works:

```sh
/opt/homebrew/opt/ruby@3.4/bin/gem install bundler -v 2.5.11
/opt/homebrew/opt/ruby@3.4/bin/bundle _2.5.11_ config set path .bundle
/opt/homebrew/opt/ruby@3.4/bin/bundle _2.5.11_ install
```

### Tests

Run the local test suite with:

```sh
script/test
```

`script/test` runs a full `jekyll build` and then a Minitest suite against the generated `_site` output. The tests cover core generated pages, data-generated chapter pages, news post output slugs, news image references, Jekyll Picture Tag output, and a few key rendered pages for unexpanded Liquid.

Before dependency upgrades, run `script/test` on the current branch to establish the baseline. After changing `Gemfile`, `Gemfile.lock`, CDN dependencies, Jekyll plugins, Docker build behavior, or layout/include behavior, run `script/test` again and compare the result before considering the change safe.

The current lockfile intentionally keeps precompiled native platforms for `ffi` 1.17.4
and `google-protobuf` 4.33.6 so Linux Docker/server builds do not compile those gems from
generic Ruby packages.

## Deployment (important branch semantics)

Deploy is via GitHub Actions that SSH into the web servers and `git reset --hard && git pull` — the server builds the site, not CI.

- `.github/workflows/dev.yml` → triggers on push to **`development`** → deploys to dev.unamilodge.org
- `.github/workflows/prod.yml` → triggers on push to **`master`** → deploys to production

The default working branch is `development`. Changes flow through `development` (staging) first, then to `master`/production. Any push to these branches deploys immediately, so treat commits to them as publishes.

## Architecture

### Content lives in three places
- **Root-level Markdown pages** (`about-*.md`, `history-*.md`, `membership-*.md`, `leadership-*.md`, `kb*.md`, `portal-*.md`, etc.). Filenames are topic-prefixed for grouping; the URL comes from each file's `permalink` front matter, not its filename. To find the source for a page, grep front matter for the `permalink` rather than guessing from the path.
- **News posts** in `_posts/news/` (`YYYY-MM-DD-Title.md`). Permalink pattern is `/news/:title/` (see `_config.yml`), paginated 9/page via `jekyll-paginate-v2`. Posts use front matter `banner`, `thumbnail`, `excerpt`, and an optional `event:` block. Images resolve from `/img/posts/`, `/img/posts/banners/`, `/img/posts/thumbs/`.
  - Known gotcha (see README TODO): two posts with the same slug/title overwrite each other at build time.
- **Data** in `_data/*.yml` (and one `.csv`) drives the data-heavy pages. Pages read these with Liquid (e.g. chapter meeting info, officers, awards, events, LEC roster, reports). Editing lodge facts usually means editing a `_data` file, not a page.

### Layouts and includes
- `_layouts/` — `page`, `post`, `post-list`, `index`, `chapters`, `portal`, `links`, `error`. A page selects its shell via `layout:` front matter.
- `_includes/` — reusable sections (`section_slider`, `section_banner`, `section_button-bar`, `section_news-preview-*`, `page_head`, `page_footer`).

### Generated chapter pages (custom plugin)
`_plugins/data_page_generator.rb` generates one page per record in a data file at build time. Configured under `page_gen:` in `_config.yml`: it reads `_data/chapters.yml` and renders each chapter through the `chapters` layout at `/chapters/<email>/` (the `email` field is used as the URL slug). To change a chapter's meeting location/time, officers, or ZIP coverage, edit the record in `_data/chapters.yml` — do not create a page by hand. The plugin exposes a `datapage_url` Liquid filter for linking to generated pages.

### Images
Handled by `jekyll_picture_tag` (config in `_data/picture.yml`), which compresses/resizes at build time — this is why the build needs `vips`/`imagemagick`. Standard sizes: post thumbnails 800×800, post banners 800×345, homepage sliders 4500×1500, portals 4500×900. Standardized on PNG. Downloadable PDFs live in `files/`.

## Conventions

- Prefer Markdown over raw HTML wherever possible (README). Liquid is used only in layouts/includes/plugins, not in normal content pages.
- When adding a post, copy the closest existing post in `_posts/news/` as a template; `thumbnail` and `excerpt` are effectively required, `banner` is optional.
