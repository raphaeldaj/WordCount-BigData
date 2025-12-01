import os
import random
import string
import argparse
import time

def generate_text_file(size_mb, output_path, vocab_size=5000):
    """
    Génère un fichier texte de taille spécifiée
    
    Args:
        size_mb: Taille du fichier en Mo
        output_path: Chemin de sortie
        vocab_size: Taille du vocabulaire (mots uniques)
    """
    if size_mb >= 1024:  
        vocab_size = min(50000, 5000 * (size_mb // 1024 + 1))
    
    print(f"Création du vocabulaire de {vocab_size} mots...")
    vocabulary = []
    for _ in range(vocab_size):
        word_length = random.randint(2, 10)
        word = ''.join(random.choices(string.ascii_lowercase, k=word_length))
        vocabulary.append(word)
    
    print("Calcul de la distribution des mots...")
    ranks = range(1, vocab_size + 1)
    zipf_weights = [1.0 / (r ** 1.07) for r in ranks]
    total_weight = sum(zipf_weights)
    normalized_weights = [w / total_weight for w in zipf_weights]
    
    avg_word_length = 5
    chars_needed = int(size_mb * 1024 * 1024)
    words_needed = chars_needed // avg_word_length
    
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    if size_mb >= 1024:
        size_display = f"{size_mb/1024:.1f} GB"
    else:
        size_display = f"{size_mb} MB"
    
    print(f"Génération d'un fichier de {size_display}...")
    print(f"Vocabulaire: {vocab_size} mots uniques")
    print(f"Nombre de mots estimé: {words_needed:,}")
    
    words_written = 0
    start_time = time.time()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        buffer = []
        buffer_size = 0
        
        while f.tell() < chars_needed:
            word = random.choices(vocabulary, weights=normalized_weights)[0]
            
            if random.random() < 0.1:
                punctuation = random.choice([',', '.', ';', '!', '?'])
                f.write(word + punctuation + ' ')
            else:
                f.write(word + ' ')
            
            words_written += 1
            
            if words_written % random.randint(10, 15) == 0:
                f.write('\n')
            
            if words_written % 50000 == 0:
                mb_written = f.tell() / (1024 * 1024)
                percent = (mb_written / size_mb) * 100
                elapsed = time.time() - start_time
                
                if elapsed > 0:
                    speed = mb_written / elapsed
                    eta = (size_mb - mb_written) / speed if speed > 0 else 0
                    
                    if size_mb >= 1024:
                        gb_written = mb_written / 1024
                        total_gb = size_mb / 1024
                        print(f"Progression: {gb_written:.2f} GB / {total_gb:.1f} GB ({percent:.1f}%) - "
                              f"Vitesse: {speed:.1f} MB/s - ETA: {eta/60:.1f} min", end='\r')
                    else:
                        print(f"Progression: {mb_written:.1f} MB / {size_mb} MB ({percent:.1f}%) - "
                              f"Vitesse: {speed:.1f} MB/s - ETA: {eta:.0f}s", end='\r')
    
    end_time = time.time()
    total_time = end_time - start_time
    
    actual_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    
    print(f"\n{'='*50}")
    print("FICHIER GÉNÉRÉ AVEC SUCCÈS")
    print('='*50)
    print(f"Chemin: {output_path}")
    
    if size_mb >= 1024:
        actual_size_gb = actual_size_mb / 1024
        print(f"Taille cible: {size_mb/1024:.1f} GB")
        print(f"Taille réelle: {actual_size_gb:.3f} GB ({actual_size_mb:.1f} MB)")
    else:
        print(f"Taille cible: {size_mb} MB")
        print(f"Taille réelle: {actual_size_mb:.2f} MB")
    
    print(f"Mots écrits: {words_written:,}")
    print(f"Temps total: {total_time:.1f} secondes")
    if total_time > 0:
        print(f"Vitesse: {actual_size_mb/total_time:.1f} MB/s")
    print('='*50)

def parse_size_input(size_str):
    """
    Parse une chaîne de taille (ex: "1GB", "500MB", "2.5GB")
    
    Returns:
        int: Taille en MB
    """
    size_str = size_str.upper().strip()
    
    if size_str.endswith('GB'):
        try:
            gb_value = float(size_str[:-2].strip())
            return int(gb_value * 1024)
        except ValueError:
            raise ValueError(f"Taille invalide: {size_str}")
    
    elif size_str.endswith('MB'):
        try:
            mb_value = float(size_str[:-2].strip())
            return int(mb_value)
        except ValueError:
            raise ValueError(f"Taille invalide: {size_str}")
    
    else:

        try:
            return int(size_str)
        except ValueError:
            raise ValueError(f"Taille invalide: {size_str}. Utilisez 'MB' ou 'GB' (ex: 1GB, 500MB)")

def main():
    parser = argparse.ArgumentParser(
        description="Générateur de fichiers texte pour benchmarks WordCount",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  # Générer un fichier de 1GB
  python gen_corpus.py --size 1GB
  
  # Générer un fichier de 500MB
  python gen_corpus.py --size 500MB
  
  # Générer un fichier de 2.5GB
  python gen_corpus.py --size 2.5GB
  
  # Générer un fichier de 100MB
  python gen_corpus.py --size 100
  
  # Générer plusieurs fichiers (comportement original)
  python gen_corpus.py --sizes 1 5 10 20 50
  
  # Générer avec nom personnalisé
  python gen_corpus.py --size 1GB --name mon_fichier
        """
    )
    
    parser.add_argument('--size', type=str,
                       help='Taille d\'un seul fichier (ex: "1GB", "500MB", "100")')
    
    parser.add_argument('--sizes', type=int, nargs='+', 
                       default=[1, 5, 10, 20, 50],
                       help='Tailles des fichiers en MB (défaut: 1 5 10 20 50)')
    
    parser.add_argument('--output-dir', type=str, default='data',
                       help='Dossier de sortie (défaut: data)')
    parser.add_argument('--name', type=str,
                       help='Nom personnalisé du fichier (sans extension)')
    
    args = parser.parse_args()
    
    print("Générateur de corpus pour le benchmark WordCount")
    print("=" * 50)
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    if args.size:
        try:

            size_mb = parse_size_input(args.size)
            
            if args.name:
                filename = f"{args.name}.txt"
            else:
                if size_mb >= 1024:
                    gb_size = size_mb / 1024
                    if gb_size.is_integer():
                        filename = f"corpus_{int(gb_size)}GB.txt"
                    else:
                        filename = f"corpus_{gb_size}GB.txt".replace('.', '_')
                else:
                    filename = f"corpus_{size_mb}MB.txt"
            
            output_path = os.path.join(args.output_dir, filename)
            
            if os.path.exists(output_path):
                existing_size = os.path.getsize(output_path) / (1024 * 1024)
                print(f"⚠️  Le fichier existe déjà: {output_path}")
                print(f"   Taille actuelle: {existing_size:.1f} MB")
                response = input("   Voulez-vous le regénérer? (o/n): ")
                if response.lower() != 'o':
                    print("Annulation.")
                    return
            
            generate_text_file(size_mb, output_path)
            
        except ValueError as e:
            print(f"Erreur: {e}")
            print("Utilisez des formats comme: '1GB', '500MB', '2.5GB', '100'")
            return
    
    else:
        print(f"Génération de {len(args.sizes)} fichiers...")
        for size in args.sizes:
            output_path = os.path.join(args.output_dir, f"corpus_{size}MB.txt")
            
            if os.path.exists(output_path):
                existing_size = os.path.getsize(output_path) / (1024 * 1024)
                print(f"\n⚠️  Le fichier existe déjà: corpus_{size}MB.txt")
                print(f"   Taille actuelle: {existing_size:.1f} MB")
                response = input("   Voulez-vous le regénérer? (o/n): ")
                if response.lower() != 'o':
                    print("   Fichier conservé.")
                    print("-" * 30)
                    continue
            
            generate_text_file(size, output_path)
            print("-" * 30)
    
    print("\n✅ Génération terminée!")

if __name__ == "__main__":
    main()