[![Build Status](https://travis-ci.org/jpata/particleflow.svg?branch=master)](https://travis-ci.org/jpata/particleflow)

Notes on modernizing CMS particle flow with machine learning. Internal documentation and results can be found at https://twiki.cern.ch/twiki/bin/view/CMS/MLParticleFlow.

Quickstart with training:

```
#get the code
git clone https://github.com/jpata/particleflow.git
cd particleflow

#run a small local test including data prep and training
./scripts/local_test.sh
```

# Overview

- [x] set up datasets and ntuples for detailed PF analysis
  - [x] advanced CMSSW version with generator truth in [Validation/RecoParticleFlow/PFAnalysis.cc](https://github.com/jpata/cmssw/blob/jpata_pfntuplizer/Validation/RecoParticleFlow/plugins/PFAnalysis.cc)
- [x] reproduce existing PFCandidates with machine learning
  - [x] end-to-end training of elements to MLPF-candidates using GNN-s
- [ ] reconstruct genparticles directly from detector elements a la HGCAL, neutrino experiments etc
  - [x] set up datasets for regression genparticles from elements
  - [x] Develop a baseline ML-PF model that is able to regress pions and neutral hadrons
  - [ ] develop improved loss function for event-to-event comparison: EMD, GAN
  - [ ] Improve ML-PF model physics performance 
  - [ ] Improve ML-PF model computational performance 
  - [x] Create CMSSW EDProducer for ML-PF particles
  - [x] GPU-evaluation of MLPFProducer in CMSSW
  - [x] Implement a simple tensorflow based ML-PF training for evalutation in CMSSW
- [ ] GPU code for existing PF algorithms
  - [x] test CLUE for element to block clustering
  - [ ] port CLUE to PFBlockAlgo in CMSSW
  - [ ] parallelize PFAlgo calls on blocks
  - [ ] GPU-implementation of PFAlgo
  - [ ] GPU-implementation of PFBlockAlgo distances

## Presentations

- CMS ML Forum, 2020-09-30: https://indico.cern.ch/event/952419/contributions/4041555/attachments/2113070/3554608/2020_09_30.pdf
- CMS ML Town Hall, 2020-07-03: https://indico.cern.ch/event/922319/contributions/3928284/attachments/2068518/3472668/2020_07_02.pdf
- FastML meeting, 2020-05-29: https://indico.cern.ch/event/923986/contributions/3883991/attachments/2047940/3431648/2020_05_28.pdf
- CMS PF group, 2020-05-22: https://indico.cern.ch/event/921949/contributions/3873351/attachments/2042984/3422056/2020_05_22.pdf
- CMS scouting group, 2020-05-15: https://indico.cern.ch/event/894101/contributions/3862093/attachments/2038019/3412747/2020_05_13.pdf
- CMS PF group, 2020-04-24: https://indico.cern.ch/event/912351/contributions/3839281/attachments/2026117/3389540/2020_04_24.pdf
- Caltech CMS group ML meeting, 2020-04-16: https://indico.cern.ch/event/909688/contributions/3826957/attachments/2021475/3380133/2020_04_15_caltechml.pdf
- ML4RECO meeting, 2020-04-09: https://indico.cern.ch/event/908361/contributions/3821957/attachments/2017888/3373038/2020_04_08.pdf
- CMS PF group, 2020-03-13: https://indico.cern.ch/event/897397/contributions/3786360/attachments/2003108/3344534/2020_03_13.pdf
- ML4RECO meeting, 2020-03-12: https://indico.cern.ch/event/897281/contributions/3784715/attachments/2002839/3343921/2020_03_12.pdf
- ML4RECO meeting, 2020-03-04: https://indico.cern.ch/event/895228/contributions/3776739/attachments/1998928/3335497/2020_03_04.pdf
- CMS PF group, 2020-02-28: https://indico.cern.ch/event/892992/contributions/3766807/attachments/1995348/3328771/2020_02_28.pdf
- CMS PF group, 2020-01-31: https://indico.cern.ch/event/885043/contributions/3730304/attachments/1979098/3295074/2020_01_30_pf.pdf
- FNAL HGCAL ML meeting, 2020-01-30: https://indico.cern.ch/event/884801/contributions/3730336/attachments/1978912/3294638/2020_01_30.pdf
- Caltech group meeting, 2020-01-28: https://indico.cern.ch/event/881683/contributions/3714961/attachments/1977131/3291096/2020_01_21.pdf
- CMS PF group, 2020-01-17: https://indico.cern.ch/event/862200/contributions/3706909/attachments/1971145/3279010/2020_01_16.pdf
- CMS PF group, 2019-11-22: https://indico.cern.ch/event/862195/contributions/3649510/attachments/1949957/3236487/2019_11_22.pdf
- CMS PF group, 2019-11-08: https://indico.cern.ch/event/861409/contributions/3632204/attachments/1941376/3219105/2019_11_08.pdf
- Caltech ML meeting, 2019-10-31: https://indico.cern.ch/event/858644/contributions/3623446/attachments/1936711/3209684/2019_10_07_pf.pdf
- Caltech ML meeting, 2019-09-19: https://indico.cern.ch/event/849944/contributions/3572113/attachments/1911520/3158764/2019_09_18_pf_ml.pdf
- CMS PF group, 2019-09-10: https://indico.cern.ch/event/846887/contributions/3557300/attachments/1904664/3145310/2019_09_10_pf_refactoring.pdf
- Caltech ML meeting, 2019-09-05: https://indico.cern.ch/event/845349/contributions/3554787/attachments/1902837/3141723/2019_09_05_pfalgo.pdf

In case the above links do not load, the presentations are also mirrored on the following CERNBox link: https://cernbox.cern.ch/index.php/s/GkIRJU1YZuai4ix

## Acknowledgements

This project is supported by the Mobilitas Pluss Returning Researcher Grant MOBTP187 of the Estonian Research Council. Part of this work was conducted at **iBanks**, the AI GPU cluster at Caltech. We acknowledge NVIDIA, SuperMicro and the Kavli Foundation for their support of **iBanks**. 


## CMSSW recipe

Evaluation recipe in CMSSW:

```
cmsrel CMSSW_11_2_DEVEL_X_2020-11-01-2300
cd CMSSW_11_2_DEVEL_X_2020-11-01-2300
cmsenv
git cms-merge-topic jpata:mlpfproducer
scram b -j4

mkdir -p src/RecoParticleFlow/PFProducer/data/mlpf
wget http://jpata.web.cern.ch/jpata/mlpf/mlpf_2020_10_27.pb -O src/RecoParticleFlow/PFProducer/data/mlpf/mlpf_2020_10_27.pb

#Phase 2: timing extraction
runTheMatrix.py -l 23434.21 -w upgrade --command="-n 100 --nThreads 2 --customise Validation/Performance/TimeMemoryInfo.customise --customise RecoParticleFlow/PFProducer/mlpfproducer_customise.customise_step3_aod"

#Run 3: physics performance checks
runTheMatrix.py -l 11834.0 -w upgrade --command="-n 100 --nThreads 2 --customise Validation/Performance/TimeMemoryInfo.customise --customise RecoParticleFlow/PFProducer/mlpfproducer_customise.customise_step3_reco"
```

Retraining recipe:

```
cmsrel CMSSW_11_2_DEVEL_X_2020-11-01-2300
cd CMSSW_11_2_DEVEL_X_2020-11-01-2300
cmsenv
git cms-merge-topic jpata:mlpfproducer
scram b -j4

#TF 2.3 is needed for training, run this once only
cd src/RecoParticleFlow/PFProducer/test/mlpf_training
python3 -m venv training_env
source training_env/bin/activate
pip3 install --upgrade pip
pip3 install tensorflow==2.3 protobuf==3.13 google-cloud==0.34

#retrain on data provided by the MLPF team
source training_env/bin/activate
python3 tf_model.py --datapath /eos/user/j/jpata/www/particleflow/TTbar_14TeV_TuneCUETP8M1_cfi/
deactivate

#generate your own data and run an example training on it
./run.sh
```