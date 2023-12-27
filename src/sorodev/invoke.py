from . import utils


def invoke(function_name, function_args={}, network=None, account=None):
    if type(function_args) == dict:
        function_args = ' '.join(
            [f'--{key} {val}' for key, val in function_args.items()])

    cfg = utils.load_config()
    name = cfg['name']

    if network == None:
        network = cfg['default_network']

    if account == None:
        account = cfg['default_account']

    utils.log_action(
        f'Invoking latest "{name}" contract on {network} from {account} with "{function_name} {function_args}"')

    contract_address, error = utils.call(f'cat .soroban/{name}')
    if error:
        utils.exit_error(f'No deployment found')

    print(f'Contract address: {contract_address}')

    cmd = f'''\
        soroban contract invoke \
            --id {contract_address} \
            --source {account} \
            --network {network} \
            -- \
                {function_name} \
                {function_args}
    '''

    output, error = utils.call(cmd)

    if error:
        utils.exit_error(error)

    print(output)
