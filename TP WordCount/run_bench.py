"""
Script d'exécution des benchmarks
"""

import os
import sys
import csv
import time
import statistics
from datetime import datetime
import subprocess

def get_system_info():
    """Récupère les informations système"""
    import platform
    import psutil
    
    info = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Système": platform.system(),
        "Version": platform.version(),
        "Processeur": platform.processor(),
        "CPU Cores (physiques)": psutil.cpu_count(logical=False),
        "CPU Cores (logiques)": psutil.cpu_count(logical=True),
        "RAM totale (Go)": round(psutil.virtual_memory().total / (1024**3), 2),
        "Python version": platform.python_version()
    }
    
    return info

def run_wordcount(file_path, repetitions=5):
    """
    Exécute le comptage de mots plusieurs fois
    
    Args:
        file_path: Chemin vers le fichier
        repetitions: Nombre de répétitions
    
    Returns:
        list: Temps d'exécution pour chaque répétition
    """
    times = []
    
    for i in range(repetitions):
        print(f"  Exécution {i+1}/{repetitions}...", end='', flush=True)
        
        start_time = time.time()
        
        result = subprocess.run(
            [sys.executable, "word_count.py", file_path],
            capture_output=True,
            text=True
        )
        
        end_time = time.time()
        exec_time = end_time - start_time
        times.append(exec_time)
        
        print(f" {exec_time:.3f}s")
    
    return times

def benchmark_all_files(data_dir="data", repetitions=5):
    """
    Exécute le benchmark sur tous les fichiers du dossier
    
    Returns:
        list: Résultats du benchmark
    """
    files = []
    for f in os.listdir(data_dir):
        if f.startswith("corpus_") and f.endswith(".txt"):
            files.append(f)
    
    files.sort(key=lambda x: int(x.split('_')[1].replace('MB.txt', '')))
    
    results = []
    
    print("Lancement des benchmarks WordCount")
    print("=" * 60)
    
    for file_name in files:
        file_path = os.path.join(data_dir, file_name)
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        
        print(f"\nFichier: {file_name}")
        print(f"Taille: {file_size:.1f} MB")
        print("-" * 30)
        
        exec_times = run_wordcount(file_path, repetitions)
        
        stats = {
            "fichier": file_name,
            "taille_mb": round(file_size, 2),
            "taille_bytes": os.path.getsize(file_path),
            "repetitions": repetitions,
            "temps_min": min(exec_times),
            "temps_max": max(exec_times),
            "temps_moyen": statistics.mean(exec_times),
            "temps_median": statistics.median(exec_times),
            "ecart_type": statistics.stdev(exec_times) if len(exec_times) > 1 else 0,
            "temps_total": sum(exec_times),
            "temps_details": exec_times
        }
        
        results.append(stats)
        
        print(f"\nRésumé pour {file_name}:")
        print(f"  Moyenne: {stats['temps_moyen']:.3f}s")
        print(f"  Min: {stats['temps_min']:.3f}s")
        print(f"  Max: {stats['temps_max']:.3f}s")
        print(f"  Écart-type: {stats['ecart_type']:.3f}s")
    
    return results

def save_results_to_csv(results, system_info, output_file="results/benchmark_results.csv"):
    """Sauvegarde les résultats en CSV"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'fichier', 'taille_mb', 'taille_bytes', 'repetitions',
            'temps_min', 'temps_max', 'temps_moyen', 'temps_median',
            'ecart_type', 'temps_total'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in results:
            row = {k: v for k, v in result.items() if k != 'temps_details'}
            writer.writerow(row)
    
    print(f"\nRésultats sauvegardés dans: {output_file}")
    
    info_file = "results/system_info.txt"
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write("INFORMATIONS SYSTÈME\n")
        f.write("=" * 40 + "\n\n")
        for key, value in system_info.items():
            f.write(f"{key}: {value}\n")
    
    print(f"Informations système sauvegardées dans: {info_file}")

def main():
    """Fonction principale"""
    print("BENCHMARK - Comptage de mots séquentiel")
    print("=" * 60)
    
    if not os.path.exists("data"):
        print("Erreur: Le dossier 'data/' n'existe pas.")
        print("Exécute d'abord: python gen_corpus.py")
        sys.exit(1)
    
    system_info = get_system_info()
    
    print("\n" + "=" * 40)
    print("INFORMATIONS SYSTÈME")
    print("=" * 40)
    for key, value in system_info.items():
        if key != "Date":
            print(f"{key}: {value}")
    print("=" * 40 + "\n")
    
    results = benchmark_all_files(repetitions=5)
    
    save_results_to_csv(results, system_info)
    
    print("\n" + "=" * 60)
    print("BENCHMARK TERMINÉ AVEC SUCCÈS")
    print("=" * 60)
    
    print("\nRÉSUMÉ DES RÉSULTATS:")
    print("-" * 60)
    print(f"{'Taille (MB)':<10} {'Temps moyen (s)':<15} {'Speedup':<10}")
    print("-" * 60)
    
    base_time = results[0]['temps_moyen'] if results else 0
    for result in results:
        speedup = result['temps_moyen'] / base_time if base_time > 0 else 1
        print(f"{result['taille_mb']:<10.1f} {result['temps_moyen']:<15.3f} {speedup:<10.2f}x")

if __name__ == "__main__":
    main()