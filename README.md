# dimarkov.github.io

Personal website for Dimitrije Marković — independent researcher, ML/AI consultant.

Live at <https://di.markov.icu>.

## Stack

- [Jekyll](https://jekyllrb.com/) on GitHub Pages
- SCSS for styling
- `_data/publications.yml` + `_data/projects.yml` as content sources
- GitHub Actions workflow refreshes star counts weekly (uses `uv` with PEP 723 inline deps)

## Local development

```bash
bundle install
bundle exec jekyll serve --livereload
# → http://localhost:4000
```

## Content updates

- **New publication:** add a YAML entry to `_data/publications.yml`. Set `featured: true` to show it on the home page (currently 5 entries are featured).
- **New / removed project:** edit `_data/projects.yml`. Manual fields are `repo`, `name`, `description`, `pinned`. Star counts auto-refresh weekly via `.github/workflows/sync-stars.yml`.
- **New blog post:** drop a Markdown file into `_posts/` using the standard `YYYY-MM-DD-slug.markdown` convention. A `blog.md` index page is not yet wired up — add one when the first post lands.

## Star-sync script tests

The Python script that updates star counts has unit tests. Run them with `uv`:

```bash
uv run .github/scripts/test_sync_stars.py
```
