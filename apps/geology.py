import streamlit as st
import leafmap.foliumap as leafmap
from folium import GeoJson
from folium.features import GeoJsonPopup
from folium.plugins import MarkerCluster
import geopandas as gpd


shp_path = r"data\bnr_geology.geojson"
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

ws_path = r"data\bnr_ws_hu8.geojson"
ws_style = {'lineColor':'#F0F8FF',
            'weight': 3,
            'interactive':False,
            'stroke':True,
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
        m = leafmap.Map(center=(35.9658, -92.8103), zoom=11,locate_control=True,google_map='ROADMAP')
        
        # Add google maps as a basemap option
        # m.add_basemap("ROADMAP")
        m.add_basemap("HYBRID")
        
        # # Add geology
        # m.add_geojson(shp_path, layer_name='Geology',
        #               style_function=style_geo,
        #               highlight_function=hfunc,
        #               info_mode='on_click',popup=geo_popup)
        
        
        
        m.add_legend(title='Geologic units',labels=geo_labels,colors=geo_colors)
        
        
        m_ch = GeoJson(shp_path, name='Geology',style_function=style_geo,
                       highlight_function=hfunc,popup=geo_popup)
        m_ch.add_to(m)
        
        # Add watershed outline
        m.add_geojson(ws_path, layer_name='BNR Watershed', style=ws_style, fill_colors=['none'])
        
        # m_group = FeatureGroup(name='ch').add_to(m)
        # m_cluster.add_to(m_group)
        # m_ch.add_to(m_group)
        
        m.to_streamlit(height=700,bidirectional=False)
