"""<summary>
Repository-root launcher for the sliding puzzle solver.
</summary>

<remarks>
This file makes <c>python3 main.py</c> work without installing the package. It
adds the local <c>src/</c> directory to <c>sys.path</c>, imports the real CLI
entry point, and exits with the CLI return code.
</remarks>
"""

from __future__ import annotations

import sys
from pathlib import Path


# <summary>
# Absolute path to the repository root, computed from this file's location.
# </summary>
ROOT = Path(__file__).resolve().parent

# <summary>
# Absolute path to the local source directory that contains the package.
# </summary>
SRC = ROOT / "src"

# <summary>
# Make the package importable when the project has not been installed.
# </summary>
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sliding_puzzle.cli import main


# <summary>
# Execute the CLI only when this file is run as a script.
# </summary>
if __name__ == "__main__":
    raise SystemExit(main())
