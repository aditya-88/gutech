import pandas as pd
import smtplib
from email.mime.text import MIMEText
import time
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path, callback):
        self.file_path = file_path
        self.callback = callback

    def on_modified(self, event):
        if event.src_path == self.file_path:
            print(f"{self.file_path} has been modified")
            self.callback()

def process_samples(df):
    origin_failures = {}
    origin_counts = {}
    
    for index, row in df.iterrows():
        if len(row) < 6:
            print(f"Warning: Malformed line detected at index {index}: {row}")
            continue
        
        origin = row.iloc[0]
        covered_bases_value = row.iloc[4]
        
        try:
            if isinstance(covered_bases_value, str):
                covered_bases = float(covered_bases_value.strip('%'))
            else:
                covered_bases = float(covered_bases_value)
        except ValueError:
            print(f"Warning: Invalid covered bases value at index {index}: {covered_bases_value}")
            continue
        
        quality_flag = row.iloc[5]
        
        if origin not in origin_counts:
            origin_counts[origin] = 0
            origin_failures[origin] = 0
        
        origin_counts[origin] += 1
        
        if covered_bases < 95 or quality_flag == 'FALSE':
            origin_failures[origin] += 1
    
    return origin_failures, origin_counts

def calculate_failure_rates(origin_failures, origin_counts):
    failure_rates = {}
    for origin in origin_failures:
        failure_rate = (origin_failures[origin] / origin_counts[origin]) * 100
        failure_rates[origin] = failure_rate
    return failure_rates

def generate_warnings(failure_rates):
    warnings = []
    for origin, rate in failure_rates.items():
        if rate > 10:
            warnings.append(f"Warning: {origin} has {rate:.2f}% failed samples.")
    return warnings

def notify_user(warnings):
    for warning in warnings:
        print(warning)
    # Optionally, send an email notification
    # send_email(warnings)

def send_email(warnings):
    msg = MIMEText("\n".join(warnings))
    msg['Subject'] = 'Quality Metrics Warning'
    msg['From'] = 'your_email@example.com' # Change this to your email address
    msg['To'] = 'recipient@example.com' # Change this to the recipient's email address
    print("Sending email...")
    with smtplib.SMTP('localhost') as server: # Email server should be setup on the localhost/ use an email hosting service
        server.send_message(msg)

def process_file(file_path):
    samples = pd.read_csv(file_path, delimiter=',')
    origin_failures, origin_counts = process_samples(samples)
    failure_rates = calculate_failure_rates(origin_failures, origin_counts)
    warnings = generate_warnings(failure_rates)
    notify_user(warnings)

def main():
    parser = argparse.ArgumentParser(description='Process quality metrics file.')
    parser.add_argument('--file', type=str, default='data/samples.txt', help='Path to the quality metrics file')
    args = parser.parse_args()

    file_path = args.file
    event_handler = FileChangeHandler(file_path, lambda: process_file(file_path))
    observer = Observer()
    observer.schedule(event_handler, path=file_path.rsplit('/', 1)[0], recursive=False)
    observer.start()
    print(f"Watching for changes in {file_path}...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()