import numpy as np
from PIL import Image
import numba
from numba import jit
import argparse
import os
import pandas as pd

def MAE(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def calc_mae(true_path, pred_path):
    pred_noisemap = np.array(
        Image.open(pred_path).convert("L"),
        dtype=np.int32
    )
    true_noisemap = np.array(
        Image.open(true_path).convert("L"),
        dtype=np.int32
    )
    return MAE(true_noisemap, pred_noisemap)

def calc_mape(true_path, pred_path):
    pred_noisemap = np.array(
        Image.open(pred_path).convert("L"),
        dtype=np.int32
    )
    true_noisemap = np.array(
        Image.open(true_path).convert("L"),
        dtype=np.float32
    )
    return np.mean(np.abs((true_noisemap - pred_noisemap) / true_noisemap)) * 100


@jit(nopython=True)
def ray_tracing(image_size, image_map):
    visibility_map = np.zeros((image_size, image_size))
    source = (image_size // 2, image_size // 2)
    for x in range(image_size):
        for y in range(image_size):
            dx = x - source[0]
            dy = y - source[1]
            dist = np.sqrt(dx*dx + dy*dy)
            steps = int(dist)
            if steps == 0:
                continue  # Skip the source point itself
            step_dx = dx / steps
            step_dy = dy / steps

            visible = True  # Assume this point is visible unless proven otherwise
            ray_x, ray_y = source
            for _ in range(steps):
                ray_x += step_dx
                ray_y += step_dy
                int_x, int_y = int(ray_x), int(ray_y)
                if 0 <= int_x < image_size and 0 <= int_y < image_size:
                    if image_map[int_y, int_x] == 0:
                        visible = False
                        break
            visibility_map[y, x] = visible
    return visibility_map

def compute_visibility(osm_path, image_size=256):
    image_map = np.array(Image.open(osm_path).convert('L').resize((image_size, image_size)))
    image_map = np.where(image_map > 0, 1, 0)
    visibility_map = ray_tracing(image_size, image_map)
    pixels_in_sight = np.logical_and(visibility_map == 1, image_map == 1)
    pixels_not_in_sight = np.logical_and(visibility_map == 0, image_map == 1)
    pixels_not_in_sight = np.where(image_map == 0, 0, pixels_not_in_sight)
    pixels_in_sight = np.where(image_map == 0, 0, pixels_in_sight)
    return pixels_in_sight, pixels_not_in_sight

def masked_mae(true_labels, predictions):
    # Convert to numpy arrays
    true_labels = np.array(true_labels)
    predictions = np.array(predictions)
    
    # Create a mask where true_labels are not equal to -1
    mask = true_labels != -1
    
    # Filter arrays with the mask
    true_labels = true_labels[mask]
    predictions = predictions[mask]
    
    # Compute the MAE and return
    return np.mean(np.abs(true_labels - predictions))

def masked_error(true_labels, predictions):
    # Convert to numpy arrays
    true_labels = np.array(true_labels)
    predictions = np.array(predictions)
    
    # Create a mask where true_labels are not equal to -1
    mask = true_labels != -1
    
    # Filter arrays with the mask
    true_labels = true_labels[mask]
    predictions = predictions[mask]
    
    return np.abs(true_labels - predictions)


def calculate_sight_error(true_path, pred_path, osm_path):
    true_soundmap = (255 - np.array(
        Image.open(true_path).convert("L"),
        dtype=np.int16
    )) / 255 * 100
    pred_soundmap = (255 - np.array(
        Image.open(pred_path).convert("L"),
        dtype=np.int16
    )) / 255 * 100
    _, true_pixels_not_in_sight = compute_visibility(osm_path)

    in_sight_soundmap = true_soundmap.copy()
    not_in_sight_soundmap = true_soundmap.copy()
    
    in_sight_pred_soundmap = pred_soundmap.copy()
    not_in_sight_pred_soundmap = pred_soundmap.copy()
    
    #only get the pixels in sight
    for x in range(256):
        for y in range(256):
            if true_pixels_not_in_sight[y, x] == 0:
                not_in_sight_soundmap[y, x] = -1
                not_in_sight_pred_soundmap[y, x] = -1
            else:
                in_sight_soundmap[y, x] = -1
                in_sight_pred_soundmap[y, x] = -1

    return masked_mae(in_sight_soundmap, in_sight_pred_soundmap), masked_mae(not_in_sight_soundmap, not_in_sight_pred_soundmap)


def evaluate_sample(true_path, pred_path, osm_path=None) -> (float, float, float, float):
    mae = calc_mae(true_path, pred_path)
    mape = calc_mape(true_path, pred_path)

    mae_in_sight, mae_not_in_sight = None, None
    if osm_path is not None:
        mae_in_sight, mae_not_in_sight = calculate_sight_error(true_path, pred_path, osm_path)
    return mae, mape, mae_in_sight, mae_not_in_sight

## main function for evaluation
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="data/true")
    parser.add_argument("--pred_dir", type=str, default="data/pred")
    parser.add_argument("--output", type=str, default="evaluation.csv")
    args = parser.parse_args()

    data_dir = args.data_dir
    pred_dir = args.pred_dir
    output = args.output


    dataset_df = pd.read_csv(f"{data_dir}/dataset.csv")

    # get test set based on last 5% of the dataset
    test_df = dataset_df.iloc[int(len(dataset_df) * 0.95)+1:].reset_index(drop=True)[:100]

    results = []
    for index, sample_row in test_df.iterrows():
        # print progress
        if index % 100 == 0:
            print(f"Progress: {index}/{len(test_df)}")

        # check if prediction is available
        if not os.path.exists(f"{pred_dir}/y_0_{index}.png"):
            print(f"Prediction for sample {index} not found.")
            continue
        mae, mape, mae_in_sight, mae_not_in_sight = evaluate_sample(os.path.join(data_dir, sample_row.soundmap), f"{pred_dir}/y_0_{index}.png", os.path.join(data_dir, sample_row.osm)) # adjust prediction naming if needed
        results.append([sample_row.sample_id, mae, mape, mae_in_sight, mae_not_in_sight])

    results = pd.DataFrame(results, columns=["sample_id", "MAE", "MAPE", "MAE_in_sight", "MAE_not_in_sight"])
    results.to_csv(output, index=False)
    print(results[[ "MAE", "MAPE", "MAE_in_sight", "MAE_not_in_sight"]].describe())
