.PHONY: install build build-otf build-nerd-font install-mac

FONT_VERSION ?= $(shell git describe --tags --abbrev=0 2>/dev/null || echo 1.0.0)

install:
	uv sync

build:
	uv run python -m generate_font --font-version $(FONT_VERSION) --web-font
	uv run python -m scripts.banner
	uv run python -m scripts.specimen_pdf
	uv run python -m scripts.samples
	uv run python -m scripts.alternatives_markdown

build-font:
	uv run python -m generate_font --font-version $(FONT_VERSION) --web-font

build-otf:
	uv run python -m generate_font --font-version $(FONT_VERSION) --otf

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
