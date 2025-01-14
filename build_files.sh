<<<<<<< HEAD
# build_files.sh
pip install -r requirements.txt
python3 manage.py collectstatic
=======
#!/bin/bash

# Install dependencies
pip3 install -r requirements.txt



# Collect static files
python3 manage.py collectstatic --noinput
>>>>>>> e95ac5bda40ba9bbf40eedab5b0e9916a34a8717
