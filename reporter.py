import webbrowser
import os
import datetime

class Reporter:
    def generate_html(self, removed_count, space_saved, backup_loc, old_score, new_score):
        """Creates an HTML report and opens it."""
        
        # Convert bytes to MB
        space_mb = round(space_saved / (1024 * 1024), 2)
        
        html_content = f"""
        <html>
        <head>
            <title>Privacy Cleanup Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f9; }}
                .container {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; }}
                .score {{ font-size: 20px; font-weight: bold; color: #27ae60; }}
                .stat {{ margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Digital Footprint Shrinker - Report</h1>
                <p><strong>Date:</strong> {datetime.datetime.now()}</p>
                <hr>
                <div class="stat">Files Cleaned: <strong>{removed_count}</strong></div>
                <div class="stat">Space Recovered: <strong>{space_mb} MB</strong></div>
                <div class="stat">Backup Location: <strong>{backup_loc}</strong></div>
                <hr>
                <p class="score">Privacy Score: {old_score}/100 &rarr; {new_score}/100</p>
                <p><em>Your digital footprint has been successfully reduced.</em></p>
            </div>
        </body>
        </html>
        """
        
        filename = "cleanup_report.html"
        with open(filename, "w") as f:
            f.write(html_content)
            
        # Automatically open the report in browser
        webbrowser.open('file://' + os.path.realpath(filename))