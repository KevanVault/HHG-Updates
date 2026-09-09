import pygame
import sys
import threading
import requests
import hashlib
import os

# Configuración básica
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
VERSION_LOCAL = "1.3"

class Button:
    def __init__(self, text, x, y, width, height, color, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.callback = callback
        self.font = pygame.font.SysFont("Arial", 20)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2, 
                                 self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

class Launcher:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Holo Hunger Games Launcher")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        self.status = "Verificando conexión..."
        self.is_online = False
        self.needs_update = False
        self.buttons = []
        
        # Iniciar verificación en hilo separado
        threading.Thread(target=self.check_connection, daemon=True).start()

    def play_game(self):
        print("Lanzando el juego...")
        # Aquí llamaríamos a subprocess.Popen(["Holo Hunger Games.exe"])
        pygame.quit()
        sys.exit()

    def update_game(self):
        if not self.is_online or not self.manifest:
            return
            
        print("Iniciando actualización...")
        self.status = "Descargando actualización..."
        
        # Iterar sobre los archivos definidos en el manifiesto
        for file_name, file_info in self.manifest.get('files', {}).items():
            file_url = file_info.get('url')
            expected_hash = file_info.get('hash')
            
            print(f"Descargando {file_name} desde {file_url}...")
            # Aquí implementaremos la lógica de descarga real
            # response = requests.get(file_url)
            # ...
            
        self.status = "Actualización completada. Reinicie el launcher."
        # self.needs_update = False
        # self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        if self.needs_update:
            self.buttons.append(Button("Actualizar", 300, 400, 200, 50, (0, 150, 0), self.update_game))
        else:
            self.buttons.append(Button("Jugar", 300, 400, 200, 50, (0, 0, 150), self.play_game))

    def calculate_hash(self, file_path):
        """Calcula el hash SHA-256 de un archivo local."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except FileNotFoundError:
            return None

    def check_connection(self):
        try:
            # Reemplazar con URL real del manifest.json en GitHub
            response = requests.get("https://raw.githubusercontent.com/KevanVault/HHG-Updates/refs/heads/main/manifest.json", timeout=5)
            if response.status_code == 200:
                self.is_online = True
                self.manifest = response.json()
                remote_version = self.manifest.get('version', '0.0')

                if remote_version > VERSION_LOCAL:
                    self.status = f"Nueva versión disponible: {remote_version}"
                    self.needs_update = True
                else:
                    self.status = f"Juego actualizado (v{VERSION_LOCAL})"
                    self.needs_update = False
                self.create_buttons()
            else:
                self.status = "Modo Offline"
        except Exception as e:
            self.status = f"Error de conexión: {e}. Modo Offline."

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for button in self.buttons:
                    button.handle_event(event)

            self.screen.fill(BG_COLOR)
            
            # Dibujar estado
            status_text = self.font.render(self.status, True, TEXT_COLOR)
            self.screen.blit(status_text, (50, 50))
            
            # Dibujar botones
            for button in self.buttons:
                button.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    launcher = Launcher()
    launcher.run()
