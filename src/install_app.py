from pathlib import Path


import utils
import constants


def write_soroban_dev_config(app_path, name, app_type):
    data = {
        'name': name,
        'type': app_type,
        'default_network': 'testnet'
    }

    target = app_path.joinpath(constants.SOROBAN_DEV_FILE_NAME)
    utils.write_json(target, data)


def write_gitignore(app_path):
    lines = '''\
        .soroban/
        target/
    '''

    target = app_path.joinpath('.gitignore')
    utils.write_lines(target, lines)


def write_standalone_cargo_toml(app_path, name):
    lines = '''\
        [package]
        name = "{name}"
        version = "0.1.0"
        edition = "2021"

        [lib]
        crate-type = ["cdylib"]

        [dependencies]
        soroban-sdk = "20.0.0"

        [dev_dependencies]
        soroban-sdk = {{ version = "20.0.0", features = ["testutils"] }}

        [features]
        testutils = ["soroban-sdk/testutils"]

        [profile.release]
        opt-level = "z"
        overflow-checks = true
        debug = 0
        strip = "symbols"
        debug-assertions = false
        panic = "abort"
        codegen-units = 1
        lto = true

        [profile.release-with-logs]
        inherits = "release"
        debug-assertions = true
    '''

    target = app_path.joinpath('Cargo.toml')
    args = {
        'name': name
    }

    utils.write_lines(target, lines, args)


def write_default_lib_rs(app_path):
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

    target = app_path.joinpath('src/lib.rs')
    utils.write_lines(target, lines)


def write_default_test_rs(app_path):
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

    target = app_path.joinpath('src/test.rs')
    utils.write_lines(target, lines)


def install_standalone_app(name):
    print(f'Installing standalone app: {name}')

    app_path = Path(name)
    app_path.mkdir(exist_ok=True)

    src_path = app_path.joinpath('src')
    src_path.mkdir(exist_ok=True)

    src_path = app_path.joinpath('.soroban')
    src_path.mkdir(exist_ok=True)

    write_soroban_dev_config(app_path, name, 'standalone')
    write_standalone_cargo_toml(app_path, name)
    write_default_lib_rs(app_path)
    write_default_test_rs(app_path)
    write_gitignore(app_path)


def install_astro_app(name):
    print(f'installing astro app: {name}')


def install_nextjs_app(name):
    print(f'installing nextjs app: {name}')
