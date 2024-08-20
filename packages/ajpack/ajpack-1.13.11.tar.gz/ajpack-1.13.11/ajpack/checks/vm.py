import subprocess
import re

def run_on_vm(additional_blacklist: list[str] = []) -> bool:
    """
    Checks if current script is running on a vm.
    
    :param additional_blacklists: Some additionional keywords for a vm from you side.
    :return: bool --> If running on vm
    """
    blacklist: list[str] = [
        "vm",
        "black",
        "box",
        "vbox",
        "sand",
        "virtual",
        "hypervisor",
        "emulator",
        "qemu",
        "kvm",
        "xen",
        "hyper-v",
        "parallels",
        "fusion",
    ]

    for item in additional_blacklist: blacklist.append(item)

    # Convert blacklist items to lowercase
    blacklist = [item.lower() for item in blacklist]

    # Run system information queries
    bios_output = subprocess.run(["wmic", "bios"], capture_output=True, text=True).stdout.lower()
    csproduct_output = subprocess.run(["wmic", "csproduct"], capture_output=True, text=True).stdout.lower()
    baseboard_output = subprocess.run(["wmic", "baseboard"], capture_output=True, text=True).stdout.lower()
    cpu_output = subprocess.run(["wmic", "cpu"], capture_output=True, text=True).stdout.lower()
    systeminfo_output = subprocess.run(["systeminfo"], capture_output=True, text=True).stdout.lower()

    # Check for keywords in output
    for item in blacklist:
        if re.search(r"\b" + re.escape(item) + r"\b", bios_output) or \
           re.search(r"\b" + re.escape(item) + r"\b", csproduct_output) or \
           re.search(r"\b" + re.escape(item) + r"\b", baseboard_output) or \
           re.search(r"\b" + re.escape(item) + r"\b", cpu_output) or \
           re.search(r"\b" + re.escape(item) + r"\b", systeminfo_output):
            return True

    # Additional checks
    if "vmware" in systeminfo_output or "virtualbox" in systeminfo_output:
        return True

    # Check for virtual network adapters
    network_adapters = subprocess.run(["wmic", "nic"], capture_output=True, text=True).stdout.lower()
    if "virtual" in network_adapters or "vmware" in network_adapters:
        return True

    return False