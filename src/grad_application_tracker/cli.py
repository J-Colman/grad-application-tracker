from datetime import date

import click

from . import services
from .models import Opportunity

DATA_PATH: str = "data/opportunities.json"


@click.group()
def cli() -> None:
    """Track graduate job opportunities."""


@cli.command("list")
def list_opportunities() -> None:
    """Show all saved opportunities."""
    try:
        opportunities = services.get_opportunities(DATA_PATH)
    except (TypeError, ValueError) as error:
        raise click.ClickException(str(error)) from error

    if not opportunities:
        click.echo("No opportunities saved yet.")
        return

    for opportunity in opportunities:
        click.echo(opportunity)


@cli.command("add")
@click.option("--company", required=True, help="Company name.")
@click.option("--role", required=True, help="Job title.")
@click.option("--deadline", help="Deadline in YYYY-MM-DD format.")
@click.option(
    "--status",
    type=click.Choice(Opportunity.VALID_STATUSES, case_sensitive=False),
    default="saved",
    show_default=True,
)
def add_opportunity(company: str, role: str, deadline: str | None, status: str) -> None:
    """Save a new opportunity."""
    try:
        parsed_deadline = date.fromisoformat(deadline) if deadline else None
    except ValueError as error:
        raise click.BadParameter(
            "Use YYYY-MM-DD format.", param_hint="--deadline"
        ) from error

    try:
        services.add_opportunity(DATA_PATH, company, role, parsed_deadline, status)
    except (TypeError, ValueError) as error:
        raise click.ClickException(str(error)) from error
    except OSError as error:
        raise click.ClickException(f"Could not save opportunities: {error}") from error

    click.echo(f"Added '{role}' at '{company}'. Status: '{status}'")
