import os
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables from multiple locations
# Priority: 1. Current directory .env, 2. Current directory .znrc, 3. Home directory .znrc, 4. System env vars
def load_environment():
    current_dir_config = Path.cwd()
    # Load from current directory .env file
    current_env_config = current_dir_config / ".env"
    if current_env_config.exists():
        load_dotenv(current_env_config)

    # Load from current directory .znrc file
    current_znrc_config = current_dir_config / ".znrc"
    if current_znrc_config.exists():
        load_dotenv(current_znrc_config)

    # Load from home directory configuration file
    home_config = Path.home() / ".znrc"
    if home_config.exists():
        load_dotenv(home_config)


# Load environment variables
load_environment()


class EnvironmentConfig:
    def __init__(self):
        self.notion_base_url = os.getenv("NOTION_BASE_URL")
        self.database_id = os.getenv("DATABASE_ID")
        self.notion_user_id = os.getenv("NOTION_USER_ID")
        self.notion_token = os.getenv("NOTION_TOKEN")
        self.mr_template = os.getenv("MR_TEMPLATE")
        self.gitlab_assignee_id = os.getenv("GITLAB_ASSIGNEE_ID")

        # Property names configuration
        self.state_property_name = os.getenv("STATE_PROPERTY_NAME", "État")

        # Ticket states configuration
        self.initial_states = self._parse_states("INITIAL_TICKET_STATES", [])
        self.available_states = self._parse_states("AVAILABLE_TICKET_STATES", [])
        self.in_progress_state = os.getenv("IN_PROGRESS_STATE")
        self.code_review_state = os.getenv("CODE_REVIEW_STATE")

        # Gitlab configuration
        self.gitlab_repository_url = os.getenv("GITLAB_REPOSITORY_URL")

    def get_notion_base_url(self):
        """Get the NOTION_BASE_URL environment variable"""
        return self.notion_base_url

    def get_database_id(self):
        """Get the DATABASE_ID environment variable"""
        return self.database_id

    def get_notion_user_id(self):
        """Get the NOTION_USER_ID environment variable"""
        return self.notion_user_id

    def get_notion_token(self):
        """Get the NOTION_TOKEN environment variable"""
        return self.notion_token

    def get_mr_template(self):
        """Get the MR_TEMPLATE environment variable"""
        return self.mr_template

    def get_gitlab_repository_url(self):
        """Get the GITLAB_REPOSITORY_URL environment variable"""
        return self.gitlab_repository_url

    def get_gitlab_assignee_id(self):
        """Get the GITLAB_ASSIGNEE_ID environment variable"""
        return self.gitlab_assignee_id

    def _parse_states(self, env_var_name, default_states):
        """Parse comma-separated states from environment variable"""
        states_str = os.getenv(env_var_name)
        if states_str:
            return [state.strip() for state in states_str.split(",")]
        return default_states

    def get_initial_states(self):
        """Get the initial ticket states to search for"""
        return self.initial_states

    def get_available_states(self):
        """Get all available ticket states"""
        return self.available_states

    def get_in_progress_state(self):
        """Get the state name for tickets in progress"""
        return self.in_progress_state

    def get_code_review_state(self):
        """Get the state name for tickets in code review"""
        return self.code_review_state

    def get_state_property_name(self):
        """Get the property name for ticket state"""
        return self.state_property_name

    def validate_config(self):
        """Validate that required environment variables are set"""
        missing_vars = []

        if self.notion_base_url is None:
            missing_vars.append("NOTION_BASE_URL")
        if self.database_id is None:
            missing_vars.append("DATABASE_ID")
        if self.notion_user_id is None:
            missing_vars.append("NOTION_USER_ID")
        if self.notion_token is None:
            missing_vars.append("NOTION_TOKEN")
        if not self.initial_states:
            missing_vars.append("INITIAL_TICKET_STATES")
        if not self.available_states:
            missing_vars.append("AVAILABLE_TICKET_STATES")
        if self.in_progress_state is None:
            missing_vars.append("IN_PROGRESS_STATE")
        if self.code_review_state is None:
            missing_vars.append("CODE_REVIEW_STATE")
        if self.state_property_name is None:
            missing_vars.append("STATE_PROPERTY_NAME")
        if self.gitlab_repository_url is None:
            missing_vars.append("GITLAB_REPOSITORY_URL")
        if missing_vars:
            print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")
            return False

        print("All required environment variables are set")
        return True

    def print_config(self):
        """Print the current configuration"""
        print(f"NOTION_BASE_URL: {self.notion_base_url}")
        print(f"DATABASE_ID: {self.database_id}")
        print(f"NOTION_USER_ID: {self.notion_user_id}")
        token_display = "*" * len(self.notion_token) if self.notion_token else "Not set"
        print(f"NOTION_TOKEN: {token_display}")
        print(f"MR_TEMPLATE: {self.mr_template}")
        print(f"GITLAB_ASSIGNEE_ID: {self.gitlab_assignee_id}")
        initial_states_display = (
            ", ".join(self.initial_states) if self.initial_states else "Not set"
        )
        print(f"INITIAL_TICKET_STATES: {initial_states_display}")

        available_states_display = (
            ", ".join(self.available_states) if self.available_states else "Not set"
        )
        print(f"AVAILABLE_TICKET_STATES: {available_states_display}")
        print(f"IN_PROGRESS_STATE: {self.in_progress_state or 'Not set'}")
        print(f"CODE_REVIEW_STATE: {self.code_review_state or 'Not set'}")
        print(f"STATE_PROPERTY_NAME: {self.state_property_name or 'Not set'}")
        print(f"GITLAB_REPOSITORY_URL: {self.gitlab_repository_url or 'Not set'}")

# Example usage
if __name__ == "__main__":
    config = EnvironmentConfig()
    config.print_config()
    config.validate_config()
