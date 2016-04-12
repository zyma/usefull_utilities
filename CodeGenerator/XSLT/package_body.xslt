<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" />
<xsl:template match="/">
  <html>
  <body>
<br/>
<pre>
create or replace PACKAGE BODY <xsl:value-of select="normalize-space(TABLE/TABLE_NAME)"/>_PKG AS

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
    )
    is
    begin
       <xsl:text>select SEQ_</xsl:text><xsl:value-of select="normalize-space(TABLE/TABLE_NAME)"/><xsl:text>.nextval </xsl:text>
<xsl:for-each select="TABLE/COLUMNS/COLUMN">
 <xsl:if test="IS_PK = 1">
        <xsl:text>
       into a</xsl:text> 
        <xsl:value-of select="normalize-space(COLUMN_NAME)"/>
   </xsl:if>
</xsl:for-each>
       from dual;
       
       insert into <xsl:value-of select="normalize-space(TABLE/TABLE_NAME)"/> (
<xsl:for-each select="TABLE/COLUMNS/COLUMN">
        <xsl:text>                </xsl:text>
        <xsl:value-of select="normalize-space(COLUMN_NAME)"/>
         <xsl:if test="position()!=last()">
                <xsl:text>,  
</xsl:text>
         </xsl:if>
</xsl:for-each>
       )
       values (
<xsl:for-each select="TABLE/COLUMNS/COLUMN">
        <xsl:text>                a</xsl:text>
        <xsl:value-of select="normalize-space(COLUMN_NAME)"/>
         <xsl:if test="position()!=last()">
                <xsl:text>,  
</xsl:text>
         </xsl:if>
</xsl:for-each>
       );
    end InsertItem;

   procedure UpdateItem (
<xsl:for-each select="TABLE/COLUMNS/COLUMN">
    <xsl:text>      a</xsl:text><xsl:value-of select="normalize-space(COLUMN_NAME)"/> 
    <xsl:text> IN </xsl:text>
    <xsl:value-of select="normalize-space(COLUMN_TYPE)"/>
    <xsl:if test="position()!=last()">
         <xsl:text>,  
</xsl:text>
    </xsl:if>
</xsl:for-each>
    )
    is
    begin
       update <xsl:value-of select="normalize-space(TABLE/TABLE_NAME)"/>
        <xsl:text>  
       set   </xsl:text>
<xsl:for-each select="TABLE/COLUMNS/COLUMN">
     <xsl:if test="IS_PK = 0">
        <xsl:text>
             </xsl:text> 
        <xsl:value-of select="normalize-space(COLUMN_NAME)"/>
        <xsl:text> = a</xsl:text> 
        <xsl:value-of select="normalize-space(COLUMN_NAME)"/>
        <xsl:if test="position()!=last()">
            <xsl:text>, </xsl:text> 
        </xsl:if>
   </xsl:if>
</xsl:for-each>

<xsl:for-each select="TABLE/COLUMNS/COLUMN">
 <xsl:if test="IS_PK = 1">
        <xsl:text>
        where </xsl:text> 
        <xsl:value-of select="normalize-space(COLUMN_NAME)"/>
        <xsl:text> = a</xsl:text> 
        <xsl:value-of select="normalize-space(COLUMN_NAME)"/>
        <xsl:text>; </xsl:text> 
   </xsl:if>
</xsl:for-each>
       
    end UpdateItem;

   procedure DeleteItem (
<xsl:for-each select="TABLE/COLUMNS/COLUMN">
 <xsl:if test="IS_PK = 1">
        <xsl:text>      a</xsl:text><xsl:value-of select="normalize-space(COLUMN_NAME)"/> 
             <xsl:text> IN </xsl:text>
        <xsl:value-of select="normalize-space(COLUMN_TYPE)"/>
   </xsl:if>
</xsl:for-each>
    )
    is
    begin
        delete from <xsl:value-of select="normalize-space(TABLE/TABLE_NAME)"/>
<xsl:for-each select="TABLE/COLUMNS/COLUMN">
 <xsl:if test="IS_PK = 1">
        <xsl:text>
        where </xsl:text> 
        <xsl:value-of select="normalize-space(COLUMN_NAME)"/>
        <xsl:text> = a</xsl:text> 
        <xsl:value-of select="normalize-space(COLUMN_NAME)"/>
        <xsl:text>; </xsl:text> 
   </xsl:if>
</xsl:for-each>
        
    end DeleteItem;
    
END <xsl:value-of select="normalize-space(TABLE/TABLE_NAME)"/>_PKG;
/
</pre>
<br/>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
