
from pathlib import Path

from . import utils


def deploy(network=None):
    cfg = utils.load_config()
    name = cfg['name']

    if network == None:
        network = cfg['default_network']

    print(f'Deploying "{name}" to "{network}"')
    cmd = f'''\
        soroban contract deploy \
        --wasm target/wasm32-unknown-unknown/release/{name}.wasm \
        --source alice \
        --network {network}
    '''
    output, error = utils.call(cmd)

    if error:
        utils.exit_error(error)

    contract_address = output.split('\n')[0]

    if contract_address[0] != 'C':
        utils.exit_error(f'Could not extract contract address from: {output}')

    print(f'Contract address: {contract_address}')
    Path(f'.soroban/{name}').write_text(contract_address)
