# HTML Mailer

This library simplifies sending HTML formated emails. 
Currently there is one HTML format. Planning for future releases to customize format.

To use, simply pip install.

Example:
```python
import os
from py_html_email import Emailer

emailer = Emailer(sender_email='example@microsoft.com',
                  sender_password=os.getenv('email_password'),
                  smtp_server='office',
                  )
emailer.send_email(to='to@address.com',
                   subject='Email Sent with HTML Mailer',
                   msg_header='Alert!!',
                   msg_title='There was an issue',
                   msg_body='Details on the issue are related to process x'
                   )
```