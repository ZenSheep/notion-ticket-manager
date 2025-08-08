import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class EnvironmentConfig:
    def __init__(self):
        self.notion_base_url = os.getenv("NOTION_BASE_URL")
        self.database_id = os.getenv("DATABASE_ID")
        self.notion_user_id = os.getenv("NOTION_USER_ID")
        self.notion_token = os.getenv("NOTION_TOKEN")
        self.mr_template = os.getenv("MR_TEMPLATE")
        self.gitlab_assignee_id = os.getenv("GITLAB_ASSIGNEE_ID")

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

    def get_gitlab_assignee_id(self):
        """Get the GITLAB_ASSIGNEE_ID environment variable"""
        return self.gitlab_assignee_id

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


# Example usage
if __name__ == "__main__":
    config = EnvironmentConfig()
    config.print_config()
    config.validate_config()
