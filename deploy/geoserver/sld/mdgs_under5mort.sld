<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc"
  xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd">
  <NamedLayer>
    <Name>Under5mort</Name>
    <UserStyle>
      <Name>under5mort</Name>
      <Title>Poverty</Title>
      <Abstract>A style emphasizing under 5 mortality statistics</Abstract>
      <FeatureTypeStyle>
        <Rule>
          <Name>Less than 31</Name>
          <ogc:Filter>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>under5mort</ogc:PropertyName>
           <ogc:Literal>31</ogc:Literal>
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
          <Name>31 to 37.4</Name>
          <ogc:Filter>
          <ogc:And>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>under5mort</ogc:PropertyName>
             <ogc:Literal>31</ogc:Literal>
           </ogc:PropertyIsGreaterThanOrEqualTo>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>under5mort</ogc:PropertyName>
           <ogc:Literal>37.4</ogc:Literal>
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
          <Name>37.4 to 46.3</Name>
          <ogc:Filter>
          <ogc:And>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>under5mort</ogc:PropertyName>
             <ogc:Literal>37.4</ogc:Literal>
           </ogc:PropertyIsGreaterThanOrEqualTo>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>under5mort</ogc:PropertyName>
           <ogc:Literal>46.3</ogc:Literal>
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
          <Name>46.3 to 51.5</Name>
          <ogc:Filter>
          <ogc:And>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>poverty</ogc:PropertyName>
             <ogc:Literal>46.3</ogc:Literal>
           </ogc:PropertyIsGreaterThanOrEqualTo>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>under5mort</ogc:PropertyName>
           <ogc:Literal>51.5</ogc:Literal>
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
          <Name>51.5 to 71.5</Name>
          <ogc:Filter>
          <ogc:And>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>under5mort</ogc:PropertyName>
             <ogc:Literal>51.5</ogc:Literal>
           </ogc:PropertyIsGreaterThanOrEqualTo>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>under5mort</ogc:PropertyName>
           <ogc:Literal>71.5</ogc:Literal>
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

