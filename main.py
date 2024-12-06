import pygame, random, sys
from pygame.rect import RectType

def hauptmenue():
    # Pygame initialisieren
    pygame.init()

    # Fenstergröße
    screen_width, screen_height = 600, 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Hauptmenü")

    # Schriftart
    font_title = pygame.font.Font(None, 60)
    font_button = pygame.font.Font(None, 40)

    # Buttons (Text, Farbe, Position)
    buttons = [
        {"text": "Spiel starten", "color": farbpalette("hellgruen"), "rect": pygame.Rect(200, 120, 200, 50)},
        {"text": "Highscores", "color": farbpalette("blau"), "rect": pygame.Rect(200, 200, 200, 50)},
        {"text": "Spiel beenden", "color": farbpalette("rot"), "rect": pygame.Rect(200, 280, 200, 50)},
    ]

    menue = True
    while menue:
        screen.fill(farbpalette("schwarz"))

        # Titel anzeigen
        title_text = font_title.render("Packmann"+"\u00AE", True, farbpalette("gelb"))
        title_rect = title_text.get_rect(center=(screen_width // 2, 50))
        screen.blit(title_text, title_rect)

        # Buttons anzeigen
        for button in buttons:
            pygame.draw.rect(screen, button["color"], button["rect"])
            button_text = font_button.render(button["text"], True, farbpalette("weiss"))
            button_text_rect = button_text.get_rect(center=button["rect"].center)
            screen.blit(button_text, button_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Linksklick
                    for i, button in enumerate(buttons):
                        if button["rect"].collidepoint(event.pos):
                            if i == 0:  # Spiel starten
                                menue = False
                            elif i == 1:  # Highscores anzeigen
                                show_highscores(screen, screen_width, screen_height)
                            elif i == 2:  # Spiel beenden
                                pygame.quit()
                                sys.exit()

                                #Funktion für das Spiel beenden

def show_highscores(screen, screen_width, screen_height):
    """Zeigt die Highscores an und ermöglicht Rückkehr oder Löschen per Mausklick."""

    def load_highscores():
        """Lädt die Highscores aus der Datei und behandelt korrupte Daten."""
        try:
            with open("highscores.txt", "r") as file:
                lines = [line.strip() for line in file.readlines()]
                highscores = [tuple(line.rsplit(" ", 1)) for line in lines if " " in line]
                # Überprüfen, ob alle Scores numerisch sind
                for _, score in highscores:
                    int(score)  # Test auf numerischen Score
                return highscores
        except (FileNotFoundError, ValueError, IndexError):
            return None  # Korrupte oder fehlende Datei

    def clear_highscores():
        """Löscht alle Highscores."""
        with open("highscores.txt", "w") as file:
            file.write("")  # Datei leeren

    highscores = load_highscores()

    # Schriftarten
    font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 30)  # Kleinere Schrift für Instruktionen
    title_font = pygame.font.Font(None, 60)

    # Buttons
    buttons = [
        {"text": "Zurück", "color": farbpalette("hellgruen"), "rect": pygame.Rect(100, screen_height - 80, 150, 50)},
        {"text": "Alle löschen", "color": farbpalette("rot"), "rect": pygame.Rect(300, screen_height - 80, 200, 50)},
    ]

    highscore_screen = True
    while highscore_screen:
        screen.fill(farbpalette("schwarz"))

        if highscores is None:
            # Korruptes File
            warning_text = title_font.render("Highscores korrupt!", True, farbpalette("rot"))
            warning_rect = warning_text.get_rect(center=(screen_width // 2, screen_height // 3))
            screen.blit(warning_text, warning_rect)

            # Kleinere Anweisungen
            instruction_text = small_font.render(
                "Drücke 'Alle löschen' um Highscores zurückzusetzen", True, farbpalette("weiss")
            )
            instruction_rect = instruction_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(instruction_text, instruction_rect)
        else:
            # Titel anzeigen
            title_text = title_font.render("Highscores", True, farbpalette("weiss"))
            title_rect = title_text.get_rect(center=(screen_width // 2, 50))
            screen.blit(title_text, title_rect)

            # Highscores anzeigen
            for i, (name, score) in enumerate(highscores[:10]):
                name_text = font.render(name, True, farbpalette("blau"))
                name_rect = name_text.get_rect(topleft=(100, 120 + i * 40))
                screen.blit(name_text, name_rect)

                score_text = font.render(score, True, farbpalette("rot"))
                score_rect = score_text.get_rect(topright=(500, 120 + i * 40))
                screen.blit(score_text, score_rect)

        # Buttons anzeigen
        for button in buttons:
            pygame.draw.rect(screen, button["color"], button["rect"])
            button_text = font.render(button["text"], True, farbpalette("weiss"))
            button_text_rect = button_text.get_rect(center=button["rect"].center)
            screen.blit(button_text, button_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Linksklick
                    if buttons[0]["rect"].collidepoint(event.pos):  # Zurück
                        highscore_screen = False
                    elif buttons[1]["rect"].collidepoint(event.pos):  # Löschen
                        clear_highscores()
                        highscores = load_highscores()

def check_if_highscore(score):
    """Prüft, ob der gegebene Score ein Highscore ist, und ersetzt bei Bedarf eine kaputte Datei."""
    try:
        with open("highscores.txt", "r") as file:
            highscores = [int(line.split()[1]) for line in file.readlines()]
    except (FileNotFoundError, ValueError, IndexError):
        # Datei fehlt oder ist korrupt, neue leere Datei erstellen
        with open("highscores.txt", "w") as file:
            file.write("")  # Neue leere Datei
        highscores = []

    return len(highscores) < 10 or score > min(highscores)

def save_highscore(name, score):
    try:
        with open("highscores.txt", "r") as file:
            highscores = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        highscores = []

    # Neuen Highscore hinzufügen und sortieren
    highscores.append(f"{name} {score}")
    highscores = sorted(highscores, key=lambda x: int(x.split()[1]), reverse=True)[:10]

    # Datei aktualisieren
    with open("highscores.txt", "w") as file:
        file.write("\n".join(highscores))

def game_over(score, packmann, muenzen, roter_geist, weisser_geist, rosa_geist, gruener_geist):

    # Initialisiere Liste mit Geistern
    geister = [roter_geist, weisser_geist, rosa_geist, gruener_geist]

    # Prüfe Kollision mit Geistern, -1 steht für Kollision mit beliebigem Geist auf der Liste
    if pygame.Rect.collidelist(packmann, geister) != -1:
        niederlage = True
        sieg = False

    # prüfe, ob alle Münzen eingesammelt worden sind
    elif not muenzen:
        sieg = True
        niederlage = False

    # kein GameOver: Keine Kollision, es gibt noch Münzen auf dem Spielfeld.
    else:
        return geister

    # sieg oder niederlage
    if sieg or niederlage:

        # Pygame initialisieren
        pygame.init()

        # Fenstergröße festlegen
        screen_width, screen_height = 400, 300
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Spiel beendet")

        # Schriftarten
        font_large = pygame.font.Font(None, 50)
        font_medium = pygame.font.Font(None, 30)

        # Nachricht basierend auf Sieg/Niederlage
        if sieg:
            message_text = font_large.render("Level abgeschlossen!", True, farbpalette("hellgruen"))
        if niederlage:
            message_text = font_large.render("Game Over", True, farbpalette("rot"))
        message_rect = message_text.get_rect(center=(screen_width // 2, 50))

        # Punktestand anzeigen
        score_text = font_medium.render(f"Dein Score: {score}", True, farbpalette("blau"))
        score_rect = score_text.get_rect(center=(screen_width // 2, 100))

        # Highscores prüfen
        is_highscore = check_if_highscore(score)

        name = ""
        if is_highscore:
            input_prompt = font_medium.render("Neuer Highscore! Name eingeben:", True, farbpalette("weiss"))
            input_prompt_rect = input_prompt.get_rect(center=(screen_width // 2, 150))

        # Hauptanzeigeschleife
        game_over_screen = True
        while game_over_screen:
            screen.fill(farbpalette("schwarz"))
            screen.blit(message_text, message_rect)
            screen.blit(score_text, score_rect)

            if is_highscore:
                screen.blit(input_prompt, input_prompt_rect)
                name_text = font_medium.render(name, True, farbpalette("weiss"))
                name_text_rect = name_text.get_rect(center=(screen_width // 2, 200))
                screen.blit(name_text, name_text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and is_highscore:
                        # Name und Score speichern
                        save_highscore(name, score)
                        game_over_screen = False
                    elif event.key == pygame.K_BACKSPACE and is_highscore:
                        name = name[:-1]  # Zeichen löschen
                    elif is_highscore and len(name) < 10:  # Begrenze Namenslänge auf 10
                        name += event.unicode

        pygame.quit()
        sys.exit()

def farbpalette(farbe):
    farben = {
    "schwarz": (0, 0, 0),
    "blau": (0, 30, 180),
    "violett": (148, 0, 211),
    "gelb": (255, 255, 0),
    "weiss": (255, 255, 255),
    "rosa": (255, 192, 203),
    "rot": (255, 0, 0),
    "limette": (173, 255, 47),
    "hellgruen": (0, 200, 0),
    }
    return farben.get(farbe)

# Generiere basierend auf Konfiguration.txt ein Dictionary
def lade_konfiguration(filename="Konfiguration.txt"):
    config = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.split("#")[0].strip()  # Kommentar entfernen und Zeile trimmen
                if line:  # Nur nicht-leere Zeilen verarbeiten
                    key, value = line.split()[:2]  # Key und Value extrahieren
                    config[key] = float(value) if "." in value else int(value)  # Typ bestimmen
    except FileNotFoundError:
        print(f"Die Datei {filename} wurde nicht gefunden.")
    return config


def level_initialisieren():
    with open("Level.txt", 'r') as datei:
        return [list(map(int, line.strip().split())) for line in datei]

def mauern_initialisieren(level, kacheln):
    mauern = []
    for y in range(len(level)):
        for x in range(len(level[0])):
            if level[y][x] == 1:
                mauerabschnitt = (x * kacheln, y * kacheln, kacheln, kacheln)
                mauern.append(mauerabschnitt)
    return mauern

def mauern_zeichnen(mauern):
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

def muenzen_zeichnen(muenzen):
    for muenze in muenzen:
        pygame.draw.rect(fenster,farbpalette("gelb"),muenze)

def teleporter_initialisieren(level, kacheln):
    teleporter = []
    for y in range(len(level)):
        for x in range(len(level[0])):
            if level[y][x] == 3:
                portal = RectType(x * kacheln, y * kacheln, kacheln, kacheln)
                teleporter.append(portal)
    return teleporter

def teleporter_zeichen(teleporter, kacheln):
    for portal in teleporter:
        pygame.draw.circle(fenster, farbpalette("violett"), (portal.centerx, portal.centery), kacheln / 2)

# Erzeuge ein Rect auf einer Kachel mit einem bestimmten wert
def erzeuge_rect(wert_kachel, level, kacheln):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == wert_kachel:
                rect_x = x * kacheln
                rect_y = y * kacheln
                rect = RectType(rect_x, rect_y, kacheln, kacheln)
                return rect

def wegweiser(rect, kacheln, level):
    # Erzeuge die Koordinaten des Rect-Objekts
    rect_x, rect_y,_,_ = rect
    # Falls das Rect-Object genau passend auf einer Kachel sitzt:
    if rect_x % kacheln == 0 and rect_y % kacheln == 0:
        # initialisiere Liste
        erlaubte_richtungen = []
        # Erzeuge die Koordinaten der Kachel im Raster und rufe ihre Nachbarn ab
        aktuelle_kachel_x = int (rect_x/kacheln)
        aktuelle_kachel_y = int (rect_y/kacheln)
        aktuelle_kachel = (aktuelle_kachel_x, aktuelle_kachel_y)
        oberer_nachbar = level[aktuelle_kachel_y - 1][aktuelle_kachel_x]
        unterer_nachbar = level[aktuelle_kachel_y + 1][aktuelle_kachel_x]
        linker_nachbar = level[aktuelle_kachel_y][aktuelle_kachel_x - 1]
        rechter_nachbar = level[aktuelle_kachel_y][aktuelle_kachel_x + 1]
        # Erzeuge eine Liste erlaubter Richtungen
        if oberer_nachbar != 1:
            erlaubte_richtungen.append("oben")
        if unterer_nachbar != 1:
            erlaubte_richtungen.append("unten")
        if linker_nachbar != 1:
            erlaubte_richtungen.append("links")
        if rechter_nachbar != 1:
            erlaubte_richtungen.append("rechts")
        return erlaubte_richtungen, aktuelle_kachel
    else:
        return None, None

def rect_bewegen(rect, geschwindigkeit_rect, richtung_rect):
    # bestimme die Koordinaten des Rect-Objekts
    x_rect, y_rect, _, _ = rect
    # bewege das Rect-Objekts
    if richtung_rect == "oben":
        y_rect = y_rect - 1 * geschwindigkeit_rect
    elif richtung_rect == "unten":
        y_rect = y_rect + 1 * geschwindigkeit_rect
    elif richtung_rect == "links":
        x_rect = x_rect - 1 * geschwindigkeit_rect
    elif richtung_rect == "rechts":
        x_rect = x_rect + 1 * geschwindigkeit_rect
    # deklariere das Rect-Objekts neu anhand der angepassten Koordinaten
    rect = RectType(x_rect, y_rect, kacheln, kacheln)
    # gib das angepasste Rect-Objekt zurück
    return rect

def rect_teleportieren(rect, richtung_rect, geschwindigkeit_rect):
    # bestimme die Koordinaten des Rect-Objekts
    x_rect, y_rect, kacheln, _ = rect
    # Rect-Objekt erreicht rechten Teleporter:
    if x_rect == 26 * kacheln and y_rect == 14 * kacheln:
        # Teleportiere zu linkem Teleporter mit offset in +x-Richtung abhängig von der Geschwindigkeit (verhindert sofortiges zurück-teleportieren in manchen Fällen)
        x_rect, y_rect = 1 * kacheln + geschwindigkeit_rect, 14 * kacheln
        richtung_rect = "rechts"
    # Rect-Objekt erreicht rechten Teleporter:
    if x_rect == 1 * kacheln and y_rect == 14 * kacheln:
        # Teleportiere zu rechtem Teleporter mit offset in -x-Richtung abhängig von der Geschwindigkeit (verhindert sofortiges zurück-teleportieren in manchen Fällen)
        x_rect, y_rect = 26 * kacheln - geschwindigkeit_rect, 14 * kacheln
        richtung_rect = "links"
    rect = RectType(x_rect,y_rect,kacheln,kacheln)
    return rect, richtung_rect

def geist_bewegen_und_zeichnen(aktueller_geist, geschwindigkeit_aktueller_geist, richtung_aktueller_geist, farbe, kacheln, level):

    # steht der Geist im Teleporter?
    aktueller_geist, richtung_aktueller_geist = rect_teleportieren(aktueller_geist, richtung_aktueller_geist, geschwindigkeit_aktueller_geist)

    # checke mögliche Richtungen, weise diese dem Geist zu
    erlaubte_richtungen, _ = wegweiser(aktueller_geist, kacheln, level)
    if erlaubte_richtungen:
        # gibt es mehr als 2 mögliche Richtungen? Wegkreuzung, entscheide neu
        if len(erlaubte_richtungen) > 2:
            richtung_aktueller_geist = random.choice(erlaubte_richtungen)
        # kann der Geist sich weiterbewegen? falls nein ändere die Richtung
        if richtung_aktueller_geist not in erlaubte_richtungen:
            richtung_aktueller_geist = random.choice(erlaubte_richtungen)

    # bewege den Geist anhand von Geschwindigkeit und Richtung
    aktueller_geist = rect_bewegen(aktueller_geist, geschwindigkeit_aktueller_geist, richtung_aktueller_geist)
    # Zeichne den Geist
    pygame.draw.rect(fenster, farbpalette(farbe), aktueller_geist)
    # gib die relevanten Informationen zurück an das Hauptprogramm
    return aktueller_geist, richtung_aktueller_geist

def packmann_bewegen_und_zeichnen(packmann, richtung_packmann, geschwindigkeit_packmann, kacheln, level):

    # gab es ein Update der erlaubten Richtungen für packmann? (er steht auf einer Wegkreuzung)
    erlaubte_richtungen, aktuelle_kachel = wegweiser(packmann, kacheln, level)

    # Falls ja, ändere die Richtung abhängig vom User-Input
    if erlaubte_richtungen:
        tasten = pygame.key.get_pressed()
        if tasten[pygame.K_RIGHT] and "rechts" in erlaubte_richtungen:
            richtung_packmann = "rechts"
        elif tasten[pygame.K_LEFT] and "links" in erlaubte_richtungen:
            richtung_packmann = "links"
        elif tasten[pygame.K_UP] and "oben" in erlaubte_richtungen:
            richtung_packmann = "oben"
        elif tasten[pygame.K_DOWN] and "unten" in erlaubte_richtungen:
            richtung_packmann = "unten"
        else:
            richtung_packmann = None

    # steht packmann im Teleporter?
    packmann, richtung_packmann = rect_teleportieren(packmann, richtung_packmann, geschwindigkeit_packmann)

    # bewege den packmann anhand von Geschwindigkeit und Richtung
    packmann = rect_bewegen(packmann, geschwindigkeit_packmann, richtung_packmann)

    # zeichne den packmann als Kreis
    pygame.draw.circle(fenster, farbpalette("gelb"), (packmann.centerx, packmann.centery), kacheln / 2)

    # gib die relevanten Informationen zurück an das Hauptprogramm
    return packmann, richtung_packmann

def muenzen_fressen(packmann, muenzen, score):
    gefressene_muenze = pygame.Rect.collidelist(packmann, muenzen)
    # bei Kollision gibt collidelist als Argument den Indexeintrag des entsprechenden Elements
    if gefressene_muenze != -1:
        muenzen.pop(gefressene_muenze)
        score = score + 1
    return muenzen, score

if __name__ == "__main__":

    # Starte das Hauptmenü
    hauptmenue()

    # hier beginnt das Spiel: Es werden alle notwendigen Komponenten für die Eventschleife initialisiert
    pygame.init()               # starte pygame
    fps = pygame.time.Clock()   # erzeuge ein Clock Objekt, um in der Event-Schleife die frames per second einzustellen
    score = 0                   # initialisiere den Score
    konfiguration = lade_konfiguration()

    # Erzeuge ein Fenster aus Kacheln (Tiles), Anzahl der Kacheln aus Matrix "Level.txt", größe aus Variable "kacheln"
    level = level_initialisieren()
    kacheln = konfiguration.get("kacheln",)
    fenster_x = len(level[0]) * kacheln
    fenster_y = len(level) * kacheln
    fenster = pygame.display.set_mode((fenster_x,fenster_y))
    pygame.display.set_caption("Packmann"+"\u00AE")

    # Erzeuge Listen von Mauerabschnitten, Münzen und Teleportern
    mauern = mauern_initialisieren(level, kacheln)
    muenzen = muenzen_initialisieren(level, kacheln)
    teleporter = teleporter_initialisieren(level, kacheln)

    # Initialisiere packmann (Wert 5 in Level.txt) für die Event-Schleife
    packmann = erzeuge_rect(5, level, kacheln)
    geschwindigkeit_packmann = konfiguration.get("geschwindigkeit_packmann")
    richtung_packmann = None

    # Initialisiere weißen Geist für die Event-Schleife (Wert 6 in Level.txt)
    weisser_geist = erzeuge_rect(6, level, kacheln)
    geschwindigkeit_weisser_geist = konfiguration.get("geschwindigkeit_weisser_geist")
    richtung_weisser_geist = None

    # Initialisiere roten Geist für die Event-Schleife (Wert 7 in Level.txt)
    roter_geist = erzeuge_rect(7, level, kacheln)
    geschwindigkeit_roter_geist = konfiguration.get("geschwindigkeit_roter_geist")
    richtung_roter_geist = None

    # Initialisiere rosa Geist für die Event-Schleife (Wert 8 in Level.txt)
    rosa_geist = erzeuge_rect(8, level, kacheln)
    geschwindigkeit_rosa_geist = konfiguration.get("geschwindigkeit_rosa_geist")
    richtung_rosa_geist = None

    # Initialisiere gruenen Geist für die Event-Schleife (Wert 9 in Level.txt)
    gruener_geist = erzeuge_rect(9, level, kacheln)
    geschwindigkeit_gruener_geist = konfiguration.get("geschwindigkeit_gruener_geist")
    richtung_gruener_geist = None

    # Event-Schleife
    spiel = True
    while spiel:
    # Tickspeed von 60 fps
        fps.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                spiel = False

        # zeichne den Hintergrund
        fenster.fill(farbpalette("schwarz"))

        # zeichne die Mauern
        mauern_zeichnen(mauern)

        # zeichne die Münzen auf der Liste
        muenzen_zeichnen(muenzen)

        # zeichne die Teleporter
        teleporter_zeichen(teleporter, kacheln)

        # bewege und zeichne Packmann und Geister
        packmann, richtung_packmann = packmann_bewegen_und_zeichnen(packmann, richtung_packmann, geschwindigkeit_packmann, kacheln, level)
        weisser_geist, richtung_weisser_geist = geist_bewegen_und_zeichnen(weisser_geist, geschwindigkeit_weisser_geist, richtung_weisser_geist,"weiss", kacheln, level)
        roter_geist, richtung_roter_geist = geist_bewegen_und_zeichnen(roter_geist, geschwindigkeit_roter_geist, richtung_roter_geist, "rot", kacheln, level)
        rosa_geist, richtung_rosa_geist = geist_bewegen_und_zeichnen(rosa_geist, geschwindigkeit_rosa_geist, richtung_rosa_geist, "rosa", kacheln, level)
        gruener_geist, richtung_gruener_geist = geist_bewegen_und_zeichnen(gruener_geist, geschwindigkeit_gruener_geist, richtung_gruener_geist, "limette", kacheln, level)

        # friss Münzen
        muenzen, score = muenzen_fressen(packmann, muenzen, score)

        # Aktualisiere die Liste der Geister und prüfe, ob das Spiel endet. Falls ja, initialisiere den GameOver Screen
        geister = game_over(score, packmann,muenzen, roter_geist, weisser_geist, rosa_geist, gruener_geist)

        # Aktualisiere Bildschirm
        pygame.display.update()

    pygame.quit()