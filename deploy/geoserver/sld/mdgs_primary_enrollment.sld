<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc"
  xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd">
  <NamedLayer>
    <Name>Primary Enrollment</Name>
    <UserStyle>
      <Name>primary enrollment</Name>
      <Title>Primary Enrollement</Title>
      <Abstract>A style emphasizing enrollment in Primary School</Abstract>
      <FeatureTypeStyle>
        <Rule>
          <Name>Less than 75</Name>
          <ogc:Filter>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>enrollment</ogc:PropertyName>
           <ogc:Literal>75</ogc:Literal>
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
          <Name>75 to 80</Name>
          <ogc:Filter>
          <ogc:And>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>enrollment</ogc:PropertyName>
             <ogc:Literal>75</ogc:Literal>
           </ogc:PropertyIsGreaterThanOrEqualTo>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>enrollment</ogc:PropertyName>
           <ogc:Literal>80</ogc:Literal>
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
          <Name>80 to 85</Name>
          <ogc:Filter>
          <ogc:And>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>enrollment</ogc:PropertyName>
             <ogc:Literal>80</ogc:Literal>
           </ogc:PropertyIsGreaterThanOrEqualTo>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>enrollment</ogc:PropertyName>
           <ogc:Literal>85</ogc:Literal>
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
          <Name>85 to 90</Name>
          <ogc:Filter>
          <ogc:And>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>enrollment</ogc:PropertyName>
             <ogc:Literal>85</ogc:Literal>
           </ogc:PropertyIsGreaterThanOrEqualTo>
          <ogc:PropertyIsLessThan>
           <ogc:PropertyName>enrollment</ogc:PropertyName>
           <ogc:Literal>90</ogc:Literal>
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
          <Name>Greater than 90</Name>
          <ogc:Filter>
           <ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyName>enrollment</ogc:PropertyName>
             <ogc:Literal>90</ogc:Literal>
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

