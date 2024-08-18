import platform
import psutil
from rich.console import Console
from rich.table import Table
import random

# Expanded list of sus phrases with brainrot phrases
sus_phrases_os = {
    "Windows": [
        "You're on Windows... someone's definitely watching",
        "Windows detected. The most sus of all operating systems",
        "Windows? Must be the Impostor's favorite",
        "Only in Ohio could you be using Windows",
        "Skibidi gyatt rizz on a Windows machine",
        "Windows OS: Goated with the sauce, but sussy",
        "Literally hitting the griddy on Windows right now",
    ],
    "Linux": [
        "Linux? Are you some kind of hacker?",
        "Linux detected. Are you plotting something?",
        "Linux user... you seem skilled, but are you trustworthy?",
        "Sigma grindset detected on Linux",
        "Are you coding or just gooning in the terminal?",
        "Linux OS: Based, but also cringe?",
        "This Linux machine screams 'I love lean'",
    ],
    "Darwin": [
        "macOS detected. Is this the Impostor's machine?",
        "Using a Mac, huh? I bet you're a crewmate... or are you?",
        "macOS... stylish, but it hides secrets",
        "Bro really thinks he's Carti using macOS",
        "Livvy Dunne rizzing up Baby Gronk on a MacBook",
        "macOS: Delulu but make it chic",
        "Quirked up white boy busting it down on macOS",
    ],
    "Other": [
        "{os_name}... kinda sus",
        "Unknown OS detected. Definitely suspicious",
        "This operating system is uncharted territory... proceed with caution",
        "Literally hitting the gritty on {os_name}",
        "This OS is bussing... or is it?",
        "{os_name} OS? That's some uncanny energy",
        "{os_name} OS... feeling a bit zesty today",
    ],
}

sus_phrases_cpu = [
    "Your CPU's slacking off... or pretending to",
    "Seems normal, but keep an eye on it",
    "Your CPU's working hard... but for whom?",
    "CPU at max... emergency meeting called!",
    "This CPU is too quiet... what's it up to?",
    "High CPU usage... is it downloading something sus?",
    "Bro really thinks he's Carti with that CPU load",
    "CPU rizzing up all the processes at once",
    "Your CPU is goated with the sauce, but watch out",
    "CPU acting like it's hitting the gym. We go CPU!",
]

sus_phrases_memory = [
    "Plenty of RAM... for now",
    "A little sus, but not enough to accuse",
    "RAM's almost full... is it hiding something?",
    "Your memory seems fine... but is it?",
    "Low memory usage... or is it hiding something in the background?",
    "RAM usage is spiking... sussy amogus imposter?",
    "Memory acting zesty today, not gonna lie",
    "Is that Grimace Shake in your RAM?",
    "Your RAM is literally bussing right now",
    "Memory's like 'hit or miss, I guess they never miss, huh?'",
]

sus_phrases_disk = [
    "Lots of space... too much, maybe?",
    "Your disk's getting crowded... what's going on?",
    "Disk almost full... someone might be storing something they shouldn't",
    "Is that a secret file hidden on your disk?",
    "This disk has seen some things... suspicious things",
    "Disk usage rising... is there an Impostor among us?",
    "Whopper whopper whopper whopper, this disk space is gone forever",
    "Disk acting like it's in the backrooms",
    "This disk space is giving me uncanny vibes",
    "Your disk is looking thicc with those files",
]

platform_info_phrases = {
    "Machine": [
        "{machine} machine detected... highly sus",
        "Are you plotting something with this {machine}?",
        "Type {machine}. Hope it's not compromised",
        "Your {machine} looks clean... for now",
        "Is this {machine} secretly rizzing up the network?",
        "{machine}: looking kinda sussy, ngl",
        "{machine} is built different. Just like Ohio",
    ],
    "Processor": [
        "The {processor} processor is powerful... maybe too powerful",
        "Hmmm... {processor}. Keep an eye on this one",
        "{processor} processor detected. Could be sus",
        "Your {processor} processor out here acting like John Pork",
        "This {processor} processor? Giving major Chad energy",
        "Damn, {processor} processor be built for the grindset fr",
    ],
}


def get_platform_info_phrase(info_type, value):
    return random.choice(platform_info_phrases[info_type]).format(
        **{info_type.lower(): value}
    )


def get_sus_description_os(os_name):
    if os_name in sus_phrases_os:
        return random.choice(sus_phrases_os[os_name])
    else:
        return random.choice(sus_phrases_os["Other"]).format(os_name=os_name)


def get_sus_description_cpu(cpu_usage):
    if cpu_usage < 20:
        return random.choice(sus_phrases_cpu[:2])
    elif cpu_usage < 60:
        return random.choice(sus_phrases_cpu[2:4])
    else:
        return random.choice(sus_phrases_cpu[4:])


def get_sus_description_memory(used_mem_percentage):
    if used_mem_percentage < 40:
        return random.choice(sus_phrases_memory[:2])
    elif used_mem_percentage < 70:
        return random.choice(sus_phrases_memory[2:4])
    else:
        return random.choice(sus_phrases_memory[4:])


def get_sus_description_disk(used_disk_percentage):
    if used_disk_percentage < 40:
        return random.choice(sus_phrases_disk[:2])
    elif used_disk_percentage < 70:
        return random.choice(sus_phrases_disk[2:4])
    else:
        return random.choice(sus_phrases_disk[4:])


def get_system_info():
    console = Console()
    table = Table(show_header=True, header_style="bold cyan")

    # Adding columns
    table.add_column("Component", style="dim", width=30)
    table.add_column("Details")

    # OS Info
    os_name = platform.system()
    table.add_row("Operating System", get_sus_description_os(os_name))
    table.add_row("Machine", get_platform_info_phrase("Machine", platform.machine()))
    table.add_row(
        "Processor", get_platform_info_phrase("Processor", platform.processor().upper())
    )

    # Memory Info
    mem = psutil.virtual_memory()
    used_mem_percentage = mem.percent
    table.add_row("Total Memory", f"{mem.total / (1024 ** 3):.2f} GB")
    table.add_row("Used Memory", get_sus_description_memory(used_mem_percentage))
    table.add_row("Available Memory", f"{mem.available / (1024 ** 3):.2f} GB")

    # Disk Info
    disk = psutil.disk_usage("/")
    used_disk_percentage = disk.percent
    table.add_row("Total Disk Space", f"{disk.total / (1024 ** 3):.2f} GB")
    table.add_row("Used Disk Space", get_sus_description_disk(used_disk_percentage))
    table.add_row("Free Disk Space", f"{disk.free / (1024 ** 3):.2f} GB")

    # CPU Info
    cpu_usage = psutil.cpu_percent(interval=1)
    table.add_row("CPU Usage", get_sus_description_cpu(cpu_usage))

    console.print(table)
