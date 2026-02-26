"""CLI entrypoint for dotruler."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(
    name="dotruler",
    help="One config. Every AI coding tool. Always in sync.",
    no_args_is_help=True,
)
console = Console()


def _load_or_exit(config_path: Path | None = None):
    """Load config or exit with a helpful message."""
    from dotruler.config import find_config, load_config

    path = config_path or find_config()
    if not path:
        console.print(
            "[red]No .dotruler.toml found.[/red] Run [bold]dotruler init[/bold] to create one."
        )
        raise typer.Exit(1)

    config = load_config(path)
    return config, path


@app.command()
def init(
    directory: Path = typer.Argument(Path("."), help="Project directory to scan"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing config"),
):
    """Scan your project and generate a starter .dotruler.toml."""
    from dotruler.config import CONFIG_FILENAME
    from dotruler.scanner import scan_project

    project_dir = directory.resolve()
    config_path = project_dir / CONFIG_FILENAME

    if config_path.exists() and not force:
        console.print(
            f"[yellow]{CONFIG_FILENAME} already exists.[/yellow] Use --force to overwrite."
        )
        raise typer.Exit(1)

    console.print(f"[bold]Scanning[/bold] {project_dir}...\n")
    scan = scan_project(project_dir)

    # Show what was detected
    if scan["languages"]:
        console.print(f"  Languages:  {', '.join(scan['languages'])}")
    if scan["frameworks"]:
        console.print(f"  Frameworks: {', '.join(scan['frameworks'])}")
    if scan["commands"]:
        console.print(f"  Commands:   {', '.join(scan['commands'].keys())}")
    if scan["existing_ai_configs"]:
        console.print(
            f"  AI configs: {', '.join(scan['existing_ai_configs'].keys())} (found existing)"
        )
    console.print()

    # Generate TOML
    name = project_dir.name
    toml_lines = [
        f'[project]',
        f'name = "{name}"',
        f'description = ""',
    ]

    if scan["languages"]:
        langs = ", ".join(f'"{l}"' for l in scan["languages"])
        toml_lines.append(f"languages = [{langs}]")
    else:
        toml_lines.append('languages = []')

    if scan["frameworks"]:
        fws = ", ".join(f'"{f}"' for f in scan["frameworks"])
        toml_lines.append(f"frameworks = [{fws}]")
    else:
        toml_lines.append('frameworks = []')

    toml_lines.append("")
    toml_lines.append("[style]")
    toml_lines.append("rules = [")
    toml_lines.append('  # "Use functional components with hooks",')
    toml_lines.append('  # "Prefer const over let",')
    toml_lines.append("]")

    toml_lines.append("")
    toml_lines.append("[commands]")
    for cmd_name, cmd_value in scan.get("commands", {}).items():
        toml_lines.append(f'{cmd_name} = "{cmd_value}"')
    if not scan.get("commands"):
        toml_lines.append('# build = "npm run build"')
        toml_lines.append('# test = "npm test"')
        toml_lines.append('# lint = "npm run lint"')
        toml_lines.append('# dev = "npm run dev"')

    toml_lines.append("")
    toml_lines.append("[architecture]")
    toml_lines.append("notes = [")
    toml_lines.append('  # "API routes in src/app/api/",')
    toml_lines.append('  # "Database models in src/models/",')
    toml_lines.append("]")

    toml_lines.append("")
    toml_lines.append("[targets]")
    toml_lines.append('enabled = ["claude-md", "cursorrules", "copilot"]')

    content = "\n".join(toml_lines) + "\n"
    config_path.write_text(content, encoding="utf-8")

    console.print(
        Panel(
            f"Created [bold green]{CONFIG_FILENAME}[/bold green]\n\n"
            "Next steps:\n"
            f"  1. Edit {CONFIG_FILENAME} — add your coding rules\n"
            "  2. Run [bold]dotruler generate[/bold] to sync configs",
            title="[bold]dotruler init[/bold]",
            border_style="green",
        )
    )


@app.command()
def generate(
    config_path: Path = typer.Option(None, "--config", "-c", help="Path to .dotruler.toml"),
    directory: Path = typer.Argument(Path("."), help="Project directory to write configs to"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Preview without writing"),
):
    """Generate config files for all enabled AI tools."""
    # Import outputs to trigger registration
    import dotruler.outputs  # noqa: F401
    from dotruler.registry import get_renderer

    config, found_path = _load_or_exit(config_path)
    project_dir = directory.resolve()

    console.print(
        f"[bold]Generating[/bold] from {found_path.name}...\n"
    )

    for target_id in config.targets.enabled:
        try:
            renderer_cls = get_renderer(target_id)
        except KeyError as e:
            console.print(f"  [red]✗[/red] {e}")
            continue

        renderer = renderer_cls()
        override = config.targets.overrides.get(target_id)
        output_path = renderer.get_output_path(override)

        if dry_run:
            console.print(f"  [dim]would write[/dim] {output_path}")
        else:
            written = renderer.write(config, project_dir)
            console.print(f"  [green]✓[/green] {written.relative_to(project_dir)}")

    console.print()
    if dry_run:
        console.print("[dim]Dry run — no files written.[/dim]")
    else:
        console.print(f"[bold green]Done.[/bold green] {len(config.targets.enabled)} configs generated.")


@app.command()
def validate(
    config_path: Path = typer.Option(None, "--config", "-c", help="Path to .dotruler.toml"),
):
    """Validate your .dotruler.toml config."""
    import dotruler.outputs  # noqa: F401
    from dotruler.config import validate_config

    config, found_path = _load_or_exit(config_path)
    issues = validate_config(config)

    if not issues:
        console.print(f"[bold green]✓[/bold green] {found_path.name} is valid.")
        return

    for issue in issues:
        if issue.startswith("[error]"):
            console.print(f"  [red]✗[/red] {issue.replace('[error] ', '')}")
        elif issue.startswith("[warn]"):
            console.print(f"  [yellow]![/yellow] {issue.replace('[warn] ', '')}")

    errors = sum(1 for i in issues if i.startswith("[error]"))
    if errors:
        raise typer.Exit(1)


@app.command(name="list")
def list_targets():
    """Show all available output targets."""
    import dotruler.outputs  # noqa: F401
    from dotruler.registry import list_targets as _list_targets

    targets = _list_targets()

    table = Table(title="Available Targets", show_header=True)
    table.add_column("ID", style="bold cyan")
    table.add_column("Output File")
    table.add_column("Description")
    table.add_column("Limit", justify="right")

    for target_id, renderer_cls in sorted(targets.items()):
        r = renderer_cls()
        limit = f"{r.max_chars:,}" if r.max_chars else "—"
        table.add_row(target_id, r.default_output_path, r.description, limit)

    console.print(table)


@app.command()
def diff(
    config_path: Path = typer.Option(None, "--config", "-c", help="Path to .dotruler.toml"),
    directory: Path = typer.Argument(Path("."), help="Project directory"),
):
    """Preview what would change before writing."""
    import difflib

    import dotruler.outputs  # noqa: F401
    from dotruler.registry import get_renderer

    config, found_path = _load_or_exit(config_path)
    project_dir = directory.resolve()
    has_changes = False

    for target_id in config.targets.enabled:
        try:
            renderer_cls = get_renderer(target_id)
        except KeyError:
            continue

        renderer = renderer_cls()
        override = config.targets.overrides.get(target_id)
        output_path = project_dir / renderer.get_output_path(override)
        new_content = renderer.render(config)

        if output_path.exists():
            old_content = output_path.read_text(encoding="utf-8")
            if old_content == new_content:
                console.print(f"  [dim]unchanged[/dim] {output_path.relative_to(project_dir)}")
                continue

            diff_lines = difflib.unified_diff(
                old_content.splitlines(keepends=True),
                new_content.splitlines(keepends=True),
                fromfile=str(output_path.relative_to(project_dir)),
                tofile=str(output_path.relative_to(project_dir)),
            )
            console.print(f"\n  [yellow]modified[/yellow] {output_path.relative_to(project_dir)}")
            for line in diff_lines:
                line = line.rstrip("\n")
                if line.startswith("+") and not line.startswith("+++"):
                    console.print(f"    [green]{line}[/green]")
                elif line.startswith("-") and not line.startswith("---"):
                    console.print(f"    [red]{line}[/red]")
                else:
                    console.print(f"    {line}")
        else:
            console.print(f"\n  [green]new[/green] {output_path.relative_to(project_dir)}")

        has_changes = True

    if not has_changes:
        console.print("\n[dim]Everything is in sync.[/dim]")
    else:
        console.print(
            "\n[dim]Run[/dim] [bold]dotruler generate[/bold] [dim]to apply changes.[/dim]"
        )


@app.command()
def version():
    """Show the current version."""
    from dotruler import __version__

    console.print(f"dotruler [bold]{__version__}[/bold]")


if __name__ == "__main__":
    app()
