import os
from pathlib import Path
import streamlit as st
# import leafmap.foliumap as leafmap
import folium
from folium.plugins import BeautifyIcon, MarkerCluster, Fullscreen
# from streamlit_folium import folium_static#st_folium
import streamlit.components.v1 as components
# import geopandas as gpd
import pandas as pd




# popup_dict = {'source':"Data Source",'inside':"Miles from BNRW",
#               'last_active':"Last year active",'gps':'GPS'}

popup_dict = {'source':"Data Source",'inside_bnr':"Miles from BNRW",
              'gps':'GPS','integrator':'Integrator', 'type': 'Type',
              'last_active':"Last year active",'num_poultry':"Number of birds",'waste_lbs_yr':'Poultry waste [lbs/yr]'}

@st.cache  
def popupHTML(row, popup_dict=popup_dict,col1width=50):
    '''Create custom HTML for popup.

    Parameters
    ----------
    row : TYPE
        DESCRIPTION.

    Returns
    -------
    html : TYPE
        DESCRIPTION.
        
    After: https://towardsdatascience.com/folium-map-how-to-create-a-table-style-pop-up-with-html-code-76903706b88a
           and https://github.com/Gromopo/GroMoPo

    '''
    html = """<!DOCTYPE html>
            <html>
            
            <table>
            <tbody>
            """
    
    for key, value in popup_dict.items():
        # Loop through entries for popup with specific formatting
        
        if row[key] is None:
            second_col_val= 'N/A'
        else:
            second_col_val = row[key]
        
        if 'link' in value: # format for clickable link
            html += """<tr>
                       <td><span style="text-align: left;width: {0}px; color: #293191; overflow-wrap: break-word;"><b>{1}</b></span></td>
                       <td><span style="text-align: right;overflow-wrap: break-word;>""".format(col1width,value) # Attribute name
                       
            # if second_col_val != 'N/A' and second_col_val is not None:
                
            links = second_col_val.split('|')
            links.insert(0,"") # for some reason need a dummy entry, as first entry doesn't show up as link, only as text.
            
                
            # link_html = """ """.join(["""<a href="{0}" target="_blank"> {0}</a><br>""".format(link) for link in links])
            link_html = """ """
            for i,link in enumerate(links):
                if i == 0:
                    link_html += """<a href="{0}" target="_blank">{0}</a>""".format(link)
                elif link == 'N/A':
                    link_html += """{}<br>""".format(link)
                else:
                    link_html += """<a href="{0}" target="_blank">{0}</a><br>""".format(link)
            
            html += link_html
            # else:
            #     html += """{0}<br>""".format(second_col_val)
                
            html += """</span></td></tr>"""
            # html += """</td></td></td></tr>"""


        else:
            html += """<tr>
                       <td style="text-align: left;"><span style="width: {0}px;color: #000000;overflow-wrap: break-word;"><b>{1}</b></span></td>
                       <td style="text-align: right; overflow-wrap: break-word;">{2}</td></tr>""".format(col1width,value,second_col_val)
                       
    
    html += """</tbody>
               </table>                    
               </html>"""
    
    return html

