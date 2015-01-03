#!/bin/env python
from ledgerdashboard import app
from ledgerdashboard import settings

app.run(debug=settings.DEBUG, port=settings.PORT)
