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
                    <Name>Less than 68</Name>
                    <ogc:Filter>
                        <ogc:PropertyIsLessThan>
                            <ogc:PropertyName>enrollment</ogc:PropertyName>
                            <ogc:Literal>68</ogc:Literal>
                        </ogc:PropertyIsLessThan>
                    </ogc:Filter>
                    <PolygonSymbolizer>
                        <Fill>
                            <CssParameter name="fill">#fbec04</CssParameter>
                            <CssParameter name="fill-opacity">0.40</CssParameter>
                        </Fill>
                        <Stroke>
                            <CssParameter name="stroke">#777777</CssParameter>
                            <CssParameter name="stroke-width">0.5</CssParameter>
                        </Stroke>
                    </PolygonSymbolizer>
                </Rule>
                <Rule>
                    <Name>68 to 76</Name>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>enrollment</ogc:PropertyName>
                                <ogc:Literal>68</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThan>
                                <ogc:PropertyName>enrollment</ogc:PropertyName>
                                <ogc:Literal>76</ogc:Literal>
                            </ogc:PropertyIsLessThan>
                        </ogc:And>
                    </ogc:Filter>
                    <PolygonSymbolizer>
                        <Fill>
                            <CssParameter name="fill">#c3eb18</CssParameter>
                            <CssParameter name="fill-opacity">0.45</CssParameter>
                        </Fill>
                        <Stroke>
                            <CssParameter name="stroke">#777777</CssParameter>
                            <CssParameter name="stroke-width">0.5</CssParameter>
                        </Stroke>
                    </PolygonSymbolizer>
                </Rule>
                <Rule>
                    <Name>76 to 84</Name>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>enrollment</ogc:PropertyName>
                                <ogc:Literal>76</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThan>
                                <ogc:PropertyName>enrollment</ogc:PropertyName>
                                <ogc:Literal>84</ogc:Literal>
                            </ogc:PropertyIsLessThan>
                        </ogc:And>
                    </ogc:Filter>
                    <PolygonSymbolizer>
                        <Fill>
                            <CssParameter name="fill">#7de931</CssParameter>
                            <CssParameter name="fill-opacity">0.50</CssParameter>
                        </Fill>
                        <Stroke>
                            <CssParameter name="stroke">#777777</CssParameter>
                            <CssParameter name="stroke-width">0.5</CssParameter>
                        </Stroke>
                    </PolygonSymbolizer>
                </Rule>
                <Rule>
                    <Name>84 to 92</Name>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>enrollment</ogc:PropertyName>
                                <ogc:Literal>84</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThan>
                                <ogc:PropertyName>enrollment</ogc:PropertyName>
                                <ogc:Literal>92</ogc:Literal>
                            </ogc:PropertyIsLessThan>
                        </ogc:And>
                    </ogc:Filter>
                    <PolygonSymbolizer>
                        <Fill>
                            <CssParameter name="fill">#33e74b</CssParameter>
                            <CssParameter name="fill-opacity">0.55</CssParameter>
                        </Fill>
                        <Stroke>
                            <CssParameter name="stroke">#777777</CssParameter>
                            <CssParameter name="stroke-width">0.5</CssParameter>
                        </Stroke>
                    </PolygonSymbolizer>
                </Rule>
                <Rule>
                    <Name>Greater than 92</Name>
                    <ogc:Filter>
                        <ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyName>enrollment</ogc:PropertyName>
                            <ogc:Literal>92</ogc:Literal>
                        </ogc:PropertyIsGreaterThanOrEqualTo>
                    </ogc:Filter>
                    <PolygonSymbolizer>
                        <Fill>
                            <CssParameter name="fill">#00e65d</CssParameter>
                            <CssParameter name="fill-opacity">0.60</CssParameter>
                        </Fill>
                        <Stroke>
                            <CssParameter name="stroke">#777777</CssParameter>
                            <CssParameter name="stroke-width">0.5</CssParameter>
                        </Stroke>
                    </PolygonSymbolizer>
                </Rule>
            </FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>
