# AFib Prediction
### Step 1: Download the training data.

For PhysioNet 2017
[Download training data](https://physionet.org/content/challenge-2017/1.0.0/)

For MIT-BIT 
[Download training data](https://github.com/dhiah-dev/Dataset-Compiled-ECG-MIT-BIH-Arrhythmia)


### Step 2: Make sure to setup the environment.
Some libraries require older version of numpy (1.3.25) to work correctly.
We recommend you start from a clean environment using the following commands:

conda create --name afib  python=3.9
conda activate afiv
pip install -r requirements.txt

### References and Citations

[1] Pan, J. and Tompkins, W., 1985. A Real-Time QRS Detection Algorithm. IEEE Transactions on Biomedical Engineering, BME-32(3), pp.230-236.

https://github.com/antimattercorrade/Pan_Tompkins_QRS_Detection
