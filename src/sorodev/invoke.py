from . import utils


def invoke_with_str(function_name, function_args_str='', network=None):
    cfg = utils.load_config()
    name = cfg['name']

    if network == None:
        network = cfg['default_network']

    print(
        f'Invoking latest "{name}" contract on {network} with "{function_name} {function_args_str}"')

    cmd = '''\
        soroban contract invoke \
            --id $(cat .soroban/{name}) \
            --source alice \
            --network {network} \
            -- \
                {function_name} \
                {function_args_str}
    '''

    args = {
        "name": name,
        "network": network,
        "function_name": function_name,
        "function_args_str": function_args_str
    }
    output, error = utils.call(cmd.format(**args))

    if error:
        utils.exit_error(error)

    print(output)


def invoke_with_dict(function_name, function_args={}, network=None):
    function_args_str = ' '.join(
        [f'--{key} {val}' for key, val in function_args.items()])

    invoke_with_str(function_name, function_args_str)
