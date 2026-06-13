# Operations Research Final Presentation

This directory contains the Slidev web courseware for the operations research final project.

## Run Locally

```bash
npm install
npm run dev
```

Then open:

```text
http://localhost:3030/
```

## Build

```bash
npm run build
```

The production build is written to `dist/`.

## Export / Verify Pages

```bash
npm run export -- --format png --range 6,31 --output verify-pages
```

The export command is useful for checking whether specific pages render correctly.
Remove `verify-pages/` after visual inspection if the images are only temporary checks.

## Main Files

- `slides.md`: slide content and structure.
- `style.css`: global visual style for the deck.
- `public/figures/`: copied figures used by the deck.
