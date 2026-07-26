import sys
import json
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse

# Make sure we can import the src package
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sliding_puzzle import Puzzle, breadth_first_search, astar_search

# The directory to serve static files from
WEB_DIR = ROOT / "web"

class PuzzleHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def do_POST(self):
        if self.path == '/api/solve':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                start_state = tuple(data['start'])
                algorithm = data['algorithm']
                
                # Standard target state for 3x3
                target_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)
                
                # Create puzzle instance
                puzzle = Puzzle(start=start_state, target=target_state, size=3)
                
                # Solve based on algorithm
                if algorithm == 'bfs':
                    result = breadth_first_search(puzzle)
                elif algorithm == 'astar':
                    result = astar_search(puzzle)
                else:
                    raise ValueError(f"Unknown algorithm: {algorithm}")
                
                # Format response
                response_data = {
                    "found": result.found,
                    "expansions": result.expansions,
                    "max_nodes_in_memory": result.max_nodes_in_memory,
                    "max_frontier_size": result.max_frontier_size,
                    "elapsed_seconds": result.elapsed_seconds,
                    "path": result.path if result.found else [],
                    "moves": result.moves if result.found else []
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_resp = {"error": str(e)}
                self.wfile.write(json.dumps(error_resp).encode('utf-8'))
        else:
            # For any other POST, just return 404
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=PuzzleHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on http://localhost:{port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped.")

if __name__ == '__main__':
    run()
