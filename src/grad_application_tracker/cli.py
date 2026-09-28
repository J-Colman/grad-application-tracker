from datetime import date

import click

from .models import Opportunity
from .storage import load_opportunities, save_opportunities


@click.group()
def cli():
    """Track graduate job opportunities."""


@cli.command("list")
def list_opportunities():
    """Show all saved opportunities."""
    file_path = "data/opportunities.json"

    try:
        opportunities = load_opportunities(file_path)
    except FileNotFoundError:
        click.echo("No opportunities saved yet.")
        return
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
def add_opportunity(company, role, deadline, status):
    """Save a new opportunity."""
    file_path = "data/opportunities.json"

    try:
        parsed_deadline = date.fromisoformat(deadline) if deadline else None
    except ValueError as error:
        raise click.BadParameter(
            "Use YYYY-MM-DD format.", param_hint="--deadline"
        ) from error

    try:
        opportunities = load_opportunities(file_path)
    except FileNotFoundError:
        opportunities = []
    except (TypeError, ValueError) as error:
        raise click.ClickException(str(error)) from error

    opportunities.append(Opportunity(company, role, parsed_deadline, status))

    try:
        save_opportunities(opportunities, file_path)
    except OSError as error:
        raise click.ClickException(f"Could not save opportunities: {error}") from error

    click.echo(f"Added '{role}' at '{company}'. Status: {status}")
