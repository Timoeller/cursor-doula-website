# AGENTS.md

## Cursor Cloud specific instructions

This repository is a single, intentionally framework-free **static one-page website** for
Edda Möller (a Doula in Erkelenz / Kreis Heinsberg, Germany). It is plain HTML/CSS/vanilla
JavaScript with **no build step, no package manager, no backend, no database, and no tests
or linters configured**. See `README.md` for the full structure and design notes.

### Running the site (dev)
Serve the repository root as static files and open the page in a browser:

```bash
python3 -m http.server 8080   # then open http://localhost:8080/
```

There is no watch/build step — edit any file and refresh the browser. Opening `index.html`
via `file://` mostly works, but use the HTTP server so the web manifest, relative asset
paths, and responsive images behave like production.

### Lint / test / build
- **Lint:** none configured (no ESLint/Prettier/Stylelint, no `package.json`).
- **Test:** none exist (no test framework or test files).
- **Build:** none — files are deployed as-is to any static host.

Do not invent lint/test/build tooling unless explicitly requested.

### Optional: regenerating images
`site-assets/process_images.py` regenerates the optimized responsive images in
`assets/img/` from the originals in `site-assets/originals/`. It requires Pillow
(installed by the update script). Regeneration is deterministic (re-running produces
byte-identical files), so it normally leaves the working tree clean:

```bash
python3 site-assets/process_images.py
```

This is a one-off dev tool only; it is not part of running or deploying the site.