def load_xy_to_cluster(shp_df,icon_name='home',popup_cols=[],
                       include_latlon=True,min_width=100,max_width=200,):
    
    icf_active = '''
    function(cluster) {
    return L.divIcon({html: '<div><span>' + cluster.getChildCount() + '</span></div>',
                      className: 'marker-cluster marker-cluster-large',
                      iconSize: new L.Point(30, 30)});
    }
    '''
    icf_inactive = '''
        function(cluster) {

        return L.divIcon({html:'<div><span>' + cluster.getChildCount() + '</span></div>',
                          className: 'marker-cluster marker-cluster-medium',
                          iconSize: new L.Point(30, 30)});
        }
    '''
    
    
    m_cluster_act = MarkerCluster(name="Poultry Houses",control=True,icon_create_function=icf_active)
    m_cluster_inact = MarkerCluster(name="Inactive Houses",control=True,icon_create_function=icf_inactive)
    # Only works with v4, https://fontawesome.com/v4/icons/
    # in v5, there is 'turkey'
    # for ilon,ilat in zip(lon,lat):
    for irow,row_df in shp_df.iterrows():
        
        html = row_df['popup_html']
        # if include_latlon: # add latitude and longitude
        #     html = html + "<b>" + 'GPS' + "</b>" + ": " + "{0:3.4f},{1:3.4f}".format(row_df.geometry.y,row_df.geometry.x) + "<br>"
        # for p in popup_cols:
        #     html = html + "<b>" + p + "</b>" + ": " + str(row[p]) + "<br>"
        
        
        if len(html)>0:
            mark_popup = folium.Popup(html,min_width=min_width, max_width=max_width)
        else:
            mark_popup = None
        
        if row_df['active'] == 1:
            color = 'black'
            icon_name2=icon_name
            
            folium.Marker([row_df.latitude,row_df.longitude],
               popup=mark_popup,
               icon=BeautifyIcon(icon=icon_name2,
                                 icon_shape='circle', 
                                 border_color='transparent', 
                                 inner_icon_style= 'color:{};font-size:30px'.format(color),
                                 # border_width=2,
                                 background_color='transparent')).add_to(m_cluster_act)
            
            
        else:
            color = 'grey'
            icon_name2 = 'times-circle'
        
            folium.Marker([row_df.latitude,row_df.longitude],
               popup=mark_popup,
               icon=BeautifyIcon(icon=icon_name2,
                                 icon_shape='circle', 
                                 border_color='transparent', 
                                 inner_icon_style= 'color:{};font-size:30px'.format(color),
                                 # border_width=2,
                                 background_color='transparent')).add_to(m_cluster_inact)
        
    return m_cluster_act,m_cluster_inact

# if platform.system() == 'Windows':
#     main_path = Path(".")
# else:
main_path = Path(".")
    
# shp_path = str(main_path.absolute().joinpath('data', 'bnr_chicken_house+2mile.geojson'))
# shp_df = gpd.read_file(shp_path)
# shp_df.loc[shp_df['last_active'].isna(),'last_active'] = 2022
# shp_df['last_active'] = gpd.pd.to_numeric(shp_df['last_active'],downcast="integer")
# shp_df['gps'] = shp_df.apply(lambda row: "{0:3.4f},{1:3.4f}".format(row.geometry.xy[1][0],row.geometry.xy[0][0]),axis=1)


# shp_df['popup_html'] = shp_df.apply(popupHTML,axis=1)


# m_cluster = load_xy_to_cluster(shp_df)

# Use csv
csv_path = str(main_path.absolute().joinpath('data', 'bnr_feedingoperations_app.csv'))
csv_df = pd.read_csv(csv_path)

# Fill no data rows
csv_df.loc[csv_df['last_active'].isna(),'last_active'] = 0
csv_df.loc[csv_df['integrator'].isin(['CLOSED']),'active'] = 0
csv_df.loc[csv_df['integrator'].isna(),'integrator'] = 'Unknown'
csv_df.loc[csv_df['type'].isna(),'type'] = 'Unknown'

csv_df['last_active'] = pd.to_numeric(csv_df['last_active'],downcast="integer")
csv_df['gps'] = csv_df.apply(lambda row: "{0:3.4f},{1:3.4f}".format(row.longitude,row.latitude),axis=1)
csv_df['waste_lbs_yr'] = csv_df['waste_tons_per_yr'].astype(int)*2000 # Convert tons to pounds
csv_df['num_poultry'] = (1.2*csv_df['roof_area_ft2']).astype(int) # calculate number of birds from sq ft

csv_df['popup_html'] = csv_df.apply(popupHTML,axis=1)


# calculate total waste for current and past
inside_bnr = csv_df.loc[csv_df['inside_bnr']==0].shape[0]
buff2mi = csv_df.loc[csv_df['inside_bnr']>0].shape[0]
active_all = csv_df.loc[(csv_df['active']==1)].shape[0]


ctotal_waste_lbs = int(int((2e3*csv_df.loc[csv_df['active']==1,'waste_tons_per_yr'].sum())/1e3)*1e3)
ctotal_roof_area = int(int((csv_df.loc[csv_df['active']==1,'roof_area_ft2'].sum())/1e3)*1e3)
cn_chickens = int(int((ctotal_roof_area * 1.2)/1e3)*1e3) # 1.2 chickens/sq ft

ptotal_waste_lbs = int(int((2e3*csv_df.loc[csv_df['active']!=1,'waste_tons_per_yr'].sum())/1e3)*1e3)
ptotal_roof_area = int(int((csv_df.loc[csv_df['active']!=1,'roof_area_ft2'].sum())/1e3)*1e3)
pn_chickens = int(int((ptotal_roof_area * 1.2)/1e3)*1e3) # 1.2 chickens/sq ft

# total_waste_lbs = int(int((2e3*csv_df['waste_tons_per_yr'].sum())/1e3)*1e3)
# total_roof_area = csv_df['roof_area_ft2'].sum()
# n_chickens = int(int((total_roof_area * 1.2)/1e3)*1e3) # 1.2 chickens/sq ft

m_cluster,m_group = load_xy_to_cluster(csv_df)

ws_path = str(main_path.absolute().joinpath('data', 'bnr_ws_hu8.geojson'))
ws_style = lambda x:{'lineColor':'#F0F8FF',
            'weight': 3,
            'interactive':False,
            'stroke':True,
            'fillColor':'none',
    }

ch_colors = ['#A9A69F','#A97B00','#00C11A','#D40000'] #very low, low, optimum, above optimum

ch_path = str(main_path.absolute().joinpath('data', 'C_and_H.geojson'))
ch_style = lambda feature: {'fillColor':"{}".format(ch_colors[feature['properties']['Pcat']]),
                    'interactive':True,
                    'stroke':False,
                    # 'color': 'grey',
                    'fillOpacity': 0.7
                    }


about_text = """
        This web [app](https://github.com/buffalorwa/streamlit-brwa) is maintained by the [Buffalo River Watershed Alliance](https://buffaloriveralliance.org/).
        You can follow the BRWA on [Facebook](https://www.facebook.com/Buffalo-River-Watershed-Alliance-164944453665495/).
    """

