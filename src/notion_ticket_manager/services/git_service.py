import subprocess
import sys
import urllib.parse

import inquirer

from ..config.environment import EnvironmentConfig


def run_git_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution de la commande: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Git n'est pas installé ou n'est pas dans le PATH.")
        sys.exit(1)


def create_branch(ticket_identifier):
    questions = [
        inquirer.Text(
            "branch_name",
            message="Nom de la branche",
            default=f"feat/{ticket_identifier}-",
        ),
    ]
    answers = inquirer.prompt(questions)

    if not answers:
        print("Operation annulée.")
        sys.exit(1)

    branch_name = answers["branch_name"]

    run_git_command(["git", "checkout", "-b", branch_name])
    print(f"✅ Branche '{branch_name}' créée et activée avec succès.")


def get_ticket_identifier_from_branch():

    branch_name = run_git_command(["git", "branch", "--show-current"])
    try:
        ticket_identifier = branch_name.split("-")[0].split("/")[1]
        return ticket_identifier, branch_name
    except IndexError:
        error_msg = (
            "❌ Branche invalide, veuillez créer une branche avec le format "
            "'feat/<ticket-identifier>-'"
        )
        print(error_msg)
        sys.exit(1)


def get_merge_request_url(branch_name, title=None, assignee_id=48):
    template = EnvironmentConfig().get_mr_template()
    base_url = (
        f"https://git.protilab.com/protilab/client-portal/-/merge_requests/new"
        f"?merge_request[source_branch]={branch_name}"
    )

    if title:
        encoded_title = urllib.parse.quote(title)
        base_url += f"&merge_request[title]={encoded_title}"

    if template:
        encoded_template = urllib.parse.quote(template)
        base_url += f"&merge_request[description]={encoded_template}"

    if assignee_id:
        base_url += f"&merge_request[assignee_id]={assignee_id}"

    return base_url
