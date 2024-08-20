import click


import typing

if typing.TYPE_CHECKING:
    from ..client import Primitive


@click.command("lint")
@click.pass_context
def cli(context):
    """Lint"""
    primitive: Primitive = context.obj.get("PRIMITIVE")
    primitive.lint.run_lint()
