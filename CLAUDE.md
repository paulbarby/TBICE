# CLAUDE.md - Helper Reference

## Build & Test Commands
- Build: `npm run build` or `yarn build`
- Lint: `npm run lint` or `yarn lint`
- Test all: `npm test` or `yarn test`
- Test single file: `npm test -- path/to/test` or `jest path/to/test`
- Dev server: `npm run dev` or `yarn dev`

## Code Style Guidelines
- **Formatting**: Use Prettier with default settings
- **Naming**: camelCase for variables/functions, PascalCase for classes/components
- **Imports**: Group and order: 1) React/framework 2) External libs 3) Internal modules
- **Error Handling**: Use try/catch blocks for async operations; avoid silent failures
- **Types**: Use TypeScript types/interfaces over PropTypes; prefer explicit return types
- **Comments**: JSDoc for public APIs; inline comments only for complex logic
- **File Structure**: One component per file; group related files in directories