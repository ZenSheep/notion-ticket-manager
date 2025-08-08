import sys

import inquirer

from ..api.notion_client import patch_page, post_database_query
from ..config.environment import EnvironmentConfig


def retrieve_tickets(states):
    config = EnvironmentConfig()

    payload = {
        "filter": {
            "and": [
                {
                    "property": "État du Cycle",
                    "rollup": {"any": {"status": {"equals": "Actuel"}}},
                },
                {
                    "property": "Personne assignée",
                    "people": {"contains": config.get_notion_user_id()},
                },
                {
                    "or": [
                        {"property": "État", "status": {"equals": state}}
                        for state in states
                    ]
                },
            ]
        }
    }

    response = post_database_query(config.get_database_id(), payload)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        sys.exit(1)


def get_available_tickets():
    states = ["Daily"]
    tickets = retrieve_tickets(states)
    if len(tickets) > 0:
        return tickets
    states.append("Strat tech OK")
    states.append("Priorisé")
    return retrieve_tickets(states)


def select_ticket(tickets):
    ticket_options = []
    for ticket in tickets:
        ticket_id = ticket["properties"]["Identifiant"]["unique_id"]["number"]
        ticket_name = get_ticket_name(ticket)
        ticket_options.append(f"{ticket_id} - {ticket_name}")
    ticket_options = [
        inquirer.List("ticket", message="Choisissez une tâche", choices=ticket_options)
    ]
    answers = inquirer.prompt(ticket_options)
    if not answers:
        print("Operation annulée.")
        sys.exit(1)
    ticket_identifier = answers["ticket"].split(" - ")[0]
    ticket = next(
        (
            ticket
            for ticket in tickets
            if ticket["properties"]["Identifiant"]["unique_id"]["number"]
            == int(ticket_identifier)
        ),
        None,
    )
    if not ticket:
        print("Tâche non trouvée.")
        sys.exit(1)

    return ticket["id"], ticket_identifier


def set_ticket_state(ticket_id, state):
    questions = [
        inquirer.Confirm(
            "state",
            message="Voulez-vous déplacer la tâche dans l état " + state + " ?",
            default=True,
        )
    ]
    answers = inquirer.prompt(questions)
    if not answers["state"]:
        return

    config = EnvironmentConfig()
    payload = {
        "properties": {"État": {"status": {"name": state}}},
        "parent": {"database_id": config.get_database_id()},
    }
    response = patch_page(ticket_id, payload)
    if response.status_code == 200:
        return True
    else:
        print(f"Error: {response.status_code} - {response.text}")
        sys.exit(1)


def get_ticket_from_identifier(identifier):
    config = EnvironmentConfig()
    payload = {
        "filter": {"property": "Identifiant", "unique_id": {"equals": int(identifier)}}
    }
    response = post_database_query(config.get_database_id(), payload)
    if response.status_code == 200:
        return response.json()["results"][0]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        sys.exit(1)


def get_ticket_name(ticket):
    return ticket["properties"]["Nom de la tâche"]["title"][0]["plain_text"]
