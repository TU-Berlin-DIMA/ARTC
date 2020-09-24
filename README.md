# ARTC - Code and MQRS-Simulation
This repository hosts the demonstration code for the Adaptive Read Time Tolerance Controler (`ARTC`).
In the first section (`Setup`), we give detailed information on how you execute the paper's experiments.
In the second section (`Custom Experiments`), we discuss how to adapt both the algorithm's configuration and its execution environment (i.e., how you adjust the number of runs over which we aggregate the read-sharing potential and the error).
Lastly, we give an overview of the structure of the code in Section (`Organization of the repository`).



## 1. Setup
This section describes
which packages you have to install,
which script you have to execute for downloading and preprocessing the datasets, and
how you run the experiments presented in the paper `Automatic Tuning of Read-Time Tolerances for Optimized On-Demand Data-Streaming from Sensor Nodes`.

### 1A) Required packages
The executables `python3` as `python`, `wget`, `unzip`, and `python3-pip` as `pip` are required to run the experiments and download the datasets.
To visualize plots via `matplotlib`, a python `tkinter` backend might be required.
We provide the commands for installing them for two Linux-Distribution derivates below:

```bash
# Ubuntu-based
sudo apt install wget unzip python3
sudo apt install python3-tk
# Arch-Based
sudo pacman -S wget python unzip
sudo pacman -S python-pmw
```

### 1B) Datasets acquisition
You download and preprocess the datasets via the initialize script, which also creates a virtual python environment into which it installs required python packages.

```bash
./initialize.sh
```
After the script successfully terminates, you find the preprocessed datasets and the source data in the dataset-specific subfolder of the `data/` directory. 

**Attention**: The initialization script loads the entire datasets into main memory and requires approximately `10GB` of free main memory. 
In case you have insufficient memory to preprocess the datasets, or the links we use in this repository provided by the authors of the dataset cease to work, contact
```bash
j [dot] huelsmann [at] tu-berlin.de
```
to obtain the extracted datasets directly.

### 1C) Execution of experiments
Before executing an experiment, load the python virtual environment:

```bash
source .venv/bin/activate
```
The quantitative experiments published in the paper can be executed as follows:

```bash
source .venv/bin/activate
python3 src/run_activities.py
python3 src/run_debs.py
python3 src/run_gas.py
```
The single-trace experiment can be executed by passing a parameter to `the run_activities` script.

```bash
source .venv/bin/activate
python3 src/run_activities.py 1
```
The experimental results of the experiments are visualized in a plot via the `matplotlib` library, and become visible as soon as the experiments terminate.
Even though the ARTC algorithm itself is very lightweight, the quantitative experiments consume a lot of time, as 
1. by default, experiments are executed multiple times to reduce the effect of randomness in the
   multi-query read-scheduler simulation.
2. we log a lot of values during the experiments, that can be visualized afterwards. This logging
   requires iteration over the sensor-values at the highest available rate multiple times.

## 2. Custom experiments
You can adapt the default parameterization of the different sub-components in the file `src/globalParams.py`.

### 2A) Adapted execution environment
By default, each quantitative configuration is executed ten times, and the results are averaged. To speed up the experiments, you can decrease the number of iterations `amount_iterations` and reduce the number of samples considered for each experiment `max_amount_samples`.

**Attention**: The configuration of the fixed read time tolerance algorithm is manually selected, such that it matches the read-sharing potential of `ARTC`. 
Especially when reducing the `max_amount_samples`, the interval-radius of the Fixed read sharing algorithm might require adaptation to remain comparable to the configuration of `ARTC`.

### 2B) Adapt read-sharing algorithm
Configuration of `ARTC` and `AdaM` that remains constant throughout the experiments can also be adapted in the file `src/globalParams.py`.
The fixpoint and the interval-radius of the fixed solution can be changed in the specific experiment runner in Line (1) and (2), respectively.

```python
run_multiple(
  source_path,
  [
    [
      "[AdaM, ARTC" + str(spf) + "]",
      udsf.rtta.ARTC(spf, aP, aI, aD, d_init, alpha, beta, minIntervalDiameter, 175, -1),
      udsf.rts.Peridoci(d_init, alpha, beta, gamma, 1., minStepSize)
    ] for spf in [.01, .1, .2, .25, .3, .35, .4]                                            # (1)
  ]
  + [
    [
      "[AdaM, Fixed" + str(p) + "]",
      udsf.rtta.Fixed(p),
      udsf.rts.AdaM(d_init, alpha, beta, gamma, 1, minStepSize)
      ] for p in [0, 3.3, 6, 10, 15, 20, 29.2, 37]                                          # (1)
  ])
```

### 2C) Exchange algorithms
Additional configurations can be added (via the + operator). The `AdaM` read-time suggestion algorithm is replaced by Periodic Sampling from the listing above as follows:

```python
run_multiple(
  source_path,
  [
    [
      "[Periodic, ARTC" + str(spf) + "]",
      udsf.rtta.ARTC(spf, aP, aI, aD, d_init, alpha, beta, minIntervalDiameter, 175, -1),
      udsf.rts.Periodic(10)                                                                # (3)
    ] for spf in [.01, .1, .2, .25, .3, .35, .4]                                            
  ]
  + [
    [
      "[Periodic, Fixed" + str(p) + "]",
      udsf.rtta.Fixed(p),
      udsf.rts.Periodic(10)                                                                # (4)
      ] for p in [0, 3.3, 6, 10, 15, 20, 29.2, 37]
  ])
```

**Attention**: The configuration of the fixed read time tolerance algorithm is manually selected, such that it matches the read-sharing potential of `ARTC`. When changing the read-time suggestion algorithm, the interval-radius of the Fixed read sharing algorithm might have to be adapted to remain comparable to the configuration of `ARTC`.



## 3. Organization of the repository
The source code of the read-time suggestion algorithms (`AdaM` & `Periodic`) and the read-time tolerance algorithm (`ARTC` & `Fixed`) can be found in the module `udsf` (`src/udsf`) in the files `udsf/rts.py` and `udsf/rtta.py` respectively.
The data-package contains the dataset representation, and the code to run multiple experiments can be found in the experiments package. Utilities such as `PEWMA`, the `PID controller`, and the code used for plotting are located in the `util` package.
The workflow of read-time suggestion and evoking the read-time tolerance algorithm during multi-query read scheduling on the sensor node is implemented in the file `sensor_node.py`, which is a good starting point for familiarizing yourself with the framework.
