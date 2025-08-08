# Notion API - Ticket Management Tool

A Python-based command-line tool for managing tickets in Notion databases and integrating with Git workflows. This tool allows you to retrieve tickets from Notion, create Git branches, and manage ticket states seamlessly.

## Features

- 🔍 **Ticket Retrieval**: Fetch available tickets from Notion database based on user assignment and ticket states
- 🌿 **Git Integration**: Automatically create feature branches for tickets
- 📊 **State Management**: Update ticket states (Daily, En cours, Code review, etc.)
- 🔗 **Merge Request Creation**: Generate GitLab merge request URLs with pre-filled templates
- 🎯 **Interactive CLI**: User-friendly command-line interface with prompts

## Prerequisites

- Python 3.7+
- Git installed and configured
- Notion API access
- GitLab account (for merge request functionality)

## Installation

### Option 1: Install from Source

1. Clone the repository:

```bash
git clone <repository-url>
cd notion-ticket-manager
```

2. Install the package in development mode:

```bash
pip install -e .
```

3. Set up environment variables:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

### Option 2: Install via pip (when published)

```bash
pip install notion-ticket-manager
```

```env
# Notion API Configuration
NOTION_BASE_URL=https://api.notion.com
DATABASE_ID=your_database_id_here
NOTION_USER_ID=your_user_id_here
NOTION_TOKEN=your_integration_token_here
MR_TEMPLATE=your_merge_request_template_here
GITLAB_ASSIGNEE_ID=your_gitlab_assignee_id_here
```

## Configuration

### Notion Setup

1. Create a Notion integration at https://www.notion.so/my-integrations
2. Get your integration token
3. Share your Notion database with the integration
4. Get your database ID from the database URL
5. Get your user ID from your Notion profile

### Environment Variables

| Variable             | Description                   | Required |
| -------------------- | ----------------------------- | -------- |
| `NOTION_BASE_URL`    | Notion API base URL           | Yes      |
| `DATABASE_ID`        | Your Notion database ID       | Yes      |
| `NOTION_USER_ID`     | Your Notion user ID           | Yes      |
| `NOTION_TOKEN`       | Your Notion integration token | Yes      |
| `MR_TEMPLATE`        | Merge request template        | No       |
| `GITLAB_ASSIGNEE_ID` | GitLab assignee ID            | No       |

## Usage

### Start a New Ticket

Create a new feature branch and update ticket state:

```bash
zn --new
```

This will:

1. Show available tickets assigned to you
2. Let you select a ticket
3. Create a Git branch with the ticket identifier
4. Update the ticket state to "En cours"

### Create a Merge Request

Generate a merge request URL for the current branch:

```bash
zn --mr
```

This will:

1. Extract ticket identifier from the current branch name
2. Update the ticket state to "Code review"
3. Generate a GitLab merge request URL with pre-filled information
4. Optionally open the URL in your browser

### Alternative Commands

You can also use the full command name:

```bash
notion-ticket-manager --new
notion-ticket-manager --mr
```

### Global Availability

Once installed, the `zn` command is available globally from any directory:

```bash
# From any folder on your system
zn --new
zn --mr
```

### Branch Naming Convention

The tool expects branches to follow this format:

```
feat/<ticket-identifier>-<description>
```

Example: `feat/123-add-user-authentication`

## Project Structure

```
notion-ticket-manager/
├── src/
│   └── notion_ticket_manager/
│       ├── __init__.py
│       ├── cli.py                 # Main CLI application
│       ├── config/
│       │   ├── __init__.py
│       │   └── environment.py     # Environment configuration management
│       ├── api/
│       │   ├── __init__.py
│       │   └── notion_client.py   # Notion API request handlers
│       ├── services/
│       │   ├── __init__.py
│       │   ├── ticket_service.py  # Ticket management functions
│       │   └── git_service.py     # Git operations and branch management
│       └── utils/
│           ├── __init__.py
│           └── helpers.py          # Utility functions
├── main.py             # Entry point for CLI
├── requirements.txt    # Python dependencies
├── requirements-dev.txt # Development dependencies
├── pyproject.toml     # Modern Python packaging
├── Makefile           # Development commands
├── .env.example       # Environment variables template
└── README.md          # This file
```

## API Endpoints

The tool interacts with the following Notion API endpoints:

- `POST /v1/databases/{database_id}/query` - Query tickets with filters
- `PATCH /v1/pages/{page_id}` - Update ticket properties

## Ticket States

The tool manages the following ticket states:

- **Daily**: Tickets ready for daily work
- **Strat tech OK**: Tickets approved for technical strategy
- **Priorisé**: Prioritized tickets
- **En cours**: Tickets currently in progress
- **Code review**: Tickets ready for code review

## Error Handling

The tool includes comprehensive error handling for:

- Missing environment variables
- Invalid Git operations
- Notion API errors
- Invalid branch naming conventions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Add your license information here]

## Development

### Setup Development Environment

```bash
# Install the package in development mode
make setup

# Or manually:
pip install -e .
pip install -r requirements-dev.txt
```

### Development Commands

```bash
# Format code
make format

# Run linting
make lint

# Run tests
make test

# Clean build artifacts
make clean

# Run CLI commands
zn --new
zn --mr
```

### Code Quality

The project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

## Support

For issues and questions, please create an issue in the repository.
