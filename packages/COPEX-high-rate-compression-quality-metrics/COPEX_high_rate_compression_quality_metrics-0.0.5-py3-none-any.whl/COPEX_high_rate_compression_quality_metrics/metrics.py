import importlib.metadata as lib_meta
import math
import os.path
from datetime import datetime
from typing import Dict, Any

import importlib_metadata  # Pour obtenir des informations sur les packages installés

import numpy as np
from skimage import io
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import mean_squared_error
import lpips
import torch


def initialize_LPIPS() -> lpips.LPIPS:
    """
    Initializes and returns an LPIPS model using the AlexNet architecture.

    LPIPS (Learned Perceptual Image Patch Similarity) is a perceptual metric
    used to evaluate the similarity between two images. The 'net' parameter
    specifies the neural network architecture to use, in this case, 'alex'
    refers to AlexNet.

    Returns:
        lpips.LPIPS: An instance of the LPIPS model initialized with AlexNet.
    """
    # Initialize the LPIPS model with the 'alex' network (AlexNet).
    lpips_model = lpips.LPIPS(net='alex',verbose=False)

    # Return the initialized LPIPS model.
    return lpips_model



def preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Preprocess an image for use with the LPIPS model.

    This function normalizes the pixel values of the input image to the range
    [-1, 1], which is required for the LPIPS model.

    Args:
        image (np.ndarray): The input image as a NumPy array.

    Returns:
        np.ndarray: The preprocessed image with pixel values normalized
                    to the range [-1, 1].
    """
    # Convert the image to float32 for precision in further calculations
    image = image.astype(np.float32)

    # Normalize the image to the range [0, 1]
    image = (image - np.min(image)) / (np.max(image) - np.min(image))

    # Scale the image to the range [-1, 1], as required by the LPIPS model
    image = image * 2 - 1

    return image


def convert_to_rgb(image: np.ndarray) -> np.ndarray:
    """
    Convert an image to a 3-channel RGB format if necessary.

    This function ensures that the input image has three channels (RGB). If the image
    is grayscale (2D), it is repeated across three channels. If the image has more
    than three channels, only the first three are retained.

    Args:
        image (np.ndarray): The input image as a NumPy array. It can be grayscale
                            (2D) or have multiple channels (3D).

    Returns:
        np.ndarray: The converted RGB image with three channels.

    Raises:
        ValueError: If the input image does not have 2 or 3 dimensions.
    """

    if image.ndim == 2:
        #print("Grayscale image detected, converting to 3 channels (RGB)...")
        # Image is grayscale (2D), so we repeat the single channel three times to create an RGB image
        image_rgb = np.repeat(image[:, :, np.newaxis], 3, axis=2)

    elif image.ndim == 3:
        n_bands = image.shape[2]
        if n_bands == 3:
            # If the image already has 3 channels, no conversion is needed
            image_rgb = image
        elif n_bands == 1:
            # If the image has a single channel, repeat it across three channels to create an RGB image
            image_rgb = np.repeat(image, 3, axis=2)
        else:
            # If the image has more than 3 channels, take only the first three
            if n_bands < 3:
                # Special case where there are fewer than 3 channels, repeat them to create 3 channels
                image_rgb = np.repeat(image, 3, axis=2)
            else:
                # Use only the first three channels to create an RGB image
                image_rgb = image[:, :, :3]

    else:
        raise ValueError("The input image must have ndim = 2 or 3 .")

    return image_rgb


def calculate_rmse(image1: np.ndarray, image2: np.ndarray) -> float:
    """
    Calculate the Root Mean Square Error (RMSE) between two multi-band images.

    RMSE is a standard metric used to measure the difference between two images.
    It is particularly useful for comparing image quality, where lower values indicate
    greater similarity.

    Args:
        image1 (np.ndarray): The first image as a NumPy array.
        image2 (np.ndarray): The second image as a NumPy array.

    Returns:
        float: The RMSE value between the two images.

    Raises:
        ValueError: If the input images do not have the same shape.
    """
    # Ensure both images have the same shape
    if image1.shape != image2.shape:
        raise ValueError("Both images must have the same dimensions.")

    # Calculate the Mean Squared Error (MSE) between the two images
    mse_value = mean_squared_error(image1, image2)

    # Calculate the Root Mean Square Error (RMSE) from the MSE
    rmse_value = np.sqrt(mse_value)

    return rmse_value


def calculate_psnr(image1: np.ndarray, image2: np.ndarray) -> float:
    """
    Calculate the Peak Signal-to-Noise Ratio (PSNR) between two multi-band images.

    PSNR is a common metric used to measure the quality of reconstruction of images.
    Higher PSNR values generally indicate better image quality, where the two images
    are more similar.

    Args:
        image1 (np.ndarray): The first image as a NumPy array.
        image2 (np.ndarray): The second image as a NumPy array.

    Returns:
        float: The PSNR value between the two images in decibels (dB).

    Raises:
        ValueError: If the input images do not have the same shape.
    """
    # Ensure both images have the same shape
    if image1.shape != image2.shape:
        raise ValueError("Both images must have the same dimensions.")

    # Calculate the PSNR value considering the data range of the images
    psnr_value = psnr(image1, image2, data_range=image1.max() - image1.min())

    return psnr_value


def calculate_ssim_multiband(image1: np.ndarray, image2: np.ndarray) -> float:
    """
    Calculate the average Structural Similarity Index (SSIM) between two images,
    processing each band separately for multi-band images.

    The SSIM metric is used to measure the similarity between two images. It is
    particularly useful for assessing image quality where higher values indicate
    better similarity. For multi-band images, SSIM is computed for each band separately
    and then averaged.

    Args:
        image1 (np.ndarray): The first image as a NumPy array (HxWxC or HxW).
        image2 (np.ndarray): The second image as a NumPy array (HxWxC or HxW).

    Returns:
        float: The average SSIM value between the two images.

    Raises:
        ValueError: If the input images do not have the same shape or have more than 3 dimensions.
    """
    # Ensure both images have the same shape
    if image1.shape != image2.shape:
        raise ValueError("Both images must have the same dimensions.")

    # Determine if the image is multi-band (3D) or single-band (2D)
    if image1.ndim == 3:
        # Multi-band image
        ssim_values = []
        for band in range(image1.shape[2]):
            # Calculate data range for each band
            data_range = max(image1[:, :, band].max() - image1[:, :, band].min(),
                             image2[:, :, band].max() - image2[:, :, band].min())
            # Calculate SSIM for each band
            ssim_value = ssim(image1[:, :, band], image2[:, :, band], data_range=data_range)
            ssim_values.append(ssim_value)

        # Compute the average SSIM value across all bands
        return np.mean(ssim_values)

    elif image1.ndim == 2:
        # Single-band image
        data_range = max(image1.max() - image1.min(), image2.max() - image2.min())
        return ssim(image1, image2, data_range=data_range)

    else:
        raise ValueError("Images must be either 2D or 3D.")


def calculate_lpips_multiband(image1: np.ndarray, image2: np.ndarray, loss_fn) -> (list, float):
    """
    Calculate the Learned Perceptual Image Patch Similarity (LPIPS) between two images,
    handling images with different dimensions and channels.

    LPIPS is a metric used to evaluate the perceptual similarity between images. It
    considers the learned features from a deep network and provides a similarity score.

    Args:
        image1 (np.ndarray): The first image as a NumPy array (HxWxC or HxW).
        image2 (np.ndarray): The second image as a NumPy array (HxWxC or HxW).
        loss_fn: A function that computes the LPIPS score given two image tensors.

    Returns:
        tuple: A tuple containing:
            - A list of LPIPS values for each band (or a single value if the image has 3 channels).
            - The average LPIPS value across bands (or the LPIPS value itself if the image has 3 channels).

    Raises:
        ValueError: If the input images do not have the same shape.
    """
    # Preprocess the images
    image1 = preprocess_image(image1)
    image2 = preprocess_image(image2)

    # Convert images to RGB if necessary (particularly if they are grayscale)
    if image1.ndim == 2:
        image1 = convert_to_rgb(image1)
    if image2.ndim == 2:
        image2 = convert_to_rgb(image2)

    # Convert images to torch tensors and permute dimensions for LPIPS calculation
    image1_tensor = torch.tensor(image1).permute(2, 0, 1).unsqueeze(0).float()
    image2_tensor = torch.tensor(image2).permute(2, 0, 1).unsqueeze(0).float()

    if image1_tensor.shape[1] == 3:
        # Case where the image already has three channels (RGB)
        lpips_value = loss_fn(image1_tensor, image2_tensor).item()
        return [lpips_value], lpips_value

    else:
        # Case where the image has more than three channels (multi-band)
        n_bands = image1.shape[2]
        lpips_values = []

        for i in range(n_bands):
            # Convert each band to RGB format
            image1_band = np.repeat(image1[:, :, i:i + 1], 3, axis=2)
            image2_band = np.repeat(image2[:, :, i:i + 1], 3, axis=2)

            # Convert the bands to torch tensors
            image1_band_tensor = torch.tensor(image1_band).permute(2, 0, 1).unsqueeze(0).float()
            image2_band_tensor = torch.tensor(image2_band).permute(2, 0, 1).unsqueeze(0).float()

            # Calculate LPIPS for this band
            lpips_value = loss_fn(image1_band_tensor, image2_band_tensor).item()
            lpips_values.append(lpips_value)

        # Compute the average LPIPS value across bands
        mean_lpips = np.mean(lpips_values)
        return lpips_values, mean_lpips


def calculate_metrics_statistics(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule la moyenne et l'écart type des valeurs dans les métriques et ajoute ces informations au dictionnaire.

    Args:
        data (Dict[str, Any]): Dictionnaire contenant les métriques avec les valeurs associées aux fichiers TIFF sous la clé 'results'.

    Returns:
        Dict[str, Any]: Dictionnaire mis à jour avec les statistiques de la métrique.
    """
    metrics = data.get("metrics", {})

    # Parcours des métriques dans le dictionnaire
    for metric_name, metric_data in metrics.items():
        # Vérifie si la clé est un dictionnaire de métriques
        if isinstance(metric_data, dict) and 'results' in metric_data:
            results = metric_data['results']

            # Filtrer uniquement les valeurs numériques des fichiers TIFF
            values = list(results.values())

            if values:
                # Calculer la moyenne et l'écart type
                try :
                    average = np.mean(values)
                    # Ajouter les statistiques au dictionnaire des métriques
                    metrics[metric_name]['average'] = round(average, 3)  # Arrondir pour la lisibilité
                except:
                    average = None
                    metrics[metric_name]['average'] = "None"  # Arrondir pour la lisibilité
                try:
                    stdev = np.std(values)
                    metrics[metric_name]['stdev'] = round(stdev, 3)  # Arrondir pour la lisibilité
                except:
                    average = None
                    metrics[metric_name]['stdev'] = "None"  # Arrondir pour la lisibilité



    return data

def calculate_lrsp(image1_path, image2_path) -> dict:
    loss_fn = initialize_LPIPS()
    # load images and show shapes
    image1 = io.imread(image1_path)
    # print(image1, " [shape =", image1.shape, ", min =", np.min(image1), ", max =", np.max(image1), ", dtype = ",
    # image1.dtype, "]")
    image2 = io.imread(image2_path)
    # print(image2, " [shape =", image2.shape, ", min =", np.min(image2), ", max =", np.max(image2), ", dtype = ",
    # image2.dtype, "]")

    # checking if images have the same shape
    if image1.shape != image2.shape:
        raise ValueError("Les deux images doivent avoir les mêmes dimensions.")

    # Calculate all metrics
    lpips_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lpips_values, lpips_value = calculate_lpips_multiband(image1, image2, loss_fn)

    mean_ssim_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mean_ssim = calculate_ssim_multiband(image1, image2)

    psnr_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    psnr_value = calculate_psnr(image1, image2)

    rmse_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rmse_value = calculate_rmse(image1, image2)

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    image_1_name = os.path.basename(image1_path)
    data = {
        "metrics": {
            "LPIPS": {
                "library": "scikit-image",
                "version": lib_meta.version("scikit-image"),
                "date": lpips_date,
                "results": {
                    image_1_name: lpips_value
                }
            },
            "SSIM": {
                "library": "scikit-image",
                "version": lib_meta.version("scikit-image"),
                "date": mean_ssim_date,
                "results": {
                    image_1_name: mean_ssim
                }
            },
            "PSNR": {
                "library": "scikit-image",
                "version": lib_meta.version("scikit-image"),
                "date": psnr_date,
                "results": {
                    image_1_name: str(psnr_value) if math.isinf(psnr_value) else psnr_value
                }
            },
            "RMSE": {
                "library": "scikit-image",
                "version": lib_meta.version("scikit-image"),
                "date": rmse_date,
                "results": {
                    image_1_name: rmse_value
                }
            }
        }
    }
    return data


import random
from datetime import datetime


def calculate_thematic_modular_test(product_path, base_value, multiplier) -> dict:
    """
    Fonction thématique de test qui génère des résultats basés sur un nombre de base et un multiplicateur.

    Arguments :
    product_path (str) : Le chemin du produit (non utilisé ici, mais requis pour l'interface).
    base_value (int) : Le nombre de base utilisé pour le calcul.
    multiplier (int) : Le multiplicateur utilisé pour le calcul.

    Retour :
    dict : Un dictionnaire contenant les résultats thématiques avec des valeurs calculées et statistiques.
    """

    # Date actuelle au format YYYY-MM-DD
    date_actuelle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Générer des valeurs aléatoires basées sur le nombre de base et le multiplicateur
    result = {
        f"band_name_{i + 1}": base_value * multiplier + random.randint(1, 10)
        for i in range(2)  # Exemple avec 2 bandes pour la démonstration
    }

    # Calculer l'average et la stdev des résultats
    values = list(result.values())
    average = sum(values) / len(values)
    stdev = (sum((x - average) ** 2 for x in values) / len(values)) ** 0.5

    # Créer le dictionnaire de résultats thématiques
    thematic_modular_test_1 = {
        "thematic_modular_test_1": {
            "library": None,
            "version": "0.1",
            "date": date_actuelle,
            "metrics": {
                "global": {
                    "result": result,
                    "average": average,
                    "stdev": stdev
                }
            }
        }
    }

    return thematic_modular_test_1


