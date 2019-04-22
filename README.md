# cognitive_extension
Software for the cognitive extension wearable AI device.

### Setup
* Download conda
   * https://docs.anaconda.com/anaconda/install/linux/
   * On RPI 3B/3B+ install berryconda https://github.com/jjhelmus/berryconda
* Setup your conda environment using the `environment.yaml`
   * If you are creating the environment on a RPI create from `environment_rpi.yaml` (note: this uses python 3.6 not 3.7)
   * On the RPI the environment is activated using `source activate cognitive_extension` and deactivated using `source deactivate`
   * On the RPI you will need to pip install the following packages manually
      * `pip install RPi.GPIO`
      * `pip install adafruit_gpio`
* Perform a `conda env export > environment.yaml` (or `environment_rpi.yaml`) in the base directory whenever packages are updated

