import pygame, random, sys, os

# Klasse für Entitäten: Packmann und die Geister sind Subklassen und erben Methoden und Attribute
class Entitaet:
    def __init__(self, x_koordinate, y_koordinate, hoehe, breite, geschwindigkeit, richtung, farbe):
        self.x_koordinate = x_koordinate
        self.y_koordinate = y_koordinate
        self.hoehe = hoehe
        self.breite = breite
        self.geschwindigkeit = geschwindigkeit
        self.richtung = richtung
        self.farbe = farbe

    def entitaet_bewegen(self):
        if self.richtung == "oben":
            self.y_koordinate -= self.geschwindigkeit
        elif self.richtung == "unten":
            self.y_koordinate += self.geschwindigkeit
        elif self.richtung == "links":
            self.x_koordinate -= self.geschwindigkeit
        elif self.richtung == "rechts":
            self.x_koordinate += self.geschwindigkeit

    # Wenn der Wegweiser Werte ausgibt, dann bedeutet das, dass die Entität, welche die Funktion aufruft, genau passend auf einer Kachel sitzt.
    def wegweiser(self, kacheln, level):
        if self.x_koordinate % kacheln == 0 and self.y_koordinate % kacheln == 0:
            erlaubte_richtungen = []
            aktuelle_kachel_x = int(self.x_koordinate / kacheln)
            aktuelle_kachel_y = int(self.y_koordinate / kacheln)

            oberer_nachbar = level[aktuelle_kachel_y - 1][aktuelle_kachel_x]
            unterer_nachbar = level[aktuelle_kachel_y + 1][aktuelle_kachel_x]
            linker_nachbar = level[aktuelle_kachel_y][aktuelle_kachel_x - 1]
            rechter_nachbar = level[aktuelle_kachel_y][aktuelle_kachel_x + 1]

            if oberer_nachbar != 1:
                erlaubte_richtungen.append("oben")
            if unterer_nachbar != 1:
                erlaubte_richtungen.append("unten")
            if linker_nachbar != 1:
                erlaubte_richtungen.append("links")
            if rechter_nachbar != 1:
                erlaubte_richtungen.append("rechts")

            return erlaubte_richtungen
        else:
            return None

class Packmann(Entitaet):
    def __init__(self, x_koordinate, y_koordinate, hoehe, breite, geschwindigkeit, richtung, farbe):
        super().__init__(x_koordinate, y_koordinate, hoehe, breite, geschwindigkeit, richtung, farbe)

    def richtung_aendern(self, erlaubte_richtungen):
        if erlaubte_richtungen:
            tasten = pygame.key.get_pressed()
            if tasten[pygame.K_RIGHT] and "rechts" in erlaubte_richtungen:
                self.richtung = "rechts"
            elif tasten[pygame.K_LEFT] and "links" in erlaubte_richtungen:
                self.richtung = "links"
            elif tasten[pygame.K_UP] and "oben" in erlaubte_richtungen:
                self.richtung = "oben"
            elif tasten[pygame.K_DOWN] and "unten" in erlaubte_richtungen:
                self.richtung = "unten"
            else:
                self.richtung = None

    def packmann_zeichnen(self, fenster, kacheln):
        centerx = self.x_koordinate + self.breite // 2
        centery = self.y_koordinate + self.hoehe // 2
        pygame.draw.circle(fenster, farbpalette(self.farbe), (centerx, centery), kacheln // 2)

    def update(self, fenster, kacheln, level):
        erlaubte_richtungen = self.wegweiser(kacheln, level)
        if erlaubte_richtungen:
            self.richtung_aendern(erlaubte_richtungen)
        self.entitaet_bewegen()
        self.packmann_zeichnen(fenster, kacheln)

    def muenzen_fressen(self, muenzen, score):
        # Erstelle ein Pygame Rect basierend auf den Packmann-Koordinaten
        packmann_rect = pygame.Rect(self.x_koordinate, self.y_koordinate, self.breite, self.hoehe)

        # Prüfe Kollisionen
        gefressene_muenze = packmann_rect.collidelist(muenzen)

        # Wenn eine Kollision gefunden wurde
        if gefressene_muenze != -1:
            muenzen.pop(gefressene_muenze)  # Entferne die Münze
            score += 1  # Erhöhe die Punktzahl

        return muenzen, score

class Geist(Entitaet):
    def __init__(self, x_koordinate, y_koordinate, hoehe, breite, geschwindigkeit, richtung, farbe):
        super().__init__(x_koordinate, y_koordinate, hoehe, breite, geschwindigkeit, richtung, farbe)

    def richtung_aendern(self, erlaubte_richtungen):
        if erlaubte_richtungen:
            if len(erlaubte_richtungen) > 2:
                self.richtung = random.choice(erlaubte_richtungen)
            elif self.richtung not in erlaubte_richtungen:
                self.richtung = random.choice(erlaubte_richtungen)

    def geist_zeichnen(self, fenster):
        pygame.draw.rect(
            fenster,
            self.farbe,  # Direktes RGB-Tupel
            (self.x_koordinate, self.y_koordinate, self.breite, self.hoehe)
        )

    def update(self, fenster, kacheln, level):
        erlaubte_richtungen = self.wegweiser(kacheln, level)
        if erlaubte_richtungen:
            self.richtung_aendern(erlaubte_richtungen)
        self.entitaet_bewegen()
        self.geist_zeichnen(fenster)


def initialisiere_packmann(level, kacheln, konfiguration):
    """
    Initialisiert einen Packmann basierend auf der Position des Werts 5 in der Level-Matrix.
    :param level: 2D-Array, das das Level beschreibt
    :param kacheln: Größe einer Kachel (Pixel)
    :return: Eine Instanz von Packmann
    """
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 5:  # Wert 5 bestimmt die Startposition von Packmann
                x_koordinate = x * kacheln
                y_koordinate = y * kacheln
                return Packmann(
                    x_koordinate=x_koordinate,
                    y_koordinate=y_koordinate,
                    hoehe=kacheln,
                    breite=kacheln,
                    geschwindigkeit= konfiguration.get("geschwindigkeit_packmann"),
                    richtung="rechts",
                    farbe="gelb"
                )
    raise ValueError("Packmann konnte nicht initialisiert werden. Wert 5 fehlt im Level.")

def zufaellige_farbe():
    """
    Generiert eine zufällige RGB-Farbe, bei der jeder Wert zwischen 50 und 255 liegt.
    """
    return (
        random.randint(50, 255),  # Rotanteil
        random.randint(50, 255),  # Grünanteil
        random.randint(50, 255)   # Blauanteil
    )


def initialisiere_geister(level, kacheln, konfiguration):
    """
    Initialisiert Geister basierend auf der Position des Werts 9 in der Level-Matrix.
    :return: Liste von Geist-Instanzen
    """
    geister = []

    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 9:  # Wert 9 bestimmt die Startposition eines Geistes
                x_koordinate = x * kacheln
                y_koordinate = y * kacheln

                # Generiere eine zufällige Farbe
                farbe = zufaellige_farbe()

                # Geist erstellen und zur Liste hinzufügen
                geister.append(
                    Geist(
                        x_koordinate=x_koordinate,
                        y_koordinate=y_koordinate,
                        hoehe=kacheln,
                        breite=kacheln,
                        geschwindigkeit=konfiguration.get("geschwindigkeit_geister"),
                        richtung=random.choice(["oben", "unten", "links", "rechts"]),  # Zufällige Richtung
                        farbe=farbe  # Zufällige Farbe als Tupel
                    )
                )

    if not geister:
        raise ValueError("Keine Geister konnten initialisiert werden. Wert 9 fehlt im Level.")

    return geister


def game_over(levels, level_name, score, packmann, muenzen, geister):
    """
    Prüft, ob das Spiel vorbei ist:
    - Packmann kollidiert mit einem Geist (Game Over).
    - Alle Münzen gesammelt (Sieg oder nächstes Level).
    """
    # Erstelle ein Rect für den Packmann basierend auf seinen Koordinaten
    packmann_rect = pygame.Rect(packmann.x_koordinate, packmann.y_koordinate, packmann.breite, packmann.hoehe)

    # Prüfe Kollision mit einem beliebigen Geist
    for geist in geister:
        geist_rect = pygame.Rect(geist.x_koordinate, geist.y_koordinate, geist.breite, geist.hoehe)
        if packmann_rect.colliderect(geist_rect):
            sieg = False
            game_over_screen(sieg, score)
            return False  # Spiel endet bei Kollision

    # Keine Münzen mehr auf dem Spielfeld
    if not muenzen:
        # Letztes Level durchgespielt
        if level_name == levels[-1]:
            sieg = True
            game_over_screen(sieg, score)
            return False  # Spiel endet mit Sieg
        else:
            next_level_screen()
            return False  # Wechsel zum nächsten Level

    # Spiel geht weiter
    return True

def hauptmenue():

    # Fenstergröße
    screen_width, screen_height = 600, 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Hauptmenü")

    # Buttons (Text, Farbe, Position)
    buttons = [
        {"text": "Spiel starten", "color": farbpalette("hellgruen"), "rect": pygame.Rect(200, 120, 200, 50)},
        {"text": "Highscores", "color": farbpalette("blau"), "rect": pygame.Rect(200, 200, 200, 50)},
        {"text": "Spiel beenden", "color": farbpalette("rot"), "rect": pygame.Rect(200, 280, 200, 50)},
    ]

    # Eventschleife für das Hauptmenü
    menue = True
    while menue:
        screen.fill(farbpalette("schwarz"))

        # Titel anzeigen
        title_text = schriftarten("gross").render("Packmann" + "\u00AE", True, farbpalette("gelb"))
        title_rect = title_text.get_rect(center=(screen_width // 2, 50))
        screen.blit(title_text, title_rect)

        # Buttons anzeigen
        for button in buttons:
            pygame.draw.rect(screen, button["color"], button["rect"])
            button_text = schriftarten("mittel").render(button["text"], True, farbpalette("weiss"))
            button_text_rect = button_text.get_rect(center=button["rect"].center)
            screen.blit(button_text, button_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Klick auf das rote Kreuz oben rechts im Fenster
                spiel_beenden()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Linksklick
                # Iteriere durch alle Buttons auf im Dictionary Buttons. Über den Index lässt sich jeder Button eine Funktion per if-Statement zuweisen.
                for i, button in enumerate(buttons):
                    if button["rect"].collidepoint(event.pos):
                        if i == 0:                                                  # Spiel starten
                            menue = False                                           # pygame läuft weiter, es wird nur das Fenster geschlossen.
                        elif i == 1:                                                # Highscores anzeigen
                            show_highscores(screen, screen_width, screen_height)    # Übergebe die größe des Hauptmenüs an den Highscore Bildschirmes
                        elif i == 2:                                                # Spiel beenden
                            spiel_beenden()

def load_highscores():
    # Lädt die Highscores aus der Datei und behandelt korrupte Daten
    try:
        with open("highscores.txt", "r") as file:
            lines = [line.strip() for line in file.readlines()]
            # Erzeuge eine Liste von Tupeln, bestehend aus einem String und einem Integer
            highscores = [tuple(line.rsplit(" ", 1)) for line in lines if " " in line]
            # Überprüfen, ob alle Scores numerisch sind
            for _, score in highscores:
                int(score)  # Test auf numerischen Score
            return highscores
    except (FileNotFoundError, ValueError, IndexError):
        return None  # Korrupte oder fehlende Datei

def clear_highscores():
    # Löscht alle Highscores
    with open("highscores.txt", "w") as file:
        file.write("")  # Datei leeren


def show_highscores(screen, screen_width, screen_height):
    # Zeigt die Highscores an und ermöglicht Rückkehr oder Löschen per Mausklick

    highscores = load_highscores()

    # Buttons
    buttons = [
        {"text": "Zurück", "color": farbpalette("hellgruen"), "rect": pygame.Rect(100, screen_height - 80, 150, 50)},
        {"text": "Alle löschen", "color": farbpalette("rot"), "rect": pygame.Rect(300, screen_height - 80, 200, 50)},
    ]

    highscore_screen = True
    while highscore_screen:
        screen.fill(farbpalette("schwarz"))

        if highscores is None: # Korruptes File
            warning_text = schriftarten("gross").render("Highscores korrupt!", True, farbpalette("rot"))
            warning_rect = warning_text.get_rect(center=(screen_width // 2, screen_height // 3))
            screen.blit(warning_text, warning_rect)

            # Kleinere Anweisungen
            instruction_text = schriftarten("klein").render("Drücke 'Alle löschen' um Highscores zurückzusetzen", True, farbpalette("weiss"))
            instruction_rect = instruction_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(instruction_text, instruction_rect)

        else: # Highscore Datei intakt
            # Titel anzeigen
            title_text = schriftarten("gross").render("Highscores", True, farbpalette("weiss"))
            title_rect = title_text.get_rect(center=(screen_width // 2, 50))
            screen.blit(title_text, title_rect)

            # Highscores anzeigen
            for i, (name, score) in enumerate(highscores[:10]):
                name_text = schriftarten("mittel").render(name, True, farbpalette("blau"))
                name_rect = name_text.get_rect(topleft=(100, 80 + i * 40))
                screen.blit(name_text, name_rect)

                score_text = schriftarten("mittel").render(score, True, farbpalette("rot"))
                score_rect = score_text.get_rect(topright=(500, 80 + i * 40))
                screen.blit(score_text, score_rect)

        # Buttons anzeigen
        for button in buttons:
            pygame.draw.rect(screen, button["color"], button["rect"])
            button_text = schriftarten("mittel").render(button["text"], True, farbpalette("weiss"))
            button_text_rect = button_text.get_rect(center=button["rect"].center)
            screen.blit(button_text, button_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                spiel_beenden()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Linksklick
                    if buttons[0]["rect"].collidepoint(event.pos):  # Zurück
                        highscore_screen = False
                    elif buttons[1]["rect"].collidepoint(event.pos):  # Löschen
                        clear_highscores()
                        highscores = load_highscores()

def check_if_highscore(score):
    # Prüft, ob der gegebene Score ein Highscore ist, und ersetzt bei Bedarf eine kaputte Datei
    try:
        with open("highscores.txt", "r") as file:
            highscores = [int(line.split()[1]) for line in file.readlines()]
    except (FileNotFoundError, ValueError, IndexError):
        # Datei fehlt oder ist korrupt, neue leere Datei erstellen
        with open("highscores.txt", "w") as file:
            file.write("")  # Neue leere Datei
        highscores = []

    return len(highscores) < 6 or score > min(highscores)
    # True, wenn weniger als 6 Highscores gespeichert sind oder der Score größer ist als der kleinste Highscore

def save_highscore(name, score):
    try:
        with open("highscores.txt", "r") as file:
            highscores = [line.strip() for line in file.readlines()]
            # Liste von Stings, jeder Sting ein Paar aus Name und Score
    except FileNotFoundError:
        highscores = []

    # Neuen Highscore hinzufügen und sortieren
    highscores.append(f"{name} {score}")
    highscores = sorted(highscores, key=lambda x: int(x.split()[1]), reverse=True)[:6]
    """Die Lambda-Funktion definiert das Sortierkriterium: die Punktzahl.
    Diese wird aus dem String herausgesplitted, und in einen int umgewandelt.
    Die 6 größten Werte werden behalten."""

    # Datei aktualisieren
    with open("highscores.txt", "w") as file:
        file.write("\n".join(highscores))

def next_level_screen():
    # Fenstergröße festlegen
    screen_width, screen_height = 400, 300
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Nächstes Level")

    # Button erstellen
    button_rect = pygame.Rect(screen_width // 2 - 125, screen_height // 2 - 25, 250, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Linksklick
                    if button_rect.collidepoint(event.pos):
                        running = False

        # Hintergrund füllen
        screen.fill(farbpalette("schwarz"))

        # Button anzeigen
        pygame.draw.rect(screen, farbpalette("hellgruen"), button_rect)
        button_text = schriftarten("mittel").render("Nächstes Level", True, farbpalette("weiss"))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

        # Fenster aktualisieren
        pygame.display.flip()

def game_over_screen(sieg, score):

        # Fenstergröße festlegen
        screen_width, screen_height = 400, 300
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Spiel beendet")

        # Nachricht basierend auf Sieg/Niederlage
        if sieg:
            message_text = schriftarten("gross").render("Sieg!", True, farbpalette("hellgruen"))
        else:
            message_text = schriftarten("gross").render("Game Over", True, farbpalette("rot"))
        message_rect = message_text.get_rect(center=(screen_width // 2, 50))

        # Punktestand anzeigen
        score_text = schriftarten("mittel").render(f"Dein Score: {score}", True, farbpalette("blau"))
        score_rect = score_text.get_rect(center=(screen_width // 2, 100))

        # Highscores prüfen
        is_highscore = check_if_highscore(score)

        name = ""
        if is_highscore:
            input_prompt = schriftarten("klein").render("Neuer Highscore! Name eingeben:", True, farbpalette("weiss"))
            input_prompt_rect = input_prompt.get_rect(center=(screen_width // 2, 150))

        # Hauptanzeigeschleife
        game_over_display = True
        while game_over_display:
            screen.fill(farbpalette("schwarz"))
            screen.blit(message_text, message_rect)
            screen.blit(score_text, score_rect)

            if is_highscore:
                screen.blit(input_prompt, input_prompt_rect)
                name_text = schriftarten("mittel").render(name, True, farbpalette("weiss"))
                name_text_rect = name_text.get_rect(center=(screen_width // 2, 200))
                screen.blit(name_text, name_text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    spiel_beenden()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and is_highscore:
                        # Name und Score speichern, Spiel beenden
                        if name == "":
                            name = "unknown_player"
                        save_highscore(name, score)
                        spiel_beenden()
                    elif event.key == pygame.K_BACKSPACE and is_highscore:
                        name = name[:-1]  # Zeichen löschen
                    elif is_highscore and len(name) < 10:  # Begrenze Namenslänge auf 10
                        name += event.unicode

def farbpalette(farbe):
    farben = {
    "schwarz": (0, 0, 0),
    "blau": (0, 30, 180),
    "gelb": (255, 255, 0),
    "weiss": (255, 255, 255),
    "rot": (255, 0, 0),
    "hellgruen": (0, 200, 0),
    }
    return farben.get(farbe)

def schriftarten(schrift):
    schriften = {
        "sehr_klein": pygame.font.Font(None, 20),
        "klein" : pygame.font.Font(None,30),
        "mittel" : pygame.font.Font(None,40),
        "gross" : pygame.font.Font(None,60),
    }
    return schriften.get(schrift)

# Generiere basierend auf Konfiguration.txt ein Dictionary
def lade_konfiguration(filename="Konfiguration.txt"):
    config = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.split("#")[0].strip()  # Kommentar entfernen und Zeile trimmen
                if line:  # Nur nicht-leere Zeilen verarbeiten
                    parts = line.split()  # Zeile in Schlüssel und Wert aufteilen
                    key = parts[0]  # Erster Teil ist der Schlüssel
                    value = parts[1] if len(parts) > 1 else "0"  # Zweiter Teil ist der Wert, falls vorhanden
                    try:
                        config[key] = abs(int((value)))  # Versuche, den Wert in einen Integer zu konvertieren
                    except ValueError:
                        print(f"Warnung: Der Wert für '{key}' ({value}) ist ungültig. Die Datei {filename} ist möglicherweise korrupt.")
                        config[key] = None  # None wird bei Bedarf später durch Defaults ersetzt
    except FileNotFoundError:
        print(f"Die Datei {filename} wurde nicht gefunden.")
    return config

def level_initialisieren(level_name):
    # Pfad zur Datei erstellen
    level_pfad = os.path.join("Levels", f"{level_name}")

    # Datei öffnen und Matrix einlesen
    with open(level_pfad, 'r') as datei:
        matrix = [
            list(map(int, line.strip().split()))
            for line in datei if line.strip() and not line.strip().startswith("#")
        ]

    # Randwerte auf 1 setzen: Ränder sind immer Wände
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i == 0 or i == len(matrix) - 1 or j == 0 or j == len(matrix[i]) - 1:
                matrix[i][j] = 1

    return matrix

def mauern_initialisieren(level, kacheln):
    mauern = []
    for y in range(len(level)):
        for x in range(len(level[0])):
            if level[y][x] == 1:
                mauerabschnitt = (x * kacheln, y * kacheln, kacheln, kacheln)
                mauern.append(mauerabschnitt)
    return mauern

def mauern_zeichnen(mauern, fenster):
    for mauerabschnitt in mauern:
        pygame.draw.rect(fenster,farbpalette("blau"),mauerabschnitt)

def muenzen_initialisieren(level, kacheln):
    muenzen = []
    for y in range(len(level)):
        for x in range(len(level[0])):
            if level[y][x] == 2:
                muenze = (x * kacheln + kacheln * 0.375, y * kacheln + kacheln * 0.375, kacheln/4, kacheln/4)
                muenzen.append(muenze)
    return muenzen

def muenzen_zeichnen(muenzen, fenster):
    for muenze in muenzen:
        pygame.draw.rect(fenster,farbpalette("gelb"),muenze)

def pruefe_konfiguration(konfiguration):
    """
    Prüft die Konfiguration für Geschwindigkeiten und Kachelgröße.
    Validiert ungültige Werte und setzt Defaults, falls notwendig.

    :param konfiguration: Dictionary mit Konfigurationswerten
    :return: Aktualisierte Konfiguration mit validierten Werten
    """
    # Prüfe Kachelgröße
    kacheln = konfiguration.get("kacheln")
    if not kacheln or not (0 < kacheln <= 32):
        konfiguration["kacheln"] = 16  # Standardwert für Kachelgröße

    # Prüfe Packmann-Geschwindigkeit
    if konfiguration.get("geschwindigkeit_packmann") is None:
        konfiguration["geschwindigkeit_packmann"] = 1
    elif konfiguration["geschwindigkeit_packmann"] != 0:
        if konfiguration["kacheln"] % konfiguration["geschwindigkeit_packmann"] != 0:
            konfiguration["geschwindigkeit_packmann"] = 1

    # Prüfe Geister-Geschwindigkeit
    if konfiguration.get("geschwindigkeit_geister") is None:
        konfiguration["geschwindigkeit_geister"] = 1
    elif konfiguration["geschwindigkeit_geister"] != 0:
        if konfiguration["kacheln"] % konfiguration["geschwindigkeit_geister"] != 0:
            konfiguration["geschwindigkeit_geister"] = 1

    return konfiguration

def score_und_level_anzeigen(fenster, fenster_x, score, level_name):
    # Text rendern
    score_text = schriftarten("sehr_klein").render(f"Score: {score}", True, farbpalette("weiss"))  # Weißer Text

    # Text auf den Bildschirm zeichnen (10px vom oberen und linken Rand)
    fenster.blit(score_text, (10, 10))

    # Levelname auf den Bildschirm zeichnen (10px vom oberen und rechten Rand)
    level_text = schriftarten("sehr_klein").render(f"{level_name}".rstrip(".txt"), True, farbpalette("weiss"))  # Weißer Text
    level_text_rect = level_text.get_rect()
    level_text_rect.topright = (fenster_x - 10, 10)
    fenster.blit(level_text, level_text_rect)

def spiel_beenden():
    pygame.quit()
    sys.exit()

def spiel(levels, level_name, score, konfiguration):
    # hier beginnt das Spiel: Es werden alle notwendigen Komponenten für die Eventschleife initialisiert
    fps = pygame.time.Clock()               # erzeuge ein Clock Objekt, um in der Event-Schleife die frames per second einzustellen

    # Erzeuge ein Fenster aus Kacheln (Tiles), Anzahl der Kacheln aus Matrix "level", größe aus Variable "kacheln"
    level = level_initialisieren(level_name)
    kacheln = konfiguration.get("kacheln")
    fenster_x = len(level[0]) * kacheln
    fenster_y = len(level) * kacheln
    fenster = pygame.display.set_mode((fenster_x,fenster_y))
    pygame.display.set_caption("Packmann"+"\u00AE")

    # Erzeuge Listen von Mauerabschnitten und Münzen
    mauern = mauern_initialisieren(level, kacheln)
    muenzen = muenzen_initialisieren(level, kacheln,)

    # Initialisiere packmann und die Geister als Objekte
    packmann = initialisiere_packmann(level, kacheln, konfiguration)
    geister = initialisiere_geister(level, kacheln, konfiguration)

    # Event-Schleife für das Spiel
    spiel = True
    while spiel:
    # Tickspeed von 60 fps
        fps.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                spiel_beenden()

        # zeichne den Hintergrund
        fenster.fill(farbpalette("schwarz"))

        # zeichne die Mauern
        mauern_zeichnen(mauern, fenster)

        # zeichne die Münzen auf der Liste
        muenzen_zeichnen(muenzen, fenster)

        # bewege und zeichne Packmann + Geister
        packmann.update(fenster, kacheln, level)
        for geist in geister:
            geist.update(fenster, kacheln, level)

        # friss Münzen
        muenzen, score = packmann.muenzen_fressen(muenzen, score)

        # Prüfe, ob das Spiel endet. Falls ja, starte den Game Over Screen
        spiel = game_over(levels,level_name, score, packmann, muenzen, geister)

        score_und_level_anzeigen(fenster, fenster_x, score, level_name)

        # Aktualisiere Bildschirm
        pygame.display.update()

    return score

# Hauptfunktion
def main():
    # starte pygame
    pygame.init()

    # Lade die Konfiguration, prüfe auf existierende und sinnhafte Werte, sonst überschreibe sie mit Defaults
    konfiguration = lade_konfiguration()
    konfiguration = pruefe_konfiguration(konfiguration)

    # initialisiere den Score
    score = 0

    # starte das Hauptmenü
    hauptmenue()

    # suche im Ordner Levels nach Level Dateien
    levels = [
        f for f in os.listdir(os.path.abspath("Levels"))
        if os.path.isfile(os.path.join(os.path.abspath("Levels"), f)) and f.lower().endswith(".txt")
    ]
    if not levels:
        print(f"Keine Levels gefunden. Bitte Integrität der Textdateien im Verzeichnis {os.path.abspath("Levels")} prüfen.")

    # starte das Spiel, durchlaufe alle Levels
    for level_name in levels:
        try:
            score = spiel(levels, level_name, score, konfiguration)
        except(FileNotFoundError, ValueError, IndexError):
            print(f"Die Datei {level_name} im Verzeichnis {os.path.abspath("Levels")} ist möglicherweise korrupt. Überspringe das Level {level_name}." )

    # beende pygame
    pygame.quit()

# Hauptprogramm
if __name__ == "__main__":
    main()