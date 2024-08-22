# -*- coding: utf-8 -*-

"""
==========================================================
Civitai CLI Manager - Helpers
==========================================================

This module contains helper functions for the Civitai Model Manager.

"""
import os
import typer

from typing import Any, Dict
from rich.console import Console
from rich.table import Table


console = Console(soft_wrap=True)

def feedback_message(message: str, type: str = "info") -> None:
    """_summary_

    Args:
        message (str): _description_
        type (str, optional): _description_. Defaults to "info".

    Returns:
        _type_: _description_
    """
    options = {
        "types": {
            "info": "green",
            "warning": "yellow",
            "error": "red",
            "exception": "red",
        },
        "titles": {
            "info": "Information",
            "warning": "Warning",
            "error": "Error Message",
            "exception": "Exception Message",
        }
    }

    feedback_message_table = Table(style=options["types"][type])
    feedback_message_table.add_column(options["titles"][type])
    feedback_message_table.add_row(message)
    
    if type == "exception":
        console.print_exception(feedback_message_table)
        raise typer.Exit()
    console.print(feedback_message_table)
    return None


def get_model_folder(models_dir: str, model_type: str, ref_types: dict) -> str:
    if model_type not in ref_types:
        console.print(f"Model type '{model_type}' is not mapped to any folder. Please select a folder to download the model.")
        selected_folder = typer.prompt("Enter the folder name to download the model:", default="unknown")
        return os.path.join(models_dir, selected_folder)
    return os.path.join(models_dir, ref_types[model_type])


def create_table(title: str, columns: list) -> Table:
    table = Table(title=title, title_justify="left")
    for col_name, style in columns:
        table.add_column(col_name, style=style)
    return table


def add_rows_to_table(table: Table, data: Dict[str, Any]) -> None:
    for key, value in data.items():
        if isinstance(value, list):
            value = ", ".join(map(str, value))
        table.add_row(key, str(value))
    