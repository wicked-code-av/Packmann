def schriftarten(schrift):
    schriften = {
        "klein" : pygame.font.Font(None, 60),
        "mittel" : pygame.font.Font(None, 40),
        "gross" : pygame.font.Font(None, 30),
    }
    return schriften.get(schrift)


schriftarten("gross")
schriftarten("mittel")
schriftarten("klein")