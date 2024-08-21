<!--
Copyright 2018-2024 Fragment Contributors
SPDX-License-Identifier: Apache-2.0
-->
# Fragme∩t 🔨🪞

Fragme∩t is a fragmentation framework developed by the John Herbert Research group at the Ohio State University. Our goal is to write a package that makes it easy to prototype, implement, and benchmark fragmentation methods. The code is currently in a pre-release state so be aware that features and backwards compatibility are subject to change.

# Install 

Use the following script to get up and running. It assumes you are 
a working Conda installation and that you are subscribed to [conda-forge](https://conda-forge.org).

This script will install the `v0.3.0` version of Fragme∩t into a Conda environment named `fragment`.

```sh
# Create a conda env and install depenencies!
conda create -n fragment "python=3.9" xtb xtb-python 
conda activate fragment

# Instal v0.3.0 of fragment
pip install https://gitlab.com/john-herbert-group/fragment/-/archive/v0.3.0pre/fragment-v0.3.0pre.tar.gz

# Test that fragment is installed 
fragment --help
```

# Getting Started

Suppose we have a cluster comprised of 6 water molecules. This can be run as a fragmentation job using the following steps

## 1. Create a project directory
```sh
mkdir water6
cd water6
fragment project init
```

You should now have a `logs` directory, a `fragment.db` database, and a `file_archive.tar` file.

## 2. Get the `.xyz` formatted file

Save this as `water6.xyz`.

```
18
A water 6 cluster in the book configure.
O   -2.294815470802032    -0.35340370829457846   -1.4570963322795638
H   -2.881960438102032    0.12296588740542158   -2.049739388579564
H   -1.4102172378020317    0.0745683714054215   -1.5604491547795636
O   0.09080023389796821    0.8777598392054216   -1.3863453437795636
H   0.9061376199979683    0.35842413990542155   -1.5279466229795637
H   0.12531031699796824    1.1077412038054215   -0.4452916094795637
O   2.4281271808979685    -0.6521726431945785   -1.3760463098795637
H   3.2654530112979683    -0.28879311869457847   -1.6763763469795636
H   2.4976507488979682    -0.6843279777945785   -0.4011477284795637
O   2.2817380552979682    -0.5383498417945785   1.3854233763204364
H   1.4467584053979683    -0.05854153339457846   1.550018357920436
H   2.238419010497968    -1.3234545270945783   1.9375358894204364
O   -2.4377266432020317    -0.26947301679457847   1.2235689994204364
H   -2.507481045702032    -0.3329421837945785   0.24094004432043636
H   -2.6210014391020318    -1.1546355394945784   1.5493709378204361
O   -0.06454193420203169    0.9356625749054215   1.5322085106204364
H   -0.17310714100203173    1.6967814865054214   2.1094337979204365
H   -0.9428015757020318    0.48184552640542144   1.5161249055204364
```

## 3. Create a strategy file

fragmention calculations are described using .yaml files. Save the following file as `strategy.yaml`.

```yaml
systems: # Import our systems
  -
    name: w6
    note: water 6 # A note with more information
    source: water6.xyz # Path to the .xyz file we made in step 2

fragmenters:
  - # Describe a fragmenter. The "Water" fragmenter will split a water-only system into
    # indivdual water molecules
    name: waterMBE
    note: Fragmeter for water
    fragmenter: Water

backends:
  - # We will be using xTB as a library
    name: xTB
    note: xTB/GFN2 backend
    program: libxtb

calculations: # Describe our calculation
  -
    name: mbe5
    system: ALL # Run this calculation on all systems (just water 6 in this case)
    note: MBE(5) Calculation
    layers:
      -
        backend: xTB # Run calculations with xTB
        view:
          fragmenter: waterMBE # Use the fragmenter we just defined
          order: 5  # Do an MBE(5 calculation)

```

Now let fragment know about it by running `fragment strategy add strategy.yaml`.

# 4. Run the calculations

If you run `fragment project info` you should see 62 pending jobs. To run these, run `fragment calc run ALL`. You can list all defined calculations using `fragment calc list` and see the details of our calculation using `fragment calc info mbe5__w6`.

You should get a total energy of ~-30.49198 Eh. You can compare this to the supersystem energy from xTB (`xtb water6.xyz`).

<!-- The documentation is out of date and has lots of YAML formatting errors... -->
<!-- # Documentation
Work-in-progress documentation can be found at https://john-herbert-group.gitlab.io/fragment -->