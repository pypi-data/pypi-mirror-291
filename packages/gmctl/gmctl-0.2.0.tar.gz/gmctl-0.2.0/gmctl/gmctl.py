from dotenv import load_dotenv
load_dotenv() 

import logging
logging.basicConfig(level=logging.ERROR, format='gmctl - %(name)s - %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import click
from gmctl.repository import Repository
from gmctl.commit import Commit
from gmctl.ecs_deployment import ECSDeployment
from gmctl.user import UserRole
from gmctl.gmclient import GitmoxiClient
from gmctl.utils import print_table
import os

@click.group()
@click.option('-e', '--endpoint-url', default="env(GITMOXI_ENDPOINT_URL), fallback to http://127.0.0.1:8080", help='The Gitmoxi FastAPI endpoint URL', show_default=True)
@click.option('-l', '--log-level', default="ERROR", type=click.Choice(["DEBUG","INFO","WARNING","ERROR","CRITICAL"], case_sensitive=False), help='The log level', show_default=True)
@click.pass_context
def cli(ctx, endpoint_url ,log_level):
    logging.getLogger().setLevel(getattr(logging, log_level.upper()))
    ctx.ensure_object(dict)
    endpoint_url = ctx.obj.get('ENDPOINT_URL', None)
    if not endpoint_url:
        endpoint_url = os.getenv('GITMOXI_ENDPOINT_URL', 'http://127.0.0.1:8080')
    ctx.obj['ENDPOINT_URL'] = endpoint_url

# Repo group with subcommands
@cli.group()
@click.pass_context 
def repo(ctx):
    """Repo related commands."""
    pass

@repo.command()
@click.option('-r', '--repo-url', required=True, help='The repository URL')
@click.option('-b', '--branch', required=True, help='The branches in the repository', multiple=True)
@click.option('-a', '--access-token-arn', required=True, help='The access token ARN')
@click.pass_context
def add(ctx, repo_url, branch, access_token_arn):
    repo = Repository(repo_url=repo_url, branches=list(branch), access_token_arn=access_token_arn)
    add_response = repo.add(GitmoxiClient(ctx.obj['ENDPOINT_URL']))
    logger.info(f"Add response: {add_response}")

@repo.command()
@click.option('-r', '--repo-url', help='The repository URL')
@click.pass_context
def get(ctx, repo_url):
    repos = Repository.get(GitmoxiClient(ctx.obj['ENDPOINT_URL']), repo_url)
    to_display = [repo.to_dict() for repo in repos]
    print_table(to_display)

@repo.command()
@click.option('-r', '--repo-url', help='The repository URL', required=True)
@click.pass_context
def delete(ctx, repo_url):
    delete_response = Repository.delete(GitmoxiClient(ctx.obj['ENDPOINT_URL']), repo_url)
    logger.info(f"Delete response: {delete_response}")
    print(f"Delete response: {delete_response}")

# Commit group with subcommands
@cli.group()
@click.pass_context  
def commit(ctx):
    """Commit related commands."""
    pass

@commit.command()
@click.option('-c', '--commit-hash', help='The commit hash')
@click.option('-r', '--repo-url', help='The repository URL')
@click.option('-f', '--file-only-flag', is_flag=True, help='Gitmoxi relevant files in the commit')
@click.pass_context
def get(ctx, commit_hash, repo_url, file_only_flag):
    commits = Commit.get(GitmoxiClient(ctx.obj['ENDPOINT_URL']), commit_hash, repo_url)
    to_display = []
    if file_only_flag:
        for commit in commits:
            to_display += commit.get_relevant_files()
    else:
        to_display = [commit.summary() for commit in commits]
    print_table(to_display)

@commit.command()
@click.option('-c', '--commit-hash', help='The commit hash to delete. Multiple is allowed', required=True, multiple=True)
@click.pass_context
def delete(ctx, commit_hash):
    for ch in commit_hash:
        delete_response = Commit.delete(GitmoxiClient(ctx.obj['ENDPOINT_URL']), ch)
        logger.info(f"Delete {ch} response: {delete_response}")
        print(f"Delete {ch} response: {delete_response}")

@commit.command()
@click.pass_context
def deploy(ctx):
    click.echo(f'Deploying commit to {ctx.obj["ENDPOINT_URL"]}')

# User group with subcommands
@cli.group()
@click.pass_context
def user(ctx):
    """User related commands."""
    pass

@user.command()
@click.pass_context
def add(ctx):
    click.echo(f'Adding user to {ctx.obj["ENDPOINT_URL"]}')

@user.command()
@click.pass_context
def get(ctx):
    click.echo(f'Getting users from {ctx.obj["ENDPOINT_URL"]}')

# Deployment group with subcommands
@cli.group()
@click.pass_context
def deployment(ctx):
    """User related commands."""
    pass

@deployment.group()
@click.pass_context
def ecs(ctx):
    pass

@ecs.command()
@click.option('-r', '--repo-url', help='The repository URL')
@click.option('-c', '--commit-hash', help='The commit hash')
@click.option('-cl', '--cluster', help='The ECS cluster')
@click.option('-s', '--service', help='The ECS service')
@click.option('-a', '--account-id', help='The AWS account ID')
@click.option('-v', '--verbose', is_flag=True, help='Verbose output')
@click.option('-A', '--show-all', is_flag=True, help='Verbose for all deployments')
@click.pass_context
def get(ctx, repo_url, commit_hash, cluster, service, account_id, verbose, show_all):
    deployments = ECSDeployment.get(GitmoxiClient(ctx.obj['ENDPOINT_URL']), repo_url, commit_hash, cluster, service, account_id)
    to_display = [deployment.summary() for deployment in deployments]
    print_table(to_display)
    if verbose:
        for deployment in deployments:
            if not show_all and deployment.status != "PROCESSED_ERROR":
                continue
            print("-------------------------------")
            print(f"\n{deployment.status}, {deployment.repo_url}, {deployment.file_prefix}, {deployment.service}, {deployment.cluster}: \n")
            for status in deployment.status_details:
                print(f"{status}\n")
            print("-------------------------------")
    