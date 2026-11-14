## Application rules

- Keep shared navigation, footer, and language context in the root layout so language selection survives navigation.
- Keep translated product copy and documented CLI commands in a browser-safe shared module so pages agree on supported behavior.
- Use separate leaf routes for documentation, commands, workflow, and safety, each with its own metadata, to support direct links and indexing.
- Define the kinetic-glass visual system and control variants in global CSS; use the shared Button component for interactive controls.
- Describe only Skald CLI behavior that exists in the Python package — do not invent features.
