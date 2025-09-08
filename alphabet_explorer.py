import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Pour afficher les images (pip install Pillow)
import pygame  # Pour jouer les sons (pip install pygame)
import os

class AlphabetExplorer:
    def __init__(self):
        # Créer la fenêtre principale
        self.root = tk.Tk()
        self.root.title("Alphabet Explorer")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f8ff")
        
        # Initialiser pygame pour les sons
        try:
            pygame.mixer.init()
            self.audio_enabled = True
        except:
            self.audio_enabled = False
            print("Audio non disponible - pygame non installé")
        
        # Chemins vers les dossiers des ressources
        self.images_path = "images"  # Dossier pour les images
        self.audio_path = "audio"    # Dossier pour les fichiers audio
        
        # Créer les dossiers s'ils n'existent pas
        self.create_folders()
        
        # Données des alphabets
        self.alphabets = {
            "Français": {
                "letters": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                "examples": {
                    "A": "Avion", "B": "Ballon", "C": "Chat", "D": "Dragon",
                    "E": "Éléphant", "F": "Fleur", "G": "Girafe", "H": "Hélicoptère",
                    "I": "Igloo", "J": "Jardin", "K": "Kangourou", "L": "Lion",
                    "M": "Maison", "N": "Nuage", "O": "Oiseau", "P": "Papillon",
                    "Q": "Queue", "R": "Robot", "S": "Soleil", "T": "Train",
                    "U": "Univers", "V": "Voiture", "W": "Wagon", "X": "Xylophone",
                    "Y": "Yacht", "Z": "Zèbre"
                },
                "folder": "fr"
            },
            "English": {
                "letters": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                "examples": {
                    "A": "Apple", "B": "Ball", "C": "Cat", "D": "Dog",
                    "E": "Elephant", "F": "Fish", "G": "Giraffe", "H": "House",
                    "I": "Ice", "J": "Juice", "K": "Kite", "L": "Lion",
                    "M": "Moon", "N": "Nest", "O": "Orange", "P": "Penguin",
                    "Q": "Queen", "R": "Rainbow", "S": "Sun", "T": "Tree",
                    "U": "Umbrella", "V": "Violin", "W": "Water", "X": "X-ray",
                    "Y": "Yellow", "Z": "Zebra"
                },
                "folder": "en"
            },
            "العربية": {
                "letters": ["ا", "ب", "ت", "ث", "ج", "ح", "خ", "د", "ذ", "ر", "ز", "س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ك", "ل", "م", "ن", "ه", "و", "ي"],
                "examples": {
                    "ا": "أسد", "ب": "بطة", "ت": "تفاح", "ث": "ثعلب", "ج": "جمل", 
                    "ح": "حصان", "خ": "خروف", "د": "دب", "ذ": "ذئب", "ر": "رز",
                    "ز": "زرافة", "س": "سمك", "ش": "شمس", "ص": "صقر", "ض": "ضفدع",
                    "ط": "طائر", "ظ": "ظبي", "ع": "عصفور", "غ": "غزال", "ف": "فيل",
                    "ق": "قط", "ك": "كلب", "ل": "ليمون", "م": "ماء", "ن": "نحلة",
                    "ه": "هدهد", "و": "وردة", "ي": "يد"
                },
                "folder": "ar"
            }
        }
        
        # Variables d'état
        self.current_language = "Français"
        self.current_letter_index = 0
        self.current_image = None
        
        self.create_interface()
        
    def create_folders(self):
        """Crée les dossiers nécessaires pour les ressources"""
        # Créer le dossier principal pour les images
        if not os.path.exists(self.images_path):
            os.makedirs(self.images_path)
            
        # Créer le dossier principal pour les audios
        if not os.path.exists(self.audio_path):
            os.makedirs(self.audio_path)
            
        # Créer les sous-dossiers pour chaque langue
        for lang_data in self.alphabets.values():
            lang_folder = lang_data["folder"]
            
            # Dossiers pour images
            img_lang_path = os.path.join(self.images_path, lang_folder)
            if not os.path.exists(img_lang_path):
                os.makedirs(img_lang_path)
                
            # Dossiers pour audio
            audio_lang_path = os.path.join(self.audio_path, lang_folder)
            if not os.path.exists(audio_lang_path):
                os.makedirs(audio_lang_path)
                
        print("✅ Dossiers créés !")
        print("📁 Structure des dossiers :")
        print("   images/")
        print("   ├── fr/  (pour images françaises)")
        print("   ├── en/  (pour images anglaises)")
        print("   └── ar/  (pour images arabes)")
        print("   audio/")
        print("   ├── fr/  (pour sons français)")
        print("   ├── en/  (pour sons anglais)")
        print("   └── ar/  (pour sons arabes)")
        
    def create_interface(self):
        # Titre principal
        title = tk.Label(
            self.root, 
            text="🔤 Alphabet Explorer", 
            font=("Arial", 24, "bold"),
            bg="#f0f8ff", 
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Sélecteur de langue
        language_frame = tk.Frame(self.root, bg="#f0f8ff")
        language_frame.pack(pady=10)
        
        tk.Label(language_frame, text="Langue:", font=("Arial", 12), bg="#f0f8ff").pack(side=tk.LEFT)
        
        self.language_var = tk.StringVar(value=self.current_language)
        language_combo = ttk.Combobox(
            language_frame, 
            textvariable=self.language_var,
            values=list(self.alphabets.keys()),
            state="readonly",
            font=("Arial", 12)
        )
        language_combo.pack(side=tk.LEFT, padx=10)
        language_combo.bind("<<ComboboxSelected>>", self.change_language)
        
        # Zone principale d'affichage
        self.main_frame = tk.Frame(self.root, bg="white", relief="raised", bd=2)
        self.main_frame.pack(pady=20, padx=50, fill="both", expand=True)
        
        # Frame pour la lettre et l'image
        content_frame = tk.Frame(self.main_frame, bg="white")
        content_frame.pack(pady=20, fill="both", expand=True)
        
        # Côté gauche : Lettre et mot
        left_frame = tk.Frame(content_frame, bg="white")
        left_frame.pack(side=tk.LEFT, padx=20, fill="both", expand=True)
        
        # Affichage de la lettre actuelle
        self.letter_label = tk.Label(
            left_frame,
            text="A",
            font=("Arial", 72, "bold"),
            bg="white",
            fg="#e74c3c"
        )
        self.letter_label.pack(pady=20)
        
        # Affichage du mot d'exemple
        self.word_label = tk.Label(
            left_frame,
            text="Avion",
            font=("Arial", 24),
            bg="white",
            fg="#2c3e50"
        )
        self.word_label.pack(pady=10)
        
        # Boutons audio
        audio_frame = tk.Frame(left_frame, bg="white")
        audio_frame.pack(pady=20)
        
        self.speak_letter_btn = tk.Button(
            audio_frame,
            text="🔊 Lettre",
            font=("Arial", 12),
            bg="#3498db",
            fg="white",
            command=self.play_letter_sound,
            relief="raised",
            bd=2
        )
        self.speak_letter_btn.pack(side=tk.TOP, pady=5)
        
        self.speak_word_btn = tk.Button(
            audio_frame,
            text="🔊 Mot",
            font=("Arial", 12),
            bg="#2ecc71",
            fg="white",
            command=self.play_word_sound,
            relief="raised",
            bd=2
        )
        self.speak_word_btn.pack(side=tk.TOP, pady=5)
        
        # Côté droit : Image
        right_frame = tk.Frame(content_frame, bg="white")
        right_frame.pack(side=tk.RIGHT, padx=20, fill="both", expand=True)
        
        # Label pour l'image
        self.image_label = tk.Label(
            right_frame,
            text="📷\n\nImage non trouvée",
            font=("Arial", 16),
            bg="#ecf0f1",
            fg="#7f8c8d",
            relief="sunken",
            bd=2,
            width=20,
            height=10
        )
        self.image_label.pack(pady=20, fill="both", expand=True)
        
        # Instructions pour ajouter des images
        self.instruction_label = tk.Label(
            right_frame,
            text="💡 Ajoutez vos images dans le dossier approprié",
            font=("Arial", 10),
            bg="white",
            fg="#95a5a6",
            wraplength=200
        )
        self.instruction_label.pack(pady=5)
        
        # Boutons de navigation
        nav_frame = tk.Frame(self.root, bg="#f0f8ff")
        nav_frame.pack(pady=20)
        
        self.prev_btn = tk.Button(
            nav_frame,
            text="⬅ Précédent",
            font=("Arial", 14),
            bg="#95a5a6",
            fg="white",
            command=self.previous_letter,
            relief="raised",
            bd=2
        )
        self.prev_btn.pack(side=tk.LEFT, padx=20)
        
        # Indicateur de position
        self.position_label = tk.Label(
            nav_frame,
            text="1/26",
            font=("Arial", 12),
            bg="#f0f8ff",
            fg="#2c3e50"
        )
        self.position_label.pack(side=tk.LEFT, padx=20)
        
        self.next_btn = tk.Button(
            nav_frame,
            text="Suivant ➡",
            font=("Arial", 14),
            bg="#95a5a6",
            fg="white",
            command=self.next_letter,
            relief="raised",
            bd=2
        )
        self.next_btn.pack(side=tk.LEFT, padx=20)
        
        # Grille des lettres
        self.create_alphabet_grid()
        
        # Mettre à jour l'affichage initial
        self.update_display()
    
    def create_alphabet_grid(self):
        """Crée une grille cliquable avec toutes les lettres"""
        grid_frame = tk.Frame(self.root, bg="#f0f8ff")
        grid_frame.pack(pady=10)
        
        tk.Label(grid_frame, text="Cliquez sur une lettre:", font=("Arial", 10), bg="#f0f8ff").pack()
        
        letters_frame = tk.Frame(grid_frame, bg="#f0f8ff")
        letters_frame.pack(pady=5)
        
        self.letter_buttons = []
        
        # Créer 30 boutons (pour supporter l'arabe qui a 28 lettres)
        for i in range(30):
            row = i // 6
            col = i % 6
            
            btn = tk.Button(
                letters_frame,
                text="",
                font=("Arial", 10, "bold"),
                width=4,
                height=1,
                command=lambda idx=i: self.select_letter_by_index(idx),
                relief="raised",
                bd=1
            )
            btn.grid(row=row, col=col, padx=2, pady=2)
            self.letter_buttons.append(btn)
    
    def select_letter_by_index(self, index):
        """Sélectionne une lettre par son index"""
        letters = self.alphabets[self.current_language]["letters"]
        if index < len(letters):
            self.current_letter_index = index
            self.update_display()
    
    def change_language(self, event=None):
        """Change la langue d'apprentissage"""
        self.current_language = self.language_var.get()
        self.current_letter_index = 0
        self.update_display()
        self.update_grid_buttons()
    
    def load_image(self, letter):
        """Charge l'image pour une lettre donnée"""
        lang_folder = self.alphabets[self.current_language]["folder"]
        word = self.alphabets[self.current_language]["examples"][letter]
        
        # Chercher plusieurs formats d'image possibles
        image_formats = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        image_names = [
            f"{letter.lower()}",  # a.png
            f"{word.lower()}",    # avion.png
            f"{letter.upper()}",  # A.png
            f"{word}"             # Avion.png
        ]
        
        for name in image_names:
            for ext in image_formats:
                image_path = os.path.join(self.images_path, lang_folder, f"{name}{ext}")
                if os.path.exists(image_path):
                    try:
                        # Charger et redimensionner l'image
                        pil_image = Image.open(image_path)
                        pil_image = pil_image.resize((200, 200), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(pil_image)
                        return photo
                    except Exception as e:
                        print(f"Erreur lors du chargement de {image_path}: {e}")
                        continue
        
        return None
    
    def play_sound(self, sound_path):
        """Joue un fichier audio"""
        if not self.audio_enabled:
            print(f"Audio non disponible. Fichier: {sound_path}")
            return
            
        if os.path.exists(sound_path):
            try:
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
                print(f"🔊 Lecture de: {sound_path}")
            except Exception as e:
                print(f"Erreur lors de la lecture de {sound_path}: {e}")
        else:
            print(f"❌ Fichier audio non trouvé: {sound_path}")
    
    def play_letter_sound(self):
        """Joue le son de la lettre"""
        letters = self.alphabets[self.current_language]["letters"]
        current_letter = letters[self.current_letter_index]
        lang_folder = self.alphabets[self.current_language]["folder"]
        
        # Formats de fichiers audio supportés
        audio_formats = ['.mp3', '.wav', '.ogg']
        
        for ext in audio_formats:
            sound_path = os.path.join(self.audio_path, lang_folder, f"letter_{current_letter.lower()}{ext}")
            if os.path.exists(sound_path):
                self.play_sound(sound_path)
                return
                
        print(f"📢 Prononcer: {current_letter}")
    
    def play_word_sound(self):
        """Joue le son du mot"""
        letters = self.alphabets[self.current_language]["letters"]
        current_letter = letters[self.current_letter_index]
        current_word = self.alphabets[self.current_language]["examples"][current_letter]
        lang_folder = self.alphabets[self.current_language]["folder"]
        
        # Formats de fichiers audio supportés
        audio_formats = ['.mp3', '.wav', '.ogg']
        
        for ext in audio_formats:
            sound_path = os.path.join(self.audio_path, lang_folder, f"word_{current_word.lower()}{ext}")
            if os.path.exists(sound_path):
                self.play_sound(sound_path)
                return
                
        print(f"📢 Prononcer: {current_word}")
    
    def update_display(self):
        """Met à jour l'affichage principal"""
        letters = self.alphabets[self.current_language]["letters"]
        current_letter = letters[self.current_letter_index]
        current_word = self.alphabets[self.current_language]["examples"][current_letter]
        
        # Mettre à jour les labels
        self.letter_label.config(text=current_letter)
        self.word_label.config(text=current_word)
        
        # Charger et afficher l'image
        photo = self.load_image(current_letter)
        if photo:
            self.current_image = photo  # Garder une référence
            self.image_label.config(image=photo, text="")
            lang_folder = self.alphabets[self.current_language]["folder"]
            self.instruction_label.config(text=f"📁 Image trouvée dans images/{lang_folder}/")
        else:
            self.image_label.config(image="", text=f"📷\n\nImage pour '{current_word}'\nnon trouvée")
            lang_folder = self.alphabets[self.current_language]["folder"]
            self.instruction_label.config(
                text=f"💡 Ajoutez: {current_letter.lower()}.png ou {current_word.lower()}.png\ndans images/{lang_folder}/"
            )
        
        # Mettre à jour l'indicateur de position
        self.position_label.config(text=f"{self.current_letter_index + 1}/{len(letters)}")
        
        # Mettre à jour les boutons de navigation
        self.prev_btn.config(state="normal" if self.current_letter_index > 0 else "disabled")
        self.next_btn.config(state="normal" if self.current_letter_index < len(letters) - 1 else "disabled")
        
        # Mettre à jour la grille
        self.update_grid_buttons()
    
    def update_grid_buttons(self):
        """Met à jour la couleur des boutons dans la grille"""
        letters = self.alphabets[self.current_language]["letters"]
        
        for i, btn in enumerate(self.letter_buttons):
            if i < len(letters):
                btn.config(text=letters[i], state="normal")
                if i == self.current_letter_index:
                    btn.config(bg="#e74c3c", fg="white")
                else:
                    btn.config(bg="SystemButtonFace", fg="black")
            else:
                btn.config(text="", state="disabled", bg="SystemButtonFace")
    
    def previous_letter(self):
        """Aller à la lettre précédente"""
        if self.current_letter_index > 0:
            self.current_letter_index -= 1
            self.update_display()
    
    def next_letter(self):
        """Aller à la lettre suivante"""
        letters = self.alphabets[self.current_language]["letters"]
        if self.current_letter_index < len(letters) - 1:
            self.current_letter_index += 1
            self.update_display()
    
    def run(self):
        """Lancer l'application"""
        self.root.mainloop()

# Point d'entrée principal
if __name__ == "__main__":
    print("🚀 Lancement d'Alphabet Explorer...")
    print("\n📋 Instructions pour utiliser toutes les fonctionnalités :")
    print("\n🖼️  IMAGES :")
    print("   - Placez vos images dans les dossiers créés automatiquement")
    print("   - Formats supportés: .png, .jpg, .jpeg, .gif, .bmp")
    print("   - Noms possibles: a.png, avion.png, A.png, ou Avion.png")
    print("\n🔊 AUDIO :")
    print("   - Placez vos fichiers audio dans les dossiers audio/")
    print("   - Formats supportés: .mp3, .wav, .ogg")
    print("   - Noms: letter_a.mp3 (pour la lettre) ou word_avion.mp3 (pour le mot)")
    print("\n📦 Bibliothèques nécessaires :")
    print("   pip install Pillow pygame")
    print("\n" + "="*60)
    
    app = AlphabetExplorer()
    app.run()
