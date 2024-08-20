import json
from datetime import datetime
import os.path
from typing import List, Any

import numpy as np
from COPEX_high_rate_compression_quality_metrics import metrics
from COPEX_high_rate_compression_quality_metrics import utils


def load_json_file(json_file_path: str) -> Any:
    """
    Charge le contenu d'un fichier JSON et le retourne sous forme de dictionnaire ou de liste.

    Args:
        json_file_path (str): Le chemin complet du fichier JSON à charger.

    Returns:
        Any: Le contenu du fichier JSON sous forme de dictionnaire, liste, ou autre
             structure de données Python (selon le contenu du fichier JSON).
    """
    # Vérifier si le fichier spécifié existe
    if not os.path.isfile(json_file_path):
        raise FileNotFoundError(f"Le fichier spécifié n'existe pas : {json_file_path}")

    # Charger le contenu du fichier JSON
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    return data


def list_json_files(target_folder: str) -> List[str]:
    """
    Liste tous les fichiers .json présents dans un dossier cible.

    Args:
        target_folder (str): Le chemin du dossier où chercher les fichiers .json.

    Returns:
        List[str]: Une liste des noms de fichiers .json présents dans le dossier cible.
                   La liste est vide s'il n'y a aucun fichier .json.
    """
    # Vérifier si le dossier cible existe
    if not os.path.isdir(target_folder):
        raise ValueError(f"Le dossier spécifié n'existe pas : {target_folder}")

    # Initialiser une liste pour stocker les noms de fichiers .json
    json_files = []

    # Parcourir tous les éléments du dossier cible
    for item in os.listdir(target_folder):
        # Construire le chemin complet de l'élément
        item_path = os.path.join(target_folder, item)

        # Vérifier si l'élément est un fichier et si son extension est .json
        if os.path.isfile(item_path) and item.endswith('.json'):
            # Ajouter le fichier .json à la liste
            json_files.append(item)

    return json_files


def get_folder_size(folderpath):
    """retourne le poid total d'un dossier"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folderpath):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def get_compressed_size_frome_folder_name(folderpath):
    # Fonction pour récupérer la taille compressée d'apres le nom du dossier
    return int(utils.get_bracket_content(folderpath, 1))


def calculate_compression_factor(folderpath_1, folderpath_2):
    # Fonction pour calculer la taille totale des fichiers dans un dossier

    print(f"calculating compression factor between {folderpath_1} and {folderpath_2}")
    size_1 = get_folder_size(folderpath_1)
    size_2 = int(utils.get_bracket_content(folderpath_2, 1))

    # Calcul du facteur de compression
    if size_2 != 0:
        print(f"size folder 1 = {size_2} and folder 2 ={size_2}")
        compression_factor = size_1 / size_2
        print(f"compression_factor = {compression_factor}")
    else:
        raise ValueError("La taille du dossier 2 est 0, impossible de calculer le facteur de compression.")

    return round(compression_factor, 2)


def get_most_recent_date_index(date_list: List[str]) -> int:
    """
    Retourne l'index de la date la plus récente dans une liste de dates formatées en 'YYYYMMDD_HHMMSS'.

    Args:
        date_list (List[str]): Une liste de dates sous forme de chaînes de caractères au format 'YYYYMMDD_HHMMSS'.

    Returns:
        int: L'index de la date la plus récente dans la liste.
    """
    # Conversion des chaînes de caractères en objets datetime
    date_objects = [datetime.strptime(date_str, '%Y%m%d_%H%M%S') for date_str in date_list]

    # Trouver l'index de la date la plus récente
    most_recent_index = max(range(len(date_objects)), key=lambda i: date_objects[i])

    return most_recent_index


def get_json_name_by_initialising_new_one_or_getting_already_existing(root_directory, dataset_name, test_case_number,
                                                                      nnvvppp_algoname) -> str:
    result_folder_path = utils.get_algorithm_results_full_path(root_directory, dataset_name, test_case_number,
                                                               nnvvppp_algoname)
    json_file_list = list_json_files(result_folder_path)
    dates = []

    if json_file_list:
        # Extraire les dates des noms de fichiers JSON
        for json_file_name in json_file_list:
            try:
                dates.append(utils.get_bracket_content(json_file_name, 3))
            except ValueError:
                print(f"Error extracting date from file: {json_file_name}")

        if dates:
            most_recent_index = get_most_recent_date_index(dates)
            final_json_file = json_file_list[most_recent_index]
            print(f"Dates: {dates}")
            print(f"Index of most recent date: {most_recent_index}")
            print(f"Final JSON file to use is {final_json_file}")
            return final_json_file
        else:
            print("No valid dates found in JSON file names.")
    else:
        print(f"No .json found in {result_folder_path}... ")
        final_json_file = initialize_json(root_directory, dataset_name, test_case_number, nnvvppp_algoname)
        print(f"Final JSON file to use is {final_json_file}")
        return final_json_file
    raise ValueError("no json file name could be get or created... verify input parameters.")


def get_last_json(root_directory, dataset_name, test_case_number, nnvvppp_algoname) -> str:
    result_folder_path = utils.get_algorithm_results_full_path(root_directory, dataset_name, test_case_number,
                                                               nnvvppp_algoname)
    json_file_list = list_json_files(result_folder_path)
    dates = []

    if json_file_list:
        # Extraire les dates des noms de fichiers JSON
        for json_file_name in json_file_list:
            try:
                dates.append(utils.get_bracket_content(json_file_name, 3))
            except ValueError:
                print(f"Error extracting date from file: {json_file_name}")

        if dates:
            most_recent_index = get_most_recent_date_index(dates)
            final_json_file = json_file_list[most_recent_index]
            print(f"Dates: {dates}")
            print(f"Index of most recent date: {most_recent_index}")
            print(f"Final JSON file to use is {final_json_file}")
            return final_json_file
        else:
            print("No valid dates found in JSON file names.")
    else:
        print(f"No .json found in {result_folder_path}... ")
        return None
    raise ValueError("no json file name could be get or created... verify input parameters.")


def make_generic(root_directory, dataset_name, test_case_number, nnvvppp_algoname):
    """Si le json existe , on modifie l'existant, sinon, on en creer un nouveau"""
    result_folder_path = utils.get_algorithm_results_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                               test_case_number=test_case_number,
                                                               nnvvppp_algoname=nnvvppp_algoname)

    original_folder_path = utils.get_original_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                        test_case_number=test_case_number)

    most_recent_json_file = get_last_json(root_directory,
                                          dataset_name,
                                          test_case_number,
                                          nnvvppp_algoname)
    if (most_recent_json_file):
        most_recent_json_file_full_path = os.path.join(result_folder_path, most_recent_json_file)
        json_content = load_json_file(most_recent_json_file_full_path)
    else:
        json_content = get_initialized_json(root_directory,
                                          dataset_name,
                                          test_case_number,
                                          nnvvppp_algoname)

    original_product_list = utils.get_product_name_list_from_path(original_folder_path)
    decompressed_product_path_list = []
    original_product_path_list = []
    for product_band_name in original_product_list:
        print("product_band_name = ", product_band_name)
        decompressed_product_path_list.append(os.path.join(result_folder_path, product_band_name))
        original_product_path_list.append(os.path.join(original_folder_path, product_band_name))

    print(decompressed_product_path_list)
    print(original_product_path_list)

    for i in range(len(original_product_path_list)):
        data_to_add = metrics.calculate_lrsp(original_product_path_list[i], decompressed_product_path_list[i])
        utils.add_data_to_dict(json_content, data_to_add)

    print("json_content = ", json_content)
    print("type(json_content) = ", type(json_content))

    final_json_name = make_json_filename(dataset_name, test_case_number,
                                         utils.get_nn_vv_ppp_from_full_nnvvppp_algo_name(nnvvppp_algoname),
                                         json_content.get("compression_factor", None))
    final_json_path = os.path.join(result_folder_path, final_json_name)

    utils.add_data_to_dict(json_content, metrics.calculate_metrics_statistics(json_content))

    with open(final_json_path, 'w') as json_file:
        json.dump(json_content, json_file, indent=4)

    print(f"Fichier JSON créé : {final_json_name}")


def make_json_filename(dataset_name, test_case_number, nnvvppp_algoname, compression_factor):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"[{dataset_name}]_[{test_case_number}]_[{utils.get_nn_vv_ppp_from_full_nnvvppp_algo_name(nnvvppp_algoname)}_x{str(compression_factor)}]_[{now}].json"


def initialize_json(root_directory, dataset_name, test_case_number, nnvvppp_algoname):
    """
    A partir d'un dossier source et d'un dossier de compression d'algorythme, on va
    """
    # Calculer le facteur de compression xC

    result_folder_path = utils.get_algorithm_results_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                               test_case_number=test_case_number,
                                                               nnvvppp_algoname=nnvvppp_algoname)
    original_folder_path = utils.get_original_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                        test_case_number=test_case_number)
    compression_factor = calculate_compression_factor(original_folder_path, result_folder_path)
    print(f"initializing json file for folder {result_folder_path}...")
    # Générer la date et l'heure actuelle

    # Créer le nom du fichier JSON au format [dataset_name_1]_[TTT]_[NN VV PPP_xC]_[yyyyMMdd_HHmmss].json
    json_filename = make_json_filename(dataset_name, test_case_number,
                                       utils.get_nn_vv_ppp_from_full_nnvvppp_algo_name(nnvvppp_algoname),
                                       compression_factor)

    # Initialiser la structure JSON de base
    json_data = {
        "original_size": get_folder_size(original_folder_path),
        "compressed_size": get_compressed_size_frome_folder_name(result_folder_path),
        "compression_factor": compression_factor,
        "compression_algorithm": nnvvppp_algoname,
        "algorithm_version": nnvvppp_algoname[2:4],
        "compression_parameter": nnvvppp_algoname[4:6],

        # D'autres sections peuvent être ajoutées ici si nécessaire
    }
    output_path_plus_filename = os.path.join(result_folder_path, json_filename)
    # Sauvegarder le fichier JSON
    with open(output_path_plus_filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    print(f"Fichier JSON créé : {json_filename}")
    return json_filename


def get_initialized_json(root_directory, dataset_name, test_case_number, nnvvppp_algoname):
    """
    A partir d'un dossier source et d'un dossier de compression d'algorythme, on va
    """
    # Calculer le facteur de compression xC

    result_folder_path = utils.get_algorithm_results_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                               test_case_number=test_case_number,
                                                               nnvvppp_algoname=nnvvppp_algoname)
    original_folder_path = utils.get_original_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                        test_case_number=test_case_number)
    compression_factor = calculate_compression_factor(original_folder_path, result_folder_path)
    print(f"initializing json file for folder {result_folder_path}...")
    # Générer la date et l'heure actuelle

    # Créer le nom du fichier JSON au format [dataset_name_1]_[TTT]_[NN VV PPP_xC]_[yyyyMMdd_HHmmss].json
    json_filename = make_json_filename(dataset_name, test_case_number,
                                       utils.get_nn_vv_ppp_from_full_nnvvppp_algo_name(nnvvppp_algoname),
                                       compression_factor)

    # Initialiser la structure JSON de base
    json_data = {
        "original_size": get_folder_size(original_folder_path),
        "compressed_size": get_compressed_size_frome_folder_name(result_folder_path),
        "compression_factor": compression_factor,
        "compression_algorithm": nnvvppp_algoname,
        "algorithm_version": nnvvppp_algoname[2:4],
        "compression_parameter": nnvvppp_algoname[4:6],

        # D'autres sections peuvent être ajoutées ici si nécessaire
    }

    return json_data
