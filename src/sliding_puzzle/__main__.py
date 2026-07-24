"""<summary>
Package execution entry point.
</summary>

<remarks>
This module supports running the installed package with
<c>python3 -m sliding_puzzle</c>. It delegates all real work to
<c>sliding_puzzle.cli.main</c>.
</remarks>
"""

from sliding_puzzle.cli import main


# <summary>
# Execute the CLI only when the module is run as the program entry point.
# </summary>
if __name__ == "__main__":
    raise SystemExit(main())
