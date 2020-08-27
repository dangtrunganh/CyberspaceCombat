

import os
print(os.path.abspath(os.path.dirname(__file__)))
print(os.path.dirname(__file__))
print(os.pardir)

print(os.path.join(os.path.dirname(__file__), 'static', 'upload_file'))
