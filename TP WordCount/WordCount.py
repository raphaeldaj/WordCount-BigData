"""
Programme de comptage de mots séquentiel
Auteur : [Ton Nom]
Date : [Date]
"""

import re
import sys
import time
from collections import defaultdict

def clean_word(word):
    """Nettoie un mot : minuscules et suppression de la ponctuation"""
    word = word.lower()
    word = re.sub(r'[^\w\s]', '', word)
    return word.strip()

def word_count_sequential(file_path):
    """
    Compte les mots dans un fichier de manière séquentielle
    
    Args:
        file_path: Chemin vers le fichier texte
    
    Returns:
        dict: Dictionnaire {mot: fréquence}
        int: Nombre total de mots
        float: Temps d'exécution en secondes
    """
    word_freq = defaultdict(int)
    total_words = 0
    
    start_time = time.time()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                words = line.split()
                for word in words:
                    cleaned_word = clean_word(word)
                    if cleaned_word:
                        word_freq[cleaned_word] += 1
                        total_words += 1
    
    except FileNotFoundError:
        print(f"Erreur: Fichier {file_path} non trouvé")
        return {}, 0, 0
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return dict(word_freq), total_words, execution_time

def print_top_words(word_freq, n=10):
    """Affiche les n mots les plus fréquents"""
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    print(f"\nTop {n} mots les plus fréquents:")
    print("-" * 30)
    for word, freq in sorted_words[:n]:
        print(f"{word:20} : {freq:6}")

def main():
    """Fonction principale"""
    if len(sys.argv) != 2:
        print("Usage: python word_count.py <fichier_texte>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print(f"Analyse du fichier: {file_path}")
    print("=" * 50)
    
    word_freq, total_words, exec_time = word_count_sequential(file_path)
    
    print(f"Temps d'exécution: {exec_time:.4f} secondes")
    print(f"Nombre total de mots: {total_words:,}")
    print(f"Nombre de mots uniques: {len(word_freq):,}")
    
    print_top_words(word_freq)
    
    save_results(word_freq, total_words, exec_time, file_path)

def save_results(word_freq, total_words, exec_time, file_path):
    """Sauvegarde les résultats dans un fichier"""
    import os
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    
    output_file = os.path.join(results_dir, f"wordcount_{os.path.basename(file_path)}.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Fichier analysé: {file_path}\n")
        f.write(f"Temps d'exécution: {exec_time:.4f} secondes\n")
        f.write(f"Nombre total de mots: {total_words}\n")
        f.write(f"Nombre de mots uniques: {len(word_freq)}\n\n")
        
        f.write("Top 20 mots les plus fréquents:\n")
        f.write("-" * 40 + "\n")
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        for word, freq in sorted_words[:20]:
            f.write(f"{word:20} : {freq:6}\n")
    
    print(f"\nRésultats détaillés sauvegardés dans: {output_file}")

if __name__ == "__main__":
    main()