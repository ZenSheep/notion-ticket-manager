import argparse
import webbrowser

import inquirer

from .config.environment import EnvironmentConfig
from .services.git_service import (
    create_branch,
    get_merge_request_url,
    get_ticket_identifier_from_branch,
)
from .services.ticket_service import (
    get_available_tickets,
    get_ticket_from_identifier,
    get_ticket_name,
    select_ticket,
    set_ticket_state,
)


def new_ticket():
    tickets = get_available_tickets()
    tickets_list = tickets["results"]
    ticket_id, ticket_identifier = select_ticket(tickets_list)
    create_branch(ticket_identifier)
    set_ticket_state(ticket_id, "En cours")


def create_mr():
    ticket_identifier, branch_name = get_ticket_identifier_from_branch()
    ticket = get_ticket_from_identifier(ticket_identifier)
    set_ticket_state(ticket["id"], "Code review")
    ticket_name = get_ticket_name(ticket)
    merge_request_url = get_merge_request_url(branch_name, ticket_name)
    questions = [
        inquirer.Confirm(
            "open",
            message="Voulez-vous ouvrir la merge request dans votre navigateur ?",
            default=True,
        )
    ]
    answers = inquirer.prompt(questions)
    if answers["open"]:
        webbrowser.open(merge_request_url)


def main():
    # Validate configuration
    if not EnvironmentConfig().validate_config():
        raise ValueError("Missing required environment variables")

    parser = argparse.ArgumentParser(description="Notion API - Gestion des tickets")
    parser.add_argument("--new", action="store_true", help="Créer une nouvelle tâche")
    parser.add_argument("--mr", action="store_true", help="Créer une merge request")
    args = parser.parse_args()

    if args.new:
        new_ticket()
    elif args.mr:
        create_mr()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
