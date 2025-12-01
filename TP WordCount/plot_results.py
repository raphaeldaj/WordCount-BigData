import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def load_results(csv_file="results/benchmark_results.csv"):
    """Charge les résultats depuis le CSV"""
    if not os.path.exists(csv_file):
        print(f"Erreur: Fichier {csv_file} non trouvé")
        print("Exécute d'abord: python run_bench.py")
        sys.exit(1)
    
    return pd.read_csv(csv_file)

def plot_execution_time_only(df):
    """Trace uniquement le temps d'exécution en fonction de la taille"""
    plt.figure(figsize=(10, 6))
    
    plt.plot(df['taille_mb'], df['temps_moyen'], 'bo-', 
             linewidth=2.5, markersize=10, markerfacecolor='white', 
             markeredgewidth=2, markeredgecolor='blue',
             label='Temps moyen d\'exécution')
    
    for i, row in df.iterrows():
        plt.vlines(row['taille_mb'], row['temps_min'], row['temps_max'], 
                  colors='red', alpha=0.5, linewidth=2, zorder=1)
        plt.plot(row['taille_mb'], row['temps_min'], 'v', color='red', markersize=6, alpha=0.7, zorder=2)
        plt.plot(row['taille_mb'], row['temps_max'], '^', color='red', markersize=6, alpha=0.7, zorder=2)
    
    plt.title('Évolution du temps d\'exécution du Word Count\nen fonction de la taille du fichier', 
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Taille du fichier (MB)', fontsize=12)
    plt.ylabel('Temps d\'exécution (secondes)', fontsize=12)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    for i, row in df.iterrows():
        plt.text(row['taille_mb'], row['temps_moyen'] + 0.02 * max(df['temps_moyen']),
                f"{row['temps_moyen']:.2f}s", 
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.legend(loc='upper left', fontsize=11, framealpha=0.9)
    
    y_min = min(df['temps_min']) * 0.8
    y_max = max(df['temps_max']) * 1.1
    plt.ylim(y_min, y_max)
    
    plt.xticks(df['taille_mb'])
    plt.tight_layout()
    
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/execution_time_graph.png', dpi=300, bbox_inches='tight')
    plt.savefig('results/execution_time_graph.pdf', bbox_inches='tight')
    plt.show()
    
    print("\n" + "="*70)
    print("RÉSUMÉ DES TEMPS D'EXÉCUTION")
    print("="*70)
    for _, row in df.iterrows():
        print(f"{row['fichier']} ({row['taille_mb']} MB):")
        print(f"  Temps moyen: {row['temps_moyen']:.3f} s")
        print(f"  Variation: {row['temps_min']:.3f} - {row['temps_max']:.3f} s")
        print(f"  Temps par MB: {row['temps_moyen']/row['taille_mb']:.4f} s/MB")
        print()

def main():
    """Fonction principale simplifiée"""
    print("GRAPHIQUE TEMPS D'EXÉCUTION vs TAILLE")
    print("=" * 50)
    
    df = load_results()
    
    plot_execution_time_only(df)
    
    print("Graphique sauvegardé dans 'results/execution_time_graph.png'")

if __name__ == "__main__":
    main()