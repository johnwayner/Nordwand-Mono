.PHONY: install build build-otf build-nerd-font install-mac

# Newest release tag, not the nearest ancestor: release tags sit on main, so
# from dev the nearest one lags behind.
FONT_VERSION ?= $(shell git tag --sort=-v:refname 2>/dev/null | head -1 | grep . || echo 1.0.0)
# Fork marker, appended to the version string (shown in Font Book) so a
# custom build is never mistaken for an upstream release.
VERSION_NOTE ?= johnwayner/Nordwand-Mono $(shell git rev-parse --abbrev-ref HEAD) $(shell git rev-parse --short HEAD)$(shell git diff --quiet HEAD || echo -dirty)

install:
	uv sync

build:
	uv run python -m generate_font --font-version $(FONT_VERSION) --version-note "$(VERSION_NOTE)" --web-font
	uv run python -m scripts.banner
	uv run python -m scripts.specimen_pdf
	uv run python -m scripts.samples
	uv run python -m scripts.alternatives_markdown

build-font:
	uv run python -m generate_font --font-version $(FONT_VERSION) --version-note "$(VERSION_NOTE)" --web-font

build-otf:
	uv run python -m generate_font --font-version $(FONT_VERSION) --version-note "$(VERSION_NOTE)" --otf

build-nerd-font:
	uv run python -m scripts.nerd_font

# Remove the installed fonts before copying: overwriting them in place
# corrupts the text of any running app that has them open (it keeps the old
# font's tables while reading the new file). Restart those apps afterwards.
install-mac: build-otf
	rm -f ~/Library/Fonts/NordwandMono-*.otf
	cp fonts/otf/NordwandMono-*.otf ~/Library/Fonts
	@echo "Installed. Restart apps using Nordwand Mono (e.g. Emacs) to load it."

visualize:
	open -n -a /Library/Frameworks/Python.framework/Versions/3.12/Resources/Python.app \
    --env "__PYVENV_LAUNCHER__=$PWD/.venv/bin/python" \
    --args -m visualize lowercase_a
