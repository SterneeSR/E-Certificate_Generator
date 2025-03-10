import os
import csv
import cv2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import re

# Lists to store data
names = []
email_addrs = []
institutes = []
events = []
failed_emails = []
failed_emails_lock = Lock()

# Regex for validating email addresses
email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

# Function to validate and load data from CSV
def preprocess_data():
    with open("elist.csv") as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            name = row.get("NAME", "").strip()
            email = row.get("E-MAIL ID", "").strip()
            institute = row.get("INSTITUTION", "").strip()
            event = row.get("COMPETITION", "").strip()

            # Validate email
            if not email or not email_regex.match(email):
                print(f"Invalid or empty email skipped: {name}, {email}")
                continue

            names.append(name)
            email_addrs.append(email)
            institutes.append(institute)
            events.append(event)

# Function to clean up the output folder
def purge_output_folder():
    output_folder = "Generated-Certificates"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        for file in os.listdir(output_folder):
            os.remove(os.path.join(output_folder, file))

# Function to generate certificates
def generate_certificate(name, institute, event):
    try:
        template = cv2.imread("CERTIFICATE.png")
        cv2.putText(template, name, (664, 714), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(template, institute, (394, 774), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(template, event, (593, 825), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        output_path = f"Generated-Certificates/{name}.png"
        cv2.imwrite(output_path, template)
        return output_path
    except Exception as e:
        print(f"Error generating certificate for {name}: {e}")
        return None

# Function to send an email with the certificate
def send_email(name, email, institute, event, certificate_path):
    if not certificate_path:
        print(f"Skipping email for {name} due to missing certificate.")
        return

    #sender_email = "rsmartrcas.events@gmail.com"
    #sender_password = "lbcy vbxp czpq bzgt"
    sender_email = "rcasrsmart.events@gmail.com"
    sender_password = "nioa frts ngqq xzxi"
    subject = "Your Participation Certificate for Kalomix-25" 


    # Load HTML template
    with open("template.html", "r") as file:
        html_content = file.read().replace("[Name]", name).replace("[Competition Name]", event)

    # Create email
    msg = MIMEMultipart()
    msg["From"] = sender_email  
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    # Attach background image 
    try:
        with open("background.png", "rb") as bg_file:
            bg_image = MIMEImage(bg_file.read())
            bg_image.add_header("Content-ID", "<email_background>")
            msg.attach(bg_image)
    except FileNotFoundError:
        print("Background image not found. Skipping attachment.")

    # Attach Instagram logo
    try:
        with open("instagram_logo.png", "rb") as insta_file:
            insta_image = MIMEImage(insta_file.read())
            insta_image.add_header("Content-ID", "<instagram_logo>")
            msg.attach(insta_image)
    except FileNotFoundError:
        print("Instagram logo not found. Skipping attachment.")

    # Attach certificate
    try:
        with open(certificate_path, "rb") as cert_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(cert_file.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(certificate_path)}")
            msg.attach(part)
    except Exception as e:
        print(f"Error attaching certificate for {name}: {e}")
        return

    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Email sent to {email}")
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")
        with failed_emails_lock:
            failed_emails.append((name, email))

# Process recipient
def process_recipient(name, email, institute, event):
    certificate_path = generate_certificate(name, institute, event)
    send_email(name, email, institute, event, certificate_path)

# Main function
def main():
    purge_output_folder()
    preprocess_data()

    with ThreadPoolExecutor(max_workers=5) as executor:
        for name, email, inst, event in zip(names, email_addrs, institutes, events):
            executor.submit(process_recipient, name, email, inst, event)

    # Save failed emails
    if failed_emails:
        with open("failed_emails.txt", "w") as file:
            for name, email in failed_emails:
                file.write(f"{name},{email}\n")
        print("Failed emails saved to 'failed_emails.txt'.")

if __name__ == "__main__":
    main()
