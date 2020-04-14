# -*- coding: utf-8 -*-
"""Click commands."""
import os
from glob import glob
from subprocess import call

import click
from flask import cli

from stealthx.extensions import db
from stealthx.models import Role, User, SubscriptionPlan, SubscriptionType, Core, RankingSystem
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")


@click.command()
def test():
    """Run the tests."""
    import pytest

    rv = pytest.main([TEST_PATH, "--verbose"])
    exit(rv)


@click.command()
@click.option(
    "-f",
    "--fix-imports",
    default=True,
    is_flag=True,
    help="Fix imports using isort, before linting",
)
@click.option(
    "-c",
    "--check",
    default=False,
    is_flag=True,
    help="Don't make any changes to files, just confirm they are formatted correctly",
)
def lint(fix_imports, check):
    """Lint and check code style with black, flake8 and isort."""
    skip = ["node_modules", "requirements", "migrations"]
    root_files = glob("*.py")
    root_directories = [
        name for name in next(os.walk("."))[1] if not name.startswith(".")
    ]
    files_and_directories = [
        arg for arg in root_files + root_directories if arg not in skip
    ]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo("{}: {}".format(description, " ".join(command_line)))
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    isort_args = ["-rc"]
    black_args = []
    if check:
        isort_args.append("-c")
        black_args.append("--check")
    if fix_imports:
        execute_tool("Fixing import order", "isort", *isort_args)
    execute_tool("Formatting style", "black", *black_args)
    execute_tool("Checking code style", "flake8")


def init_ranking_system():
    rankings = [
        {"id": 1,
         "rank": "Spool III",
         "min_hp": 0
         },
        {"id": 2,
         "rank": "Spool II",
         "min_hp": 400
         },
        {"id": 3,
         "rank": "Spool I",
         "min_hp": 900
         }
    ]

    for rank in rankings:
        rank_obj = RankingSystem(id=rank['id'],rank=rank['rank'], min_hp=rank['min_hp'])
        db.session.add(rank_obj)

    db.session.commit()


def init_subscription_types():
    subs = [{
        "name": "free",
        "price": 0
        },
        {
            "name": "guardian",
            "price": 550
        },
        {
            "name": "mania",
            "price": 975
        }
    ]

    for sub in subs:
        obj = SubscriptionType(name=sub['name'], price=sub['price'])
        db.session.add(obj)

    db.session.commit()


@click.command()
@cli.with_appcontext
def init():
    init_ranking_system()
    init_subscription_types()

    click.echo("create user")

    role = Role(name="client")
    db.session.add(role)

    admin_role = Role(name="admin")
    db.session.add(admin_role)

    # Rank ID 1 = Spool III
    core = Core(current_rank_id=1, highest_rank_id=1)
    db.session.add(core)

    user = User(username="admin", email="admin@mail.com", password="admin", role=role, core=core)
    user.set_email_confirmed()

    user_subscription = SubscriptionPlan(user=user, subscription_type_id=1)

    db.session.add(user_subscription)
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")
