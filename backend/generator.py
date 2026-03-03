def group_by_rows(components, threshold=40):
    rows = []
    components = sorted(components, key=lambda c: (c['y'], c['x']))

    for comp in components:
        placed = False
        for row in rows:
            if abs(row[0]['y'] - comp['y']) < threshold:
                row.append(comp)
                placed = True
                break
        if not placed:
            rows.append([comp])

    return rows


def generate_html(components):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Generated UI</title>
        <style>
            body {
                font-family: 'Segoe UI', Arial;
                background: #f4f6f8;
                padding: 30px;
            }
            .container {
                max-width: 900px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            .row {
                display: flex;
                gap: 15px;
                margin-bottom: 20px;
            }
            button {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                background: #2563eb;
                color: white;
                cursor: pointer;
            }
            input {
                padding: 8px;
                border-radius: 6px;
                border: 1px solid #ccc;
                flex: 1;
            }
            .card {
                border: 1px solid #ddd;
                padding: 20px;
                border-radius: 8px;
                background: #fafafa;
            }
        </style>
    </head>
    <body>
    <div class="container">
    """

    rows = group_by_rows(components)

    for row in rows:
        html += "<div class='row'>"

        for comp in sorted(row, key=lambda c: c['x']):
            t = comp["type"]

            if t == "button":
                html += "<button>Button</button>"

            elif t == "input":
                html += """
                <div style="display:flex; flex-direction:column; flex:1;">
                    <label style="font-size:14px; margin-bottom:5px;">Input</label>
                    <input type='text' placeholder='Enter value'>
                </div>
                """

            elif t == "checkbox":
                html += "<label><input type='checkbox'> Option</label>"

            elif t == "container":
                html += "<div class='card'>Container</div>"

            else:
                html += "<div class='card'>Image</div>"

        html += "</div>"

    html += """
    </div>
    </body>
    </html>
    """

    return html