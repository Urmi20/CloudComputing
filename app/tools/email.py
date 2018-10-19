import smtplib


class Email:

    def __init__(self, server, port, account, password):
        """
        :param server: ex: smtp.gmail.com
        :param port: ex: 587
        :param account: ex: ece1779.project.fall.2018
        :param password: ex: 123aBc! (aSd123qWe456zxc)
        """

        self.server = smtplib.SMTP(server + ":" + str(port))
        self.server.starttls()
        self.server.login(account, password)


    def __del__(self):
        self.server.quit()

    def send(self, sender, to, subject, message):
        header = 'From: %s \n' % sender
        header += 'To: %s \n' % to
        header += 'Cc: \n'
        header += 'Subject: %s \n\n' % subject
        message = header + message

        self.server.sendmail(sender, to, message)
