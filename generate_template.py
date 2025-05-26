def generate_html(title="Untitled Page"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title} | Respirework</title>
    <meta name="description" content="Auto-generated content for {title}">
    <meta name="robots" content="index, follow">
</head>
<body>
    <main>
        <h1>{title}</h1>
        <p>This page has been automatically generated to resolve a broken link.</p>
    </main>
</body>
</html>"""
