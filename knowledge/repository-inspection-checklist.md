# Repository Inspection Checklist

## Ignore or de-emphasize
- `node_modules/`
- `target/`, `build/`, `dist/`, `.next/`, `.nuxt/`
- `.git/`
- binary artifacts
- generated files when clearly generated
- lock files except for ecosystem identification

## Identify project type
Look for `package.json`, `vite.config.*`, `webpack.config.*`, `angular.json`, `next.config.*`, `pom.xml`, `build.gradle`, `settings.gradle`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `requirements.txt`, `Dockerfile`, `docker-compose.yml`, Kubernetes manifests, Helm charts, database migrations, CI files.

## Entry point clues
Frontend: `src/main.*`, `src/App.*`, routing files, pages/app directories.
Backend: main application classes, controllers/resources/routes, service/application layer, repositories/DAOs, entities/models.
Infrastructure: Docker Compose services, environment variables, ports, volumes, networks, reverse proxies.

## Cross-repository analysis
For multiple repositories, identify system boundaries, shared APIs/contracts, deployment relationships, naming conventions, duplicated concepts, integration points, and ownership boundaries.
