# About

Sorodev is a CLI tool and Python package which allows to develop with [Soroban](https://soroban.stellar.org/) more efficiently. 

It is designed for Linux systems (Debian, WSL, ...)



### Why?

While [soroban-cli](https://soroban.stellar.org/docs/reference/soroban-cli) is like a Swiss knife to interact with Soroban, it also requires many arguments and parameters to specify the context, such as the current network being used, the last deployment addresses, ...

Similarly, Rust is a generic and customizable language, which requires to replicate the same patterns for each contract.

The idea behind `sorodev` is to provide the setup to get started with a development on Soroban and to bring some tools on top of `soroban-cli`.

For example:
- create new Soroban projects and contracts (create default `Cargo.toml`, `lib.rs`, `test.rs`)
- use a `sorodev.json` to configure the current parameters
- build, test, deploy, invoke contracts, or make contract bindings with simple commands

To sum up, Sorodev indends to make it easier for anyone to start developping on Soroban and to enable a more efficient development experience.

However, it's recommended to understand both the [Soroban development setup](https://soroban.stellar.org/docs/category/getting-started) and [how Sorodev works](https://github.com/flokapi/sorodev/tree/main/src/sorodev).


# Getting started

## Installation

### Install Soroban

Install Rust

```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Install the WebAssembly compilation target

```
rustup target add wasm32-unknown-unknown
```

Install `soroban-cli`

```
cargo install soroban-cli
```



### Install Sorodev

```shell
pip install sorodev
```



## Standalone project

```shell
mkdir example
cd example

sorodev install
sorodev add-contract hello_soroban
sorodev add-account alice
sorodev build
sorodev test
sorodev deploy hello_soroban
sorodev invoke hello_soroban hello --args "--to Sorodev"
```



## Create an Astro project

```shell
npm create astro@4.0.1 example_astro --\
	--template basics\
	--install\
	--no-git\
	--typescript strictest

cd example_astro

sorodev install
sorodev add-contract hello_soroban
sorodev add-account alice
sorodev build
sorodev deploy hello_soroban
sorodev make-binding hello_soroban
```


In `pages/index.astro`, add the following lines:

```jsx
---
import Layout from "../layouts/Layout.astro";
import Card from "../components/Card.astro";

+ import { Contract, networks } from "hello_soroban-client";

+ const greeter = new Contract({
+   ...networks.testnet,
+   rpcUrl: "https://soroban-testnet.stellar.org",
+ });
+ 
+ const { result } = await greeter.hello({ to: "Sorodev" });
---
```



```jsx
- <h1>Welcome to <span class="text-gradient">Astro</span></h1>
+ <h1><span class="text-gradient">{result.join(" ")}</span></h1>
```



In the `package.json`, add the following script:

```
"scripts": {
    ...
    "postinstall": "sorodev build && sorodev deploy hello_soroban && sorodev make-binding hello_soroban"
}
```



Then run:

```shell
npm i
npm run dev
```
Then open `http://localhost:4321/`, you should see `Hello Sorodev`.


## Create a Next.js project
