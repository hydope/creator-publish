"""creator-publish: official-API publishing + scheduling, shared by
ShortSmash, POVCut, and any creator tool that wants to post without
scraping or unofficial endpoints.

Extracted from ShortSmash (2026-10-19) into its own package so the
publishing layer has one home and every tool benefits from fixes.
"""

__version__ = "0.1.0"
__all__ = ["__version__"]
