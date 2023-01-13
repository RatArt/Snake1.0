from ftplib import FTP
from io import BytesIO
from tempfile import TemporaryFile

ftp = FTP('uvirt126.active24.cz', 'berryratar', 'xXTrolled159Xx')
ftp.cwd('www')

r = BytesIO()
temp = TemporaryFile()

ftp.retrbinary('RETR wp-config.php', r.write)
print(r.getvalue())