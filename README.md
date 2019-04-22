# cognitive_extension
Software for the cognitive extension wearable AI device.

### Setup
* Download conda
   * https://docs.anaconda.com/anaconda/install/linux/
   * On RPI 3B/3B+ install miniconda https://docs.conda.io/en/latest/miniconda.html (make sure to use the 32bit installer)
     * `wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh`
     * `md5sum Miniconda3-latest-Linux-armv7l.sh`
     * `bash Miniconda3-latest-Linux-armv7l.sh`
* Setup your conda environment using the `environment.yaml`
* Perform a `conda env export > environment.yaml` in the base directory whenever packages are updated
