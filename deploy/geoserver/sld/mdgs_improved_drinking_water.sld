<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc"
                       xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                       xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd">
    <NamedLayer>
        <Name>improved_d</Name>
        <UserStyle>
            <Name>improved_d</Name>
            <Title>Improved Drinking Water</Title>
            <Abstract>A style emphasizing population having access to improved drinking water statistics</Abstract>
            <FeatureTypeStyle>
                <Rule>
                    <Name>Less than 68</Name>
                    <ogc:Filter>
                        <ogc:PropertyIsLessThan>
                            <ogc:PropertyName>improved_d</ogc:PropertyName>
                            <ogc:Literal>68</ogc:Literal>
                        </ogc:PropertyIsLessThan>
                    </ogc:Filter>
                    <PolygonSymbolizer>
                        <Fill>
                            <CssParameter name="fill">#00aad4</CssParameter>
                            <CssParameter name="fill-opacity">0.12</CssParameter>
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
                                <ogc:PropertyName>improved_d</ogc:PropertyName>
                                <ogc:Literal>68</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThan>
                                <ogc:PropertyName>improved_d</ogc:PropertyName>
                                <ogc:Literal>76</ogc:Literal>
                            </ogc:PropertyIsLessThan>
                        </ogc:And>
                    </ogc:Filter>
                    <PolygonSymbolizer>
                        <Fill>
                            <CssParameter name="fill">#00aad4</CssParameter>
                            <CssParameter name="fill-opacity">0.24</CssParameter>
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
                                <ogc:PropertyName>improved_d</ogc:PropertyName>
                                <ogc:Literal>76</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThan>
                                <ogc:PropertyName>improved_d</ogc:PropertyName>
                                <ogc:Literal>84</ogc:Literal>
                            </ogc:PropertyIsLessThan>
                        </ogc:And>
                    </ogc:Filter>
                    <PolygonSymbolizer>
                        <Fill>
                            <CssParameter name="fill">#00aad4</CssParameter>
                            <CssParameter name="fill-opacity">0.36</CssParameter>
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
                                <ogc:PropertyName>improved_d</ogc:PropertyName>
                                <ogc:Literal>84</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThan>
                                <ogc:PropertyName>improved_d</ogc:PropertyName>
                                <ogc:Literal>92</ogc:Literal>
                            </ogc:PropertyIsLessThan>
                        </ogc:And>
                    </ogc:Filter>
                    <PolygonSymbolizer>
                        <Fill>
                            <CssParameter name="fill">#00aad4</CssParameter>
                            <CssParameter name="fill-opacity">0.48</CssParameter>
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
                            <ogc:PropertyName>improved_d</ogc:PropertyName>
                            <ogc:Literal>92</ogc:Literal>
                        </ogc:PropertyIsGreaterThanOrEqualTo>
                    </ogc:Filter>
                    <PolygonSymbolizer>
                        <Fill>
                            <CssParameter name="fill">#00aad4</CssParameter>
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
