# Gehirn

Learning to play tetris in Python using NEAT, Deep-Q networks, and Linear-Q networks. The best approach so far has been to use NEAT, but the current Python library does not support GPU usage and this severly hinders the training speed. This personal project is a work in progress and is intended as a way to explore machine learning outside of a classroom environment.

### Machine Learning Libraries
  - Pytorch
  - Neat

# Table of Contents
<!-- toc -->
### Model Training and Display Code [](https://github.com/NoahFrahm/Gehirn/tree/master/ml/ml_model_games)
  - [Playable tetris game](https://github.com/NoahFrahm/Gehirn/blob/master/tetris_noah.py)
  - [NEAT Training file that also renders UI of the games being played](https://github.com/NoahFrahm/Gehirn/blob/master/ml/ml_training/NEAT/displayed_NEAT_ml.py)
  - [NEAT Training file without any UI](https://github.com/NoahFrahm/Gehirn/blob/master/ml/ml_training/NEAT/tetris_NEAT_hookup.py)
  - [File that runs trained NEAT model with tetris UI](https://github.com/NoahFrahm/Gehirn/blob/master/ml/ml_training/NEAT/display_trained_model.py)
 
### Models
  - [Trained NEAT Models](https://github.com/NoahFrahm/Gehirn/tree/master/models/NEAT%20models)

### Model Configuration Files
  - [Config files](https://github.com/NoahFrahm/Gehirn/tree/master/ml/config_files)
  
### Notes
  - [Planning file for model parameters](https://github.com/NoahFrahm/Gehirn/blob/master/Notes/NEAT_model_notes.txt)
  - [Results of different training configurations](https://github.com/NoahFrahm/Gehirn/blob/master/Notes/NEAT_training_config_results.txt)
  - [Project progress](https://github.com/NoahFrahm/Gehirn/blob/master/Notes/project_progress.txt)
