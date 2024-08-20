import unittest

class Test(unittest.TestCase):
    def test(self):
        from naotw.gis import tokml
        from zhongwen.pandas_tools import show_html
        from pathlib import Path
        import geopandas as gpd
        geojson = Path(__file__).parent / '農地光電.geojson'
        gdf = gpd.read_file(geojson)
        tokml(geojson)
        # show_html(gdf)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(Test('test'))  # 指定測試
    unittest.TextTestRunner().run(suite)
