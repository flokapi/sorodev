
from pathlib import Path


from . import utils


def write_contract_cargo_toml(contract_path, name):
    lines = '''\
        [package]
        name = "{name}"
        version = "0.1.0"
        edition = "2021"

        [lib]
        crate-type = ["cdylib"]

        [dependencies]
        soroban-sdk = {{ workspace = true }}

        [dev_dependencies]
        soroban-sdk = {{ workspace = true, features = ["testutils"] }}

        [features]
        testutils = ["soroban-sdk/testutils"]
    '''

    target = contract_path.joinpath('Cargo.toml')
    args = {
        'name': name
    }

    utils.write_lines(target, lines, args)


def write_default_lib_rs(src_path, name):
    lines = '''\
        #![no_std]
        use soroban_sdk::{contract, contractimpl, symbol_short, vec, Env, Symbol, Vec};

        #[contract]
        pub struct Contract;

        #[contractimpl]
        impl Contract {
            pub fn hello(env: Env, to: Symbol) -> Vec<Symbol> {
                vec![&env, symbol_short!("Hello"), to]
            }
        }
        #[cfg(test)]
        mod test;
    '''

    target = src_path.joinpath('lib.rs')
    utils.write_lines(target, lines)


def write_default_test_rs(src_path, name):
    lines = '''\
        use crate::{Contract, ContractClient};
        use soroban_sdk::{symbol_short, vec, Env};

        #[test]
        fn hello() {
            let env = Env::default();
            let contract_id = env.register_contract(None, Contract);
            let client = ContractClient::new(&env, &contract_id);

            let words = client.hello(&symbol_short!("Dev"));
            assert_eq!(
                words,
                vec![&env, symbol_short!("Hello"), symbol_short!("Dev"),]
            );
        }
    '''

    target = src_path.joinpath('test.rs')
    utils.write_lines(target, lines)


# ------------------------------------------------


def add_contract(name, app_path=Path('.')):
    utils.log_action(f"Installing contract: {name}")

    contract_path = app_path.joinpath(f'./contracts/{name}')
    contract_path.mkdir(exist_ok=True, parents=True)

    src_path = contract_path.joinpath('src')
    src_path.mkdir(exist_ok=True)

    write_contract_cargo_toml(contract_path, name)
    write_default_test_rs(src_path, name)
    write_default_lib_rs(src_path, name)