# https://github.com/giswqs/leafmap/blob/84fb926c556dd377baaf10d9a9c57d749fb5c9cb/leafmap/basemaps.py#L23
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
    st.title("Feeding Operations in the Buffalo National River Watershed")

    st.markdown(
        """
    
    The [Buffalo River Watershed Alliance](https://buffaloriveralliance.org/) was created to help preserve and protect
    the scenic beauty and pristine water quality of the Buffalo National River. Monitoring the river to enhance its
    status as the nation's First National River benefits the river itself, the land adjacent to it, several species
    of wildlife, numerous recreation activities, local farmers, nearby communities, tourists, and the local economy
    which depends greatly upon visitors to the river and the watershed area. It is clear that we all depend on the
    quality of the Buffalo River and the Watershed.

    The purpose of this interactive map is to identify potential sources that could have a negative impact on the river
    and its tributaries under suboptimal conditions and to allow everyone who has an interest in maintaining the quality
    of the river to have a big picture view of the watershed. Sources that can produce excess nutrification or degradation
    of the river, such as commercial poultry houses, concentrated animal feeding operations (CAFOs), and municipal waste
    water treatment plants, will be shown, along with geological characteristics and more over time.
    
    The hope is that local businesses, farmers, environmental groups, and other parties can utilize this information to
    determine best practices in terms of land use, management of wastes, and optimization of operations in order to keep
    the Buffalo River pristine for generations to come.

    """
    )

    c1, c2 = st.columns([3,1])
    
    with c1:
        m = folium.Map(location=(35.9658, -92.8103), zoom_start=10)
        
        # Add google maps as a basemap option
        
        for ikey in imaps:
            folium.TileLayer(imaps[ikey]['url'],attr=imaps[ikey]['attribution'],name=imaps[ikey]['name']).add_to(m)
        # m.add_basemap("HYBRID")
        # m.add_basemap("ROADMAP")
        
        # Add watershed outline
        # m.add_geojson(ws_path, layer_name='BNR Watershed', style=ws_style, fill_colors=['none'])
        folium.GeoJson(ws_path, name='BNR Watershed', style_function=ws_style).add_to(m)
        
        # Add C&H fields
        folium.GeoJson(ch_path, name='C&H Fields', style_function=ch_style).add_to(m)
        # Add chicken houses
        # m_ch = GeoJson(shp_path, name='Chicken Houses (2014)')
        
        # m_group = FeatureGroup(name='Chicken Clusters').add_to(m)
        m_cluster.add_to(m)
        m_group.add_to(m)
        # m_ch.add_to(m_group)
        
        m.add_child(folium.LayerControl())
        Fullscreen().add_to(m)
    
        # folium_static(m, height=700, width=1400)
        # folium_static(m,height=700,width=1000)
        
        fig = folium.Figure().add_child(m)
        components.html(
                        fig.render(), height=700 + 10
                        )
        
        # outfile = os.path.abspath('feedingtemp' + ".html")
        # m.save(outfile)
        # out_html = ""
        # with open(outfile) as f:
        #     lines = f.readlines()
        #     out_html = "".join(lines)
        # os.remove(outfile)
        
        # components.html(out_html,height=700,scrolling=False)

    with c2:
        # Eventually information on the (static) number of known feeding operations and
        # how many are estimated to be active in the ws. Markdown isn't working right
        st.markdown('''
                    # Poultry Operations \n
                    <p></p>
                    
                    - **{0}** structures within the BNR watershed
    
                    - **{1}** additional structures are within a 2 mile buffer of the BNR watershed
                    
                    - **{2}** estimated active structures inside of and near the BNR watershed
                    
                    - Presumed active:
                        - **{3:,} ft$$^2$$** roof area
                        - ~**{4:,} chickens & turkeys**
                        - ~**{5:,} lb/yr solid waste**
                    
                    - Presumed inactive:
                        - **{6:,} ft$$^2$$** roof area
                        - ~**{7:,} chickens & turkeys**
                        - ~**{8:,} lb/yr solid waste**
                    
                    Active operations clustered in orange. Inactive in yellow.
                    '''.format(inside_bnr,buff2mi,active_all,
                    ctotal_roof_area,cn_chickens,ctotal_waste_lbs,
                                ptotal_roof_area,pn_chickens,ptotal_waste_lbs),unsafe_allow_html=True)
        st.image('data/opstatus.png',width=80)                    
        
        with st.expander("Hog operations"):
            st.markdown('''
                        # Hog operations \n
                        
                        No known hog operations are currently active in the BNR watershed, 
                        but closed sites could have a lasting effect on the water quality.
                        The closed C&H waste application fields near Mount Judea are shown with their excess
                        Phosphorous loading as of March 15, 2017.
                        ''',
                        unsafe_allow_html=True)
            st.image('data/plevels.png',width=200)
        
    with st.expander("Additional information"):
        st.markdown(about_text)
        st.write("""
                 The calculations for the solid waste production were based on 
                 the methods developed for the WaterKeeper Alliance and EWG
                 ["Fields of Filth" interactive map](https://www.ewg.org/interactive-maps/2020-fields-of-filth/map/).
                 This methodology is further described  at https://www.ewg.org/research/exposing-fields-filth-north-carolina.
                 
                 The Arkansas Natural Resources Commission (ANRC) is the agency responsible for overseeing poultry operations statewide. 
                 By statute, ANRC does not divulge information about individual poultry operations, such as location, capacity, annual waste
                 production or integrator name. They do provide annual summary reports for each county. As a result, we have visually determined
                 the facilities shown on this map based on satellite and aerial imagery. Information regarding bird capacity and waste production
                 are estimates based on the calculated square footage of each structure combined with information from academic sources regarding
                 poultry production, including standard stocking density, growout time, flocks per year and waste production.
                 
                 **Processing steps**
                 1) Feeding operations identified or interpreted as a poultry operation.
                 2) Poultry house roofs were manually traced from aerial imagery (e.g., [Google Maps](https://maps.google.com)) with GIS software.
                 3) The area of each roof was calculated from the traced feature.
                 4) The number of birds was estimated per house using 1.2 birds/ft$$^{2}$$ (USDA Poultry Industry Manual, 2013) multipled by roof area. Approximate range is 0.9-2 birds/ft$$^{2}$$.
                 5) The amount of waste was estimated using 7.2-25 tons/1000 birds per year based on the type of operation [Fields of Filth accumulated waste analysis Figure 1](https://www.ewg.org/research/exposing-fields-filth-north-carolina).
                 6) Active status was approximated by interpreting the condition of the roof in imagery from ~2022. When a structure was apparently damaged or removed, historic imagery (i.e., [Google Earth](https://earth.google.com) was used to approximate when the feeding operation was last active.    
                 
                 For more information or to suggest changes or improvements to the data or application, please contact the [BRWA](https://buffaloriveralliance.org/).                                                                                                                                                                         
                                                                                                                                                                                          
                 ---
                 
                 # References \n
                 AHTD (Arkansas Highway and Transportation Department) Chicken Houses, August 29, 2006: https://gis.arkansas.gov/product/chicken-house-point/
                 
                 USDA Poultry Industry Manual (2013), Table 6. Stocking Densities According to Bird Numbers and Live Weight, page 19 of 74, https://www.aphis.usda.gov/animal_health/emergency_management/downloads/documents_manuals/poultry_ind_manual.pdf
                 
                 """)