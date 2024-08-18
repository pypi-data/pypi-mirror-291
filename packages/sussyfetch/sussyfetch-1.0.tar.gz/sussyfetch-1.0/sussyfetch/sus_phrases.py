import random

sus_phrases = {
    1: [
        "Hmm... just a normal system, or is it?",
        "Everything seems fine... for now.",
        "Nothing unusual... I think.",
    ],
    5: [
        "The processor... it's *too* powerful.",
        "RAM is suspiciously high... are you hiding something?",
        "Your disk space... is someone tampering with it?",
        "You're looking kinda sus, not gonna lie.",
    ],
    10: [
        "Red alert! Impostor detected!",
        "This system is compromised! Call an emergency meeting!",
        "Your CPU is at 100%... why is it working so hard?",
        "Among Us has been found running in the background... do you dare check?",
    ],
}


def get_sus_info(sus_level):
    if sus_level <= 3:
        return random.choice(sus_phrases[1])
    elif sus_level <= 7:
        return random.choice(sus_phrases[5])
    else:
        return random.choice(sus_phrases[10])
