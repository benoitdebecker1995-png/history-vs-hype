"""
History vs Hype tools package.

This package contains all CLI tools and modules for content production,
YouTube analytics, keyword discovery, and intelligence tracking.
"""

import logging

# Add NullHandler to prevent "No handlers could be found for logger 'tools'"
# warnings when tools modules are imported without setup_logging() being called.
# This is the recommended Python pattern for library packages.
logging.getLogger("tools").addHandler(logging.NullHandler())
