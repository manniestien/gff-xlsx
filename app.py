from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import os
from gff_to_xlsx_converter import gff_to_xlsx  # Assuming this contains your conversion logic
import time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file.filename == "":
            return redirect(url_for("index"))

        # Save the uploaded file
        gff_file_path = os.path.join("uploads", file.filename)
        file.save(gff_file_path)

        # Process the file
        output_xlsx_path = os.path.join("uploads", "output.xlsx")
        gff_to_xlsx(gff_file_path, output_xlsx_path)

        # Trigger download
        return send_file(output_xlsx_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
