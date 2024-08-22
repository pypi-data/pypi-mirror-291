import click

from aiopcli import utils

@click.group('schedule')
def cli():
    pass


@cli.command
@click.argument('env')
# FIXME: restrict type options
@click.option('-t', '--type', 'schedule_type', type=str)
# FIXME: timestamp regex
@click.option('-s', '--start', 'start_time', type=str)
@click.option('-e', '--end', 'end_time', type=str)
@click.option('-a', '--autoscale', 'auto_scaling_enabled', type=bool)
@click.option('-r', '--max-replicas', 'auto_scaling_max_replicas', type=int)
@click.option('-c', '--capacity', 'desired_capacity', type=int)
@click.option('-w', '--weekday', 'day_of_week',
              type=click.Choice(['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']))
@click.option('--mm', type=int)
@click.option('--dd', type=int)

@click.option('--hh', type=int)
@click.option('--mi', type=int)
@click.pass_obj
def create(ctx, env, **request):
    env_ = ctx.get_env(env)
    if not env_:
        raise ValueError(f"No such env: '{env}'")
    request = {key: value for key, value in request.items() if value is not None}
    response = ctx.client.post(f'/api/v1/env/{env_.id}/create_scaling_schedule', json=request)
    utils.handle_response(response)


@cli.command
@click.argument('env')
@click.argument('schedule_id', type=int)
@click.pass_obj
def delete(ctx, env, schedule_id):
    env_ = ctx.get_env(env)
    if not env_:
        raise ValueError(f"No such env: '{env}'")
    response = ctx.client.post(
        f'/api/v1/env/{env_.id}/delete_scaling_schedule', json={'schedule_id': schedule_id})
    utils.handle_response(response)


@cli.command
@click.argument('env')
@click.argument('schedule_id', type=int)
# FIXME: restrict type options
@click.option('-t', '--type', 'schedule_type', type=str)
# FIXME: timestamp regex
@click.option('-s', '--start', 'start_time', type=str)
@click.option('-e', '--end', 'end_time', type=str)
@click.option('-a', '--autoscale', 'auto_scaling_enabled', type=bool)
@click.option('-r', '--max-replicas', 'auto_scaling_max_replicas', type=int)
@click.option('-c', '--capacity', 'desired_capacity', type=int)
@click.option('-w', '--weekday', 'day_of_week',
              type=click.Choice(['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']))
@click.option('--mm', type=int)
@click.option('--dd', type=int)

@click.option('--hh', type=int)
@click.option('--mi', type=int)
@click.pass_obj
def update(ctx, env, **request):
    env_ = ctx.get_env(env)
    if not env_:
        raise ValueError(f"No such env: '{env}'")
    request = {key: value for key, value in request.items() if value is not None}
    response = ctx.client.post(f'/api/v1/env/{env_.id}/update_scaling_schedule', json=request)
    utils.handle_response(response)
