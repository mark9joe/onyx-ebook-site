<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:html="http://www.w3.org/TR/REC-html40"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>

  <xsl:template match="/">
    <html>
      <head>
        <title>Respirework Sitemap</title>
        <style type="text/css">
          body { font-family: Arial, sans-serif; background: #f9f9f9; color: #333; padding: 2rem; }
          h1 { color: #2c3e50; }
          ul { list-style-type: none; padding-left: 0; }
          li { margin-bottom: 10px; }
          a { color: #1e88e5; text-decoration: none; }
          a:hover { text-decoration: underline; }
        </style>
      </head>
      <body>
        <h1>Respirework Sitemap</h1>
        <ul>
          <xsl:for-each select="urlset/url">
            <li>
              <a href="{loc}">
                <xsl:value-of select="loc"/>
              </a>
              (<xsl:value-of select="changefreq"/>)
            </li>
          </xsl:for-each>
        </ul>
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
