import os
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import folium
from folium.features import GeoJsonPopup
from folium.plugins import MarkerCluster, Fullscreen
import geopandas as gpd


main_path = Path(".")
shp_path = str(main_path.absolute().joinpath('data', 'bnr_geology.geojson'))
style_geo = lambda feature: {'fillColor':"#{}".format(feature['properties']['HexColor']),
                    'interactive':True,
                    'stroke':False,
                    # 'color': 'grey',
                    'fillOpacity': 0.7
                    }

hfunc = lambda feature:{'color':"#{}".format(feature['properties']['HexColor']),
                        'stroke':True,
                        'weight':1}

# Popup information
geo_popup = GeoJsonPopup(fields=['FM_NAME','LithName'],aliases=['Unit','Rocks'])

geo_labels = ['Boone',
             'Cotter/Jefferson City',
             'Powell',
             'Penters/Clifty/Chattanooga',
             'Newton/Everton',
             'Pitkin/Fayetteville/Batesville',
             'Cane Hill/Hale',
             'Prairie Grove/Bloyd undifferentiated',
             'Cason/Fernvale/Kimmswick/Plattin/Joachim',
             'Atoka',
             'Lafferty/St. Clair/Brassfield',
             'Ruddell',
             'Hartshorne']

geo_colors = ['#E3E3DC',
             '#FFEBEB',
             '#E06391',
             '#6E5622',
             '#FF9991',
             '#A3A196',
             '#A8D7FF',
             '#3D6A94',
             '#FFE0F5',
             '#C5E5F0',
             '#6C5282',
             '#6E6F6E',
             '#3E809E']

ws_path = str(main_path.absolute().joinpath('data', 'bnr_ws_hu8.geojson'))
ws_style = lambda x:{'lineColor':'#F0F8FF',
            'weight': 3,
            'interactive':False,
            'stroke':True,
            'fillColor':'none',
    }


imaps = {
    "ROADMAP": {
        "url": "https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        "attribution": "Google",
        "name": "Google Maps",
    },
    "TERRAIN": {
        "url": "https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
        "attribution": "Google",
        "name": "Google Terrain",
    },
    "HYBRID": {
        "url": "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        "attribution": "Google",
        "name": "Google Satellite",
    },
}

def app():
    st.title("Geology")

    st.markdown(
        """
    The geology of the Buffalo National River Watershed retains a history of long ago oceans
    that shape the environmental setting in the BNR today. Cave-forming limestones of the Boone formation create 
    shortcuts for water to flow quickly into the river.
    """
    )

    c1, c2 = st.columns([3,1])
    
    with c1:
        m = folium.Map(center=(35.9658, -92.8103), min_zoom=10, zoom_start=11)
        
        # Add google maps as a basemap option
        for ikey in imaps:
            folium.TileLayer(imaps[ikey]['url'],attr=imaps[ikey]['attribution'],name=imaps[ikey]['name']).add_to(m)
        
        # # Add geology
        m_ch = folium.GeoJson(shp_path, name='Geology',style_function=style_geo,
                       highlight_function=hfunc,popup=geo_popup)
        m_ch.add_to(m)
        
        # Add watershed outline
        folium.GeoJson(ws_path, name='BNR Watershed', style_function=ws_style).add_to(m)


        m.add_child(folium.LayerControl())
        Fullscreen().add_to(m)
        
        outfile = os.path.abspath('geotemp' + ".html")
        m.save(outfile)
        out_html = ""
        with open(outfile) as f:
            lines = f.readlines()
            out_html = "".join(lines)
        os.remove(outfile)
        
        components.html(out_html,height=700,scrolling=False)
