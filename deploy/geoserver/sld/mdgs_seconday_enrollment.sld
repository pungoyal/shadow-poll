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
                    <Name>10 to 17</Name>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>enrollmen3</ogc:PropertyName>
                                <ogc:Literal>10</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThan>
                                <ogc:PropertyName>enrollmen3</ogc:PropertyName>
                                <ogc:Literal>17</ogc:Literal>
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
                    <Name>17 to 24</Name>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>enrollmen3</ogc:PropertyName>
                                <ogc:Literal>17</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThan>
                                <ogc:PropertyName>enrollmen3</ogc:PropertyName>
                                <ogc:Literal>24</ogc:Literal>
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
                    <Name>24 to 31</Name>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>enrollmen3</ogc:PropertyName>
                                <ogc:Literal>24</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThan>
                                <ogc:PropertyName>enrollmen3</ogc:PropertyName>
                                <ogc:Literal>31</ogc:Literal>
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
                    <Name>Greater than 31</Name>
                    <ogc:Filter>
                        <ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyName>enrollmen3</ogc:PropertyName>
                            <ogc:Literal>31</ogc:Literal>
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
