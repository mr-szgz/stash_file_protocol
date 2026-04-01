# Research Summary

- Research Date: `2026-04-01`
- Official Version: Semantic Versioning `2.0.0` (semver.org spec)
- Key Findings:
  - Version format is `MAJOR.MINOR.PATCH` with optional pre-release (`-`) and build metadata (`+`).
  - Increment `MAJOR` for incompatible API changes, `MINOR` for backwards-compatible additions, and `PATCH` for backwards-compatible bug fixes.
  - A pre-release (e.g., `-alpha.1`, `-rc.2`) indicates lower precedence than the associated normal version.
  - Build metadata (e.g., `+build.5`) must be ignored when determining version precedence.
  - Pre-release identifiers are dot-separated; numeric identifiers must not include leading zeroes.
  - Once a version is released, its contents must not change (immutability).
  - Public API definition is required to make versioning rules meaningful.
- Public-Sector Reference:
  - NIST IR 8060 landing page is captured as a public-sector reference touchpoint; it does not define SemVer but provides context in software identification discussions.
- Compatibility Notes:
  - SemVer is language- and ecosystem-agnostic; use `-rc.N` or other pre-release tags for release candidates.
