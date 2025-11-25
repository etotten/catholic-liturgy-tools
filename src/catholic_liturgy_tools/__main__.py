"""Allow running the CLI as a module: python -m catholic_liturgy_tools"""

from catholic_liturgy_tools.cli import main
import sys

if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
