<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" />
<xsl:template match="/">
  <html>
  <body>
<pre>
  CREATE SEQUENCE SEQ_<xsl:value-of select="normalize-space(TABLE/TABLE_NAME)"/> MINVALUE 1 MAXVALUE 9999999999999999999999999999 
  INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE;
</pre>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
