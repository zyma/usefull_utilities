<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" indent="no"/>
   <xsl:preserve-space elements="*"/>
<xsl:template match="/" xml:space="default">
  <html>
  <body>
<pre>

CREATE OR REPLACE PACKAGE <xsl:value-of select="normalize-space(TABLE/TABLE_NAME)"/>_PKG AS

   PROCEDURE InsertItem ( 
<xsl:for-each select="TABLE/COLUMNS/COLUMN">
    <xsl:text>      a</xsl:text><xsl:value-of select="normalize-space(COLUMN_NAME)"/> 
    <xsl:if test="IS_PK = 1">
        <xsl:text> OUT </xsl:text>
    </xsl:if>
    <xsl:if test="IS_PK = 0">
        <xsl:text> IN </xsl:text>
    </xsl:if>
    <xsl:value-of select="normalize-space(COLUMN_TYPE)"/>
    <xsl:if test="position()!=last()">
         <xsl:text>,  
</xsl:text>
    </xsl:if>
</xsl:for-each>
    );

   PROCEDURE UpdateItem ( 
<xsl:for-each select="TABLE/COLUMNS/COLUMN">
    <xsl:text>      a</xsl:text><xsl:value-of select="normalize-space(COLUMN_NAME)"/> 
    <xsl:text> IN </xsl:text>
    <xsl:value-of select="normalize-space(COLUMN_TYPE)"/>
    <xsl:if test="position()!=last()">
         <xsl:text>,  
</xsl:text>
    </xsl:if>
</xsl:for-each>
    );

   PROCEDURE DeleteItem (
<xsl:for-each select="TABLE/COLUMNS/COLUMN">
 <xsl:if test="IS_PK = 1">
        <xsl:text>      a</xsl:text><xsl:value-of select="normalize-space(COLUMN_NAME)"/> 
             <xsl:text> IN </xsl:text>
        <xsl:value-of select="normalize-space(COLUMN_TYPE)"/>
   </xsl:if>
</xsl:for-each>
    );
    
END <xsl:value-of select="normalize-space(TABLE/TABLE_NAME)"/>_PKG;
/
</pre>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
