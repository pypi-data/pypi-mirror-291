import click
import yaml
import os
import openai
from typing import Dict
from dotenv import load_dotenv, set_key

VERSION = "1.0.0"
CONFIG_FILE = os.path.expanduser('~/.ola_config.yaml')
ENV_FILE = os.path.expanduser('~/.ola_env')

def load_config() -> Dict[str, str]:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return yaml.safe_load(f) or {}
    return {}

def save_config(config: Dict[str, str]):
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)

def load_env():
    load_dotenv(ENV_FILE)
    openai.api_key = os.getenv('AI_API_KEY')
    openai.api_base = os.getenv('AI_API_BASE', 'https://api.openai.com/v1')
    return os.getenv('AI_MODEL', 'gpt-4o-mini')

@click.group()
@click.version_option(version=VERSION)
def cli():
    """OLA - AI Assistant CLI"""
    pass

@cli.command()
@click.argument('name')
@click.argument('prompt')
def create(name: str, prompt: str):
    """Create a new prompt and save it to the config file."""
    config = load_config()
    config[name] = prompt
    save_config(config)
    click.echo(f"Prompt '{name}' created successfully.")

@cli.command()
@click.argument('name')
@click.argument('user_input')
def run(name: str, user_input: str):
    """Run a saved prompt with user input."""
    config = load_config()
    if name not in config:
        click.echo(f"Prompt '{name}' not found.")
        return

    prompt = config[name]
    full_prompt = f"{prompt}\n\nUser: {user_input}"

    model = load_env()

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ]
        )
        click.echo(response.choices[0].message['content'])
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
def list():
    """List all saved prompts."""
    config = load_config()
    if not config:
        click.echo("No prompts saved.")
    else:
        click.echo("Saved prompts:")
        for name, prompt in config.items():
            click.echo(f"  {name}: {prompt}")

@cli.command()
@click.argument('name')
def delete(name: str):
    """Delete a saved prompt."""
    config = load_config()
    if name not in config:
        click.echo(f"Prompt '{name}' not found.")
    else:
        del config[name]
        save_config(config)
        click.echo(f"Prompt '{name}' deleted successfully.")

@cli.command()
@click.option('--key', help='OpenAI API Key')
@click.option('--model', help='OpenAI Model to use')
@click.option('--url', help='OpenAI API base URL')
def update_env(key, model, url):
    """Update environment variables."""
    if key:
        set_key(ENV_FILE, 'AI_API_KEY', key)
        click.echo("API Key updated.")
    if model:
        set_key(ENV_FILE, 'AI_MODEL', model)
        click.echo("Model updated.")
    if url:
        set_key(ENV_FILE, 'AI_API_BASE', url)
        click.echo("API base URL updated.")
    if not any([key, model, url]):
        click.echo("No updates provided. Use --key, --model, or --url to update values.")

@cli.command()
def list_env():
    """List current environment variables."""
    load_dotenv(ENV_FILE)
    click.echo("Current environment settings:")
    click.echo(f"API Key: {'*' * 8}{os.getenv('AI_API_KEY')[-4:] if os.getenv('AI_API_KEY') else 'Not set'}")
    click.echo(f"Model: {os.getenv('AI_MODEL', 'Not set')}")
    click.echo(f"API Base URL: {os.getenv('AI_API_BASE', 'Not set')}")

def main():
    cli()

if __name__ == '__main__':
    main()
