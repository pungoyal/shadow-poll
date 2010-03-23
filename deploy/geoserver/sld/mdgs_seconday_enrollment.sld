<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc"
  xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd">
  <NamedLayer>
    <Name>Secondary Enrollment</Name>
    <UserStyle>
      <Name>secondary enrollment</Name>
      <Title>Secondary Enrollement</Title>
      <Abstract>A style emphasizing enrollment in Secondary School</Abstract>
      <FeatureTypeStyle>
        <Rule>
          <Name>Less than 10</Name>
          <ogc:Filter>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>enrollmen3</ogc:PropertyName>
           <ogc:Literal>10</ogc:Literal>
          </ogc:PropertyIsLessThan>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#808080</CssParameter>
              <CssParameter name="fill-opacity">1</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#ffffff</CssParameter>
              <CssParameter name="stroke-width">0.5</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>10 to 15</Name>
          <ogc:Filter>
          <ogc:And>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>enrollmen3</ogc:PropertyName>
             <ogc:Literal>10</ogc:Literal>
           </ogc:PropertyIsGreaterThanOrEqualTo>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>enrollmen3</ogc:PropertyName>
           <ogc:Literal>15</ogc:Literal>
          </ogc:PropertyIsLessThan>
          </ogc:And>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#4d4d4d</CssParameter>
              <CssParameter name="fill-opacity">1</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#ffffff</CssParameter>
              <CssParameter name="stroke-width">0.5</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
       <Rule>
          <Name>15 to 20</Name>
          <ogc:Filter>
          <ogc:And>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>enrollmen3</ogc:PropertyName>
             <ogc:Literal>15</ogc:Literal>
           </ogc:PropertyIsGreaterThanOrEqualTo>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>enrollmen3</ogc:PropertyName>
           <ogc:Literal>20</ogc:Literal>
          </ogc:PropertyIsLessThan>
          </ogc:And>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#333333</CssParameter>
              <CssParameter name="fill-opacity">1</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#ffffff</CssParameter>
              <CssParameter name="stroke-width">0.5</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>20 to 25</Name>
          <ogc:Filter>
          <ogc:And>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>enrollmen3</ogc:PropertyName>
             <ogc:Literal>20</ogc:Literal>
           </ogc:PropertyIsGreaterThanOrEqualTo>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>enrollmen3</ogc:PropertyName>
           <ogc:Literal>25</ogc:Literal>
          </ogc:PropertyIsLessThan>
          </ogc:And>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#262626</CssParameter>
              <CssParameter name="fill-opacity">1</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#ffffff</CssParameter>
              <CssParameter name="stroke-width">0.5</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Greater than 25</Name>
          <ogc:Filter>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>enrollmen3</ogc:PropertyName>
             <ogc:Literal>25</ogc:Literal>
           </ogc:PropertyIsGreaterThanOrEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#0d0d0d</CssParameter>
              <CssParameter name="fill-opacity">1</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#ffffff</CssParameter>
              <CssParameter name="stroke-width">0.5</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>

