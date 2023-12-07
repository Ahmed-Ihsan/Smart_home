import psutil
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def get_cpu_info():
    cpu_info = {
        "CPU Count": psutil.cpu_count(logical=False),
        "Logical CPU Count": psutil.cpu_count(logical=True),
        "CPU Frequency (GHz)": round(psutil.cpu_freq().current / 1000, 2),
    }
    return cpu_info

def get_memory_info():
    memory = psutil.virtual_memory()
    memory_info = {
        "Total Memory (GB)": round(memory.total / (1024 ** 3), 2),
        "Available Memory (GB)": round(memory.available / (1024 ** 3), 2),
        "Used Memory (GB)": round(memory.used / (1024 ** 3), 2),
        "Memory Usage Percentage": memory.percent,
    }
    return memory_info

def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_info = {}
    
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_info[partition.device] = {
            "Total Size (GB)": round(usage.total / (1024 ** 3), 2),
            "Used Space (GB)": round(usage.used / (1024 ** 3), 2),
            "Free Space (GB)": round(usage.free / (1024 ** 3), 2),
            "Usage Percentage": usage.percent,
        }
    return disk_info

def plot_cpu_info(cpu_info):
    labels = cpu_info.keys()
    values = cpu_info.values()
    
    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color='skyblue')
    plt.title('CPU Information')
    plt.xlabel('Metric')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.show()

def plot_memory_info(memory_info):
    labels = memory_info.keys()
    values = memory_info.values()
    
    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color='lightgreen')
    plt.title('Memory Information')
    plt.xlabel('Metric')
    plt.ylabel('Value (GB / %)')
    plt.xticks(rotation=45)
    plt.show()

def plot_disk_info(disk_info):
    devices = list(disk_info.keys())
    usage_percentages = [info["Usage Percentage"] for info in disk_info.values()]
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=devices, y=usage_percentages, palette="Blues_d")
    plt.title('Disk Usage Information')
    plt.xlabel('Device')
    plt.ylabel('Usage Percentage (%)')
    plt.xticks(rotation=45)
    plt.show()

def main():
    print("System Hardware Information:")
    print("-----------------------------")
    
    cpu_info = get_cpu_info()
    print("\nCPU Information:")
    for key, value in cpu_info.items():
        print(f"{key}: {value}")
    plot_cpu_info(cpu_info)
    
    memory_info = get_memory_info()
    print("\nMemory Information:")
    for key, value in memory_info.items():
        print(f"{key}: {value}")
    plot_memory_info(memory_info)
    
    disk_info = get_disk_info()
    print("\nDisk Information:")
    for device, info in disk_info.items():
        print(f"Device: {device}")
        for key, value in info.items():
            print(f"{key}: {value}")
        print("-" * 30)
    plot_disk_info(disk_info)

if __name__ == "__main__":
    main()
