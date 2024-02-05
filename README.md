## Abstract

To understand the capabilities of generative models in simulating physical phenomena, this study investigates the potency of three types of generative models in generating physically accurate sound maps. In conjunction with this research, we have introduced a new dataset, comprising 100,000 samples, specifically designed for urban noise propagation studies. This dataset, derived from OpenStreetMap and annotated with sound maps generated through the NoiseModelling v4.0 framework, provides a comprehensive resource for investigating the complexities of sound dynamics in urban environments. Its diverse range of scenarios, including various sound sources and environmental complexities, offers an opportunity for testing and refining generative models in the field of acoustic simulation. Our baseline evaluation reveals that while the model performs well in baseline scenarios, its performance varies significantly when handling complex conditions, particularly in areas not in line of sight of the sound source. These findings contribute to understanding the limitations and capabilities of generative models in simulating complex physical systems.

## Dataset Description

This dataset is assembled for research into urban sound propagation, comprising 25,000 data points across 10 diverse cities. Each city is represented by 2,500 locations, offering a comprehensive analysis of various urban configurations. The dataset utilizes OpenStreetMap (OSM) imagery to detail the urban layout within a 500m x 500m area for each location, where buildings are delineated with black pixels and open spaces with white pixels.

![alt text](figures/sample_overview.drawio.svg "Title")


Supplementing the urban structural images, the dataset includes sound distribution maps at resolutions of 512x512 and 256x256. These maps are precisely generated through the [NoiseModelling v4.0](https://github.com/Universite-Gustave-Eiffel/NoiseModelling) framework, an advanced simulation tool engineered for accurate modeling of sound dynamics within urban environments.

The data collection methodology involves sourcing information via the Overpass API, subsequently refined and verified using GeoPandas to ensure the dataset's integrity and consistency. For researchers and experts interested in exploring the intricacies of sound simulation, additional insights can be obtained from the NoiseModelling framework [documentation](https://noisemodelling.readthedocs.io/en/latest/).

## Download Dataset

The dataset used for evaluation is publicly available and published via Zenodo, ensuring easy access and reproducibility of our research findings [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10609793.svg)](https://doi.org/10.5281/zenodo.10609793).

## Code for baseline experiments
The code is located at the [GitHub repository](https://github.com/urban-sound-data/urban-sound-data).

This script evaluates the accuracy of predicted sound propagation against true data using metrics such as Mean Absolute Error (MAE) and Mean Absolute Percentage Error (MAPE), with special consideration for visibility based on Open Street Map data.

```
project_root/
│
├── urban_sound_25k_baseline/
│   ├── test/
│   │   ├── test.csv
│   │   ├── soundmaps/
│   │   ├── buildings/
│   │
│   └── pred/
│       ├── y_0.png
│       └── ...
│
└── calc_test_metrics.py
```
### Running the Script

To run the evaluation, navigate to your project's root directory and execute the evaluate.py script with the required arguments:

```bash
python evaluate.py --data_dir data/true --pred_dir data/pred --output results/evaluation.csv
```
- data_dir: Path to the directory containing true labels and OSM images.
- pred_dir: Path to the directory containing predicted sound maps.
- output: Desired path for the output CSV file containing evaluation results.

### Understanding the Output

The script generates an evaluation.csv file with the following columns:

- sample_id: Unique identifier for each sample.
- MAE: Mean Absolute Error across the entire sound map.
- MAPE: Mean Absolute Percentage Error across the entire sound map.
- MAE_in_sight: MAE for areas in sight of the sound source, based on OSM data.
- MAE_not_in_sight: MAE for areas not in sight of the sound source.
- MAPE_in_sight: MAPE for areas in sight of the sound source.
- MAPE_not_in_sight: MAPE for areas not in sight of the sound source.

After running the script, you can find summary statistics in the console output, providing an overview of the evaluation metrics across all samples.


## License
This dataset is licensed under a [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International](https://creativecommons.org/licenses/by-nc-nd/4.0/)
