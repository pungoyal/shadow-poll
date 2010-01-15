class MockGeoServer():
    def get_feature_info(self):
        return '''
        Results for FeatureType 'IRQ_adm2':
        --------------------------------------------
        the_geom = [GEOMETRY (MultiPolygon) with 564 points]
        ID_0 = 109
        ISO = IRQ
        NAME_0 = Iraq
        ID_1 = 1378
        NAME_1 = Al-Anbar
        ID_2 = 16581
        NAME_2 = Ar Rutbah
        VARNAME_2 = 
        NL_NAME_2 = 
        HASC_2 = 
        CC_2 = 
        TYPE_2 = 
        ENGTYPE_2 = 
        VALIDFR_2 = 
        VALIDTO_2 = 
        REMARKS_2 = 
        Shape_Leng = 14.0594266947
        Shape_Area = 9.37942880399
        -------------------------------------------
        '''