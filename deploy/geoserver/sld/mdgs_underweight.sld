<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc"
  xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd">
  <NamedLayer>
    <Name>Underweight</Name>
    <UserStyle>
      <Name>underweigh</Name>
      <Title>Unerweight</Title>
      <Abstract>A style emphasizing underweight statistics</Abstract>
      <FeatureTypeStyle>
        <Rule>
          <Name>Less than 4</Name>
          <ogc:Filter>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>underweigh</ogc:PropertyName>
           <ogc:Literal>4</ogc:Literal>
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
          <Name>4 to 6.5</Name>
          <ogc:Filter>
          <ogc:And>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>underweigh</ogc:PropertyName>
             <ogc:Literal>4</ogc:Literal>
           </ogc:PropertyIsGreaterThanOrEqualTo>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>underweigh</ogc:PropertyName>
           <ogc:Literal>6.5</ogc:Literal>
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
          <Name>6.5 to 8.5</Name>
          <ogc:Filter>
          <ogc:And>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>underweigh</ogc:PropertyName>
             <ogc:Literal>6.5</ogc:Literal>
           </ogc:PropertyIsGreaterThanOrEqualTo>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>underweigh</ogc:PropertyName>
           <ogc:Literal>8.5</ogc:Literal>
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
          <Name>8.5 to 10.5</Name>
          <ogc:Filter>
          <ogc:And>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>underweigh</ogc:PropertyName>
             <ogc:Literal>8.5</ogc:Literal>
           </ogc:PropertyIsGreaterThanOrEqualTo>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>underweigh</ogc:PropertyName>
           <ogc:Literal>10.5</ogc:Literal>
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
          <Name>10.5 to 15</Name>
          <ogc:Filter>
          <ogc:And>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>underweigh</ogc:PropertyName>
             <ogc:Literal>10.5</ogc:Literal>
           </ogc:PropertyIsGreaterThanOrEqualTo>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>underweigh</ogc:PropertyName>
           <ogc:Literal>15</ogc:Literal>
          </ogc:PropertyIsLessThan>
          </ogc:And>
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

