## Repo rules (please read before adding new features)

- keep pyproject.toml dependencies to the minimum
- add large modules as dependencies directly in the function scope (don't add them as global or importing hestcore will be slow)
- each class in this repo should be as generic as possible to be used across projects, avoid duplicate classes/dataloader/datasets and maximize code cohesion.
