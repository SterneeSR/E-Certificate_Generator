# Automatic E-Certificate Distribution Project:

This project automates the generation and distribution of e-certificates for participants of certain events. It reads participant details from a CSV file, generates personalized certificates, and sends them via email.

## Features
- Reads participant details (name, email, institution, competition) from a CSV file.
- Generates certificates using a pre-designed template.
- Sends certificates as email attachments.
- Handles errors gracefully, including saving failed email attempts to a log file.
- Allows parallel processing to handle multiple participants efficiently.

---

## Prerequisites

1. Python 3.8 or higher
2. Required Python libraries (install using `pip install -r requirements.txt`):
   - `opencv-python`
   - `smtplib`
   - `email`
   - `concurrent.futures`

3. Ensure the following files are present in the project directory:
   - `CERTIFICATE.png`: The certificate template.
   - `elist.csv`: The CSV file containing participant details.
   - `template.html`: The email HTML template.
   - `background.png`: Background image for the email.
   - `instagram_logo.png`: Instagram logo to include in the email.

---

## Folder Structure

```
project-directory/
├── Generated-Certificates/       # Folder for generated certificates
├── elist.csv                     # Input CSV with participant details
├── CERTIFICATE.png               # Certificate template
├── template.html                 # HTML email template
├── background.png                # Background image for email
├── instagram_logo.png            # Instagram logo for email
├── main.py                       # Main Python script
├── failed_emails.txt             # Log file for failed email attempts
├── README.md                     # This README file
├── requirements.txt			   # Required Python Libraries
```

---

## How to Use

### 1. Prepare the Input CSV
The `elist.csv` file should have the following columns:
- `NAME`: Name of the participant
- `E-MAIL ID`: Participant's email address
- `INSTITUTION`: Name of the institution
- `COMPETITION`: Competition name

Ensure the columns are properly formatted and there are no empty rows.

### 2. Configure Email Credentials
In the `main.py` file, update the email credentials for the sender email account:
```python
sender_email = "your_email@gmail.com"
sender_password = "your_email_password"
```
Make sure the email account has "Allow less secure apps" enabled, or use an app-specific password.

### 3. Run the Script
Execute the script:
```bash
python main.py
```

### 4. Check Outputs
- Generated certificates will be saved in the `Generated-Certificates/` folder.
- Emails will be sent to the participants.
- Any failed emails will be logged in `failed_emails.txt`.

---

## Error Handling
- Invalid Emails: Skipped during processing and logged in the console.
- Failed Emails: Saved to `failed_emails.txt` for later review.
- Missing Files: Ensure all required files (template, images) are in place before running the script.

---

## Notes
- The script uses multithreading for faster processing.
- Ensure your email account has sufficient daily sending limits.
- Double-check the output directory and log files for any anomalies.

---

## Credits
This project was developed for automating the distribution of Kalomix-25 participation certificates. Special thanks to the Kalomix team for their efforts and support!

---

## License
This project is open-source and free to use for non-commercial purposes.
