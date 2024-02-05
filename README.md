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

## Baseline Results

The table below presents baseline performance metrics for various architectural approaches, encompassing combined mean absolute error (MAE) and weighted mean absolute percentage error (wMAPE), alongside specific line-of-sight (LoS) and non-line-of-sight (NLoS) metrics. These results are published in our paper, which can be accessed [here]().

| Architecture | Condition   | Combined MAE | Combined wMAPE | LoS MAE | NLoS MAE | LoS wMAPE | NLoS wMAPE |
|--------------|-------------|--------------|----------------|---------|----------|-----------|------------|
| UNet         | Baseline    | 2.08         | 19.45          | 2.29    | 1.73     | 12.91     | 37.57      |
| UNet         | Diffraction | 1.65         | 9.75           | 0.94    | 3.27     | 4.22      | 22.36      |
| UNet         | Reflection  | 3.22         | 31.87          | 2.29    | 5.72     | 12.75     | 80.46      |
| UNet         | Name        | 1.77         | 20.59          | 1.03    | 2.29     | 8.23      | 38.13      |
| GAN          | Baseline    | 1.52         | 8.21           | 1.73    | 1.19     | 9.36      | 6.75       |
| GAN          | Diffraction | 1.66         | 8.03           | 0.91    | 3.36     | 3.51      | 18.06      |
| GAN          | Reflection  | 2.88         | 16.57          | 2.14    | 4.79     | 11.30     | 30.67      |
| GAN          | Name        | 1.76         | 19.12          | 1.37    | 2.67     | 9.80      | 40.68      |
| Diffusion    | Baseline    | 2.57         | 25.21          | 2.42    | 3.26     | 15.57     | 51.08      |
| Diffusion    | Diffraction | 2.12         | 11.85          | 1.59    | 3.27     | 8.25      | 20.30      |
| Diffusion    | Reflection  | 4.14         | 35.20          | 2.74    | 7.93     | 17.85     | 80.38      |
| Diffusion    | Name        | 1.57         | 21.55          | 1.26    | 2.21     | 13.10     | 40.57      |





## License
This dataset is licensed under a [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International](https://creativecommons.org/licenses/by-nc-nd/4.0/)
