# Packmann Game

## 🎮 Spielbeschreibung
Packmann ist ein klassisches Arcade-Spiel, bei dem der Spieler als Packmann Punkte (Münzen) sammelt, Geistern ausweicht und Level abschließt. Das Spiel unterstützt mehrere Level mit steigender Schwierigkeit und bietet ein Hauptmenü sowie eine Highscore-Anzeige.

---

## 📊 Funktionen

### Grundlegende Spielmechanik:
- Steuerbarer Packmann: Bewegen Sie den Packmann mit den Pfeiltasten (↑, ↓, ←, →).
- Gegner (Geister): Sie bewegen sich zufällig auf dem Spielfeld und versuchen, Packmann zu erwischen.
- Punkte sammeln: Packmann kann Münzen aufsammeln, um Punkte zu sammeln.
- Level abschließen: Ein Level endet, wenn alle Münzen gesammelt sind.
- Game Over: Das Spiel endet, wenn Packmann mit einem Geist kollidiert.
- Im Game Over Bildschirm Namen eingeben und Enter drücken zum Speichern des Scores.

### Benutzeroberfläche:
- **Hauptmenü**: Optionen zum Starten des Spiels, Anzeigen von Highscores und Beenden des Spiels.
- **Highscores**: Speicherung und Anzeige der besten Spielergebnisse.
- **Spielanzeige**: Punkte und Level werden während des Spiels angezeigt.

### Konfiguration:
- Dynamische Anpassung der Spielfeldgröße basierend auf einer Konfigurationsdatei (`Konfiguration.txt`).
- Anpassbare Geschwindigkeit für Packmann und Geister.

### Fehlerbehandlung:
- Fehlerhafte oder fehlende Dateien (Levels, Highscores, Konfiguration) werden erkannt und sinnvoll behandelt.
- Standardwerte werden automatisch verwendet, wenn ungültige Konfigurationen vorliegen.

---

## 🗄 Dateien und Ordnerstruktur

```
Packmann/
|-- Levels/                      # Enthält die Level-Textdateien
|   |-- Level1.txt
|   |-- Level2.txt
|-- highscores.txt               # Speicherung der Highscores
|-- Konfiguration.txt            # Konfigurationsdatei mit Spieleinstellungen
|-- main.py                      # Hauptskript des Spiels
|-- README.md                    # Diese Anleitung
```

---

## 🔨 Anforderungen
- **Python 3.8+**
- **Pygame**: Installation mit `pip install pygame`

---

## 🔧 Installation
1. Klonen oder herunterladen dieses Repositories:
   ```bash
   git clone https://github.com/wicked-code-av/Packmann.git
   cd packmann
   ```
2. Installiere die Abhängigkeiten:
   ```bash
   pip install pygame
   ```

---

## 🔃 Spiel starten
1. Stelle sicher, dass sich alle benötigten Dateien (z. B. `Levels/` und `Konfiguration.txt`) im Projektordner befinden.
2. Führe das Hauptskript aus:
   ```bash
   python main.py
   ```
3. Navigiere durch das Hauptmenü und starte das Spiel.

---

## 🔐 Highscores
- Highscores werden in der Datei `highscores.txt` gespeichert.
- Beim Erreichen eines neuen Highscores wird der Spieler aufgefordert, seinen Namen einzugeben.
- Das Highscore-Menü zeigt die besten Ergebnisse an und bietet eine Option zum Löschen der Highscores.

---

## 🛠️ Fehlerbehandlung
- **Fehlende oder fehlerhafte Dateien:** Standardwerte werden verwendet oder es erfolgt ein sinnvoller Abbruch.
- **Ungültige Werte:** Automatische Anpassung an Standardwerte (z. B. für Kachelgröße oder Geschwindigkeiten).

---

## 🔗 Lizenz
Dieses Projekt ist unter der [MIT-Lizenz](LICENSE) lizenziert.

