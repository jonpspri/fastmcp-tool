# Contributing to fastmcp-tool

Thank you for your interest in contributing to fastmcp-tool!

## Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/jonpspri/fastmcp-tool.git
   cd fastmcp-tool
   ```

2. Install uv if you haven't already:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Install dependencies:

   ```bash
   uv sync
   ```

4. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

## Code Quality

This project uses:

- **ruff** for linting and formatting
- **mypy** for type checking

Run checks before submitting:

```bash
# Lint and format
uv run ruff check .
uv run ruff format .

# Type check
uv run mypy src/
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Run the code quality checks
5. Commit your changes (`git commit -m 'Add my feature'`)
6. Push to your fork (`git push origin feature/my-feature`)
7. Open a Pull Request

## Reporting Issues

- Use GitHub Issues for bug reports and feature requests
- Include steps to reproduce for bugs
- Describe expected vs actual behavior

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
