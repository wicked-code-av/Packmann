import pygame, random, sys
from pygame.rect import RectType
packmann_index = 0
frame_counter = 0  # Controls the animation speed
frames_per_update = 6  # Number of frames to wait before updating animation

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

def spawn(wert_kachel, level, kacheln):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == wert_kachel:
                rect_x = x * kacheln
                rect_y = y * kacheln
                return rect_x, rect_y

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

def packmann_bewegen_und_zeichnen(packmann, richtung_packmann, geschwindigkeit_packmann, faehrte, kacheln, level):
    global packmann_index, frame_counter

    # Ensure the current frame is initialized
    current_frame = packmann_frames[packmann_index]

    # Increment the frame counter
    frame_counter += 1

    # Update the animation frame only if the counter exceeds the threshold
    if frame_counter >= frames_per_update:
        packmann_index = (packmann_index + 1) % len(packmann_frames)  # Cycle through frames
        frame_counter = 0  # Reset the counter

    # Adjust the frame orientation based on the direction
    if richtung_packmann == "rechts":
        current_frame = packmann_frames[packmann_index]
    elif richtung_packmann == "links":
        current_frame = pygame.transform.flip(packmann_frames[packmann_index], True, False)
    elif richtung_packmann == "oben":
        current_frame = pygame.transform.rotate(packmann_frames[packmann_index], 90)
    elif richtung_packmann == "unten":
        current_frame = pygame.transform.rotate(packmann_frames[packmann_index], 270)

    # Render the current frame with the correct orientation
    fenster.blit(current_frame, (packmann.x, packmann.y))

    # Movement and direction logic
    erlaubte_richtungen, aktuelle_kachel = wegweiser(packmann, kacheln, level)
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

    if aktuelle_kachel:
        faehrte.append(aktuelle_kachel)

    # Update Packmann's position
    packmann, richtung_packmann = rect_teleportieren(packmann, richtung_packmann, geschwindigkeit_packmann)
    packmann = rect_bewegen(packmann, geschwindigkeit_packmann, richtung_packmann)

    return packmann, richtung_packmann, faehrte



def weissen_geist_bewegen_und_zeichnen(weisser_geist, richtung_weisser_geist, geschwindigkeit_weisser_geist, faehrte, kacheln, level):
    # steht der Geist im Teleporter?
    weisser_geist, richtung_weisser_geist = rect_teleportieren(weisser_geist, richtung_weisser_geist, geschwindigkeit_weisser_geist)

    # bestimme die Koordinaten der aktuellen Kachel
    _, aktuelle_kachel = wegweiser(weisser_geist, kacheln, level)
    # sitzt der Geist genau auf einer Kachel und gibt es eine Fährte?
    if aktuelle_kachel and faehrte:

        # bestimme die Richtung anhand von aktueller Kachel und Fährte
        aktuelle_kachel_x, aktuelle_kachel_y = aktuelle_kachel
        ziel_x, ziel_y = faehrte[0]

        if ziel_x > aktuelle_kachel_x:
            richtung_weisser_geist = "rechts"
        elif ziel_x < aktuelle_kachel_x:
            richtung_weisser_geist = "links"
        elif ziel_y > aktuelle_kachel_y:
            richtung_weisser_geist = "unten"
        elif ziel_y < aktuelle_kachel_y:
            richtung_weisser_geist = "oben"
        else:
            richtung_weisser_geist = None


        # ist der zweite Eintrag der Fährte gleich dem ersten? Solange dies der Fall ist, lösche die Einträge. Diese Duplikate entstehen, wenn packmann still steht
        if len(faehrte) > 2:
            while faehrte[0] == faehrte[1] and len(faehrte) > 2:
                faehrte.pop(1)
        # lösche den Eintrag, im nächsten Durchlauf wird ein neues Ziel anvisiert
        faehrte.pop(0)


    # Bewege den Geist
    weisser_geist = rect_bewegen(weisser_geist, geschwindigkeit_weisser_geist, richtung_weisser_geist)
    # Zeichne den Geist
    pygame.draw.rect(fenster, farbpalette("weiss"), weisser_geist)
    # gib die relevanten Informationen zurück an das Hauptprogramm
    return weisser_geist, richtung_weisser_geist

def roten_geist_bewegen_und_zeichnen(roter_geist, richtung_roter_geist, geschwindigkeit_roter_geist, kacheln, level):
    # checke mögliche Richtungen, weise diese dem Geist zu
    erlaubte_richtungen,_ = wegweiser(roter_geist, kacheln, level)
    if erlaubte_richtungen:
        # kann der Geist sich weiterbewegen? falls nein ändere die Richtung
        if richtung_roter_geist not in erlaubte_richtungen:
            richtung_roter_geist = random.choice(erlaubte_richtungen)

    # bewege den Geist anhand von Geschwindigkeit und Richtung
    roter_geist = rect_bewegen(roter_geist, geschwindigkeit_roter_geist, richtung_roter_geist)
    # Zeichne den Geist
    pygame.draw.rect(fenster, farbpalette("rot"), roter_geist)
    # gib die relevanten Informationen zurück an das Hauptprogramm
    return roter_geist, richtung_roter_geist

def rosa_geist_bewegen_und_zeichnen(rosa_geist, geschwindigkeit_rosa_geist, richtung_rosa_geist, patrouille, kacheln, level):
    # steht der Geist im Teleporter?
    rosa_geist, richtung_rosa_geist = rect_teleportieren(rosa_geist, richtung_rosa_geist, geschwindigkeit_rosa_geist)

    # bestimme die Koordinaten der aktuellen Kachel
    _, aktuelle_kachel = wegweiser(rosa_geist, kacheln, level)
    # sitzt der Geist genau passend auf einer Kachel? Falls ja, soll anhand der Patrouille das nächste Ziel anvisiert werden
    if aktuelle_kachel:
        if aktuelle_kachel in patrouille:
            aktuelle_kachel_x, aktuelle_kachel_y = aktuelle_kachel
            ziel_x, ziel_y = patrouille[(patrouille.index(aktuelle_kachel))+1]

            if ziel_x > aktuelle_kachel_x:
                richtung_rosa_geist = "rechts"
            elif ziel_x < aktuelle_kachel_x:
                richtung_rosa_geist = "links"
            elif ziel_y > aktuelle_kachel_y:
                richtung_rosa_geist = "unten"
            elif ziel_y < aktuelle_kachel_y:
                richtung_rosa_geist = "oben"
        else:
            richtung_rosa_geist = None

    # bewege den Geist anhand von Geschwindigkeit und Richtung
    rosa_geist = rect_bewegen(rosa_geist, geschwindigkeit_rosa_geist, richtung_rosa_geist)
    # Zeichne den Geist
    pygame.draw.rect(fenster, farbpalette("rosa"), rosa_geist)
    # gib die relevanten Informationen zurück an das Hauptprogramm
    return rosa_geist, richtung_rosa_geist

def gruenen_geist_bewegen_und_zeichnen(gruener_geist, geschwindigkeit_gruener_geist, richtung_gruener_geist, kacheln, level):
    # steht der Geist im Teleporter?
    gruener_geist, richtung_gruener_geist = rect_teleportieren(gruener_geist, richtung_gruener_geist, geschwindigkeit_gruener_geist)

    # checke mögliche Richtungen, weise diese dem Geist zu
    erlaubte_richtungen, _ = wegweiser(gruener_geist, kacheln, level)
    if erlaubte_richtungen:
        # gibt es mehr als 2 mögliche Richtungen? Wegkreuzung, entscheide neu
        if len(erlaubte_richtungen) > 2:
            richtung_gruener_geist = random.choice(erlaubte_richtungen)
        # kann der Geist sich weiterbewegen? falls nein ändere die Richtung
        if richtung_gruener_geist not in erlaubte_richtungen:
            richtung_gruener_geist = random.choice(erlaubte_richtungen)

    # bewege den Geist anhand von Geschwindigkeit und Richtung
    gruener_geist = rect_bewegen(gruener_geist, geschwindigkeit_gruener_geist, richtung_gruener_geist)
    # Zeichne den Geist
    pygame.draw.rect(fenster, farbpalette("limette"), gruener_geist)
    # gib die relevanten Informationen zurück an das Hauptprogramm
    return gruener_geist, richtung_gruener_geist

def vielfrass(packmann, muenzen, score):
    gefressene_muenze = pygame.Rect.collidelist(packmann, muenzen)
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
    x_packmann, y_packmann = spawn(5, level, kacheln)
    geschwindigkeit_packmann = konfiguration.get("geschwindigkeit_packmann")
    richtung_packmann = None
    packmann = RectType(x_packmann,y_packmann,kacheln,kacheln)
    packmann_frames = []
    for i in range(1, 4):
        packmann_frames.append(pygame.transform.scale(pygame.image.load(f"assets/player_images/{i}.png"), (kacheln, kacheln)))

    # Initialisiere weißen Geist für die Event-Schleife (Wert 6 in Level.txt)
    x_weisser_geist, y_weisser_geist = spawn(6, level, kacheln)
    geschwindigkeit_weisser_geist = konfiguration.get("geschwindigkeit_weisser_geist")
    richtung_weisser_geist = None
    weisser_geist = RectType(x_weisser_geist, y_weisser_geist, kacheln, kacheln)
    # Der weiße Geist folgt der Fährte zum Packmann
    faehrte = [(12, 15), (12, 14), (12, 13), (12, 12), (12, 11), (11, 11), (10, 11), (9, 11), (9, 12), (9, 13), (9, 14), (9, 15), (9, 16), (9, 17), (9, 18), (9, 19), (9, 20), (10, 20), (11, 20), (12, 20), (12, 21), (12, 22), (12, 23)]

    # Initialisiere roten Geist für die Event-Schleife (Wert 7 in Level.txt)
    x_roter_geist, y_roter_geist = spawn(7, level, kacheln)
    geschwindigkeit_roter_geist = konfiguration.get("geschwindigkeit_roter_geist")
    richtung_roter_geist = None
    roter_geist = RectType(x_roter_geist, y_roter_geist, kacheln, kacheln)

    # Initialisiere rosa Geist für die Event-Schleife (Wert 8 in Level.txt)
    x_rosa_geist, y_rosa_geist = spawn(8, level, kacheln)
    geschwindigkeit_rosa_geist = konfiguration.get("geschwindigkeit_rosa_geist")
    richtung_rosa_geist = None
    rosa_geist = RectType(x_rosa_geist, y_rosa_geist, kacheln, kacheln)
    # Der rosa Geist hat eine fest definierte Route zu patrouillieren
    patrouille = [(16, 13), (15, 13), (15, 12), (15, 11), (16, 11), (17, 11), (18, 11), (18, 12), (18, 13), (18, 14), (18, 15), (18, 16), (18, 17), (18, 18), (18, 19), (18, 20), (17, 20), (16, 20), (15, 20), (15, 21), (15, 22), (15, 23), (16, 23), (17, 23), (18, 23), (19, 23), (20, 23), (21, 23), (21, 22), (21, 21), (21, 20), (21, 19), (21, 18), (21, 17), (21, 16), (21, 15), (21, 14), (22, 14), (23, 14), (24, 14), (25, 14), (26, 14), (2, 14), (3, 14), (4, 14), (5, 14), (6, 14), (6, 15), (6, 16), (6, 17), (6, 18), (6, 19), (6, 20), (5, 20), (4, 20), (3, 20), (2, 20), (1, 20), (1, 21), (1, 22), (1, 23), (2, 23), (3, 23), (3, 24), (3, 25), (3, 26), (4, 26), (5, 26), (6, 26), (6, 25), (6, 24), (6, 23), (7, 23), (8, 23), (9, 23), (10, 23), (11, 23), (12, 23), (12, 22), (12, 21), (12, 20), (11, 20), (10, 20), (9, 20), (9, 19), (9, 18), (9, 17), (9, 16), (9, 15), (9, 14), (9, 13), (9, 12), (9, 11), (10, 11), (11, 11), (12, 11), (12, 10), (12, 9), (12, 8), (11, 8), (10, 8), (9, 8), (9, 7), (9, 6), (9, 5), (10, 5), (11, 5), (12, 5), (13, 5), (14, 5), (15, 5), (16, 5), (17, 5), (18, 5), (18, 6), (18, 7), (18, 8), (17, 8), (16, 8), (15, 8), (15, 9), (15, 10),(15, 11)]

    # Initialisiere gruenen Geist für die Event-Schleife (Wert 9 in Level.txt)
    x_gruener_geist, y_gruener_geist = spawn(9, level, kacheln)
    geschwindigkeit_gruener_geist = konfiguration.get("geschwindigkeit_gruener_geist")
    richtung_gruener_geist = None
    gruener_geist = RectType(x_rosa_geist, y_rosa_geist, kacheln, kacheln)

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

        # packmann
        packmann, richtung_packmann, faehrte = packmann_bewegen_und_zeichnen(packmann, richtung_packmann, geschwindigkeit_packmann, faehrte, kacheln, level)

        # weisser Geist, jagd den Packmann, nutzt Teleporter
        weisser_geist, richtung_weisser_geist = weissen_geist_bewegen_und_zeichnen(weisser_geist, richtung_weisser_geist, geschwindigkeit_weisser_geist, faehrte, kacheln, level)

        # roter Geist, bewegt sich zufällig
        roter_geist, richtung_roter_geist = roten_geist_bewegen_und_zeichnen(roter_geist, richtung_roter_geist, geschwindigkeit_roter_geist, kacheln, level)

        # rosa Geist, patrouilliert eine vorgegebene Route, nutzt Teleporter
        rosa_geist, richtung_rosa_geist = rosa_geist_bewegen_und_zeichnen(rosa_geist, geschwindigkeit_rosa_geist, richtung_rosa_geist, patrouille, kacheln, level)

        # gruener Geist, Upgrade vom rotem Geist, entscheidet sich an Wegkreuzungen neu, kann Teleporter benutzen
        gruener_geist, richtung_gruener_geist = gruenen_geist_bewegen_und_zeichnen(gruener_geist, geschwindigkeit_gruener_geist, richtung_gruener_geist, kacheln, level)

        # friss Münzen
        muenzen, score = vielfrass(packmann, muenzen, score)

        # Aktualisiere die Liste der Geister und prüfe, ob das Spiel endet. Falls ja, initialisiere den GameOver Screen
        geister = game_over(score, packmann,muenzen, roter_geist, weisser_geist, rosa_geist, gruener_geist)

        # Aktualisiere Bildschirm
        pygame.display.update()

    pygame.quit()