import pandas as pd
import streamlit as st
import requests
import json
import pydeck as pdk

api_key = api_key
bike_dict = {"rackTotCnt":[], "stationName":[],
             "parkingBikeTotCnt":[], "shared":[],
             "latitude":[], "longitude":[]}
num = 0
while True:
    url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/bikeList/{1 + 1000 * num}/{1000 + 1000 * num}/"
    data = requests.get(url)
    result = json.loads(data.text)  # json --> dict
    for row in result["rentBikeStatus"]["row"]:
        bike_dict["rackTotCnt"].append(int(row["rackTotCnt"]))
        bike_dict["stationName"].append(row["stationName"])
        bike_dict["parkingBikeTotCnt"].append(int(row["parkingBikeTotCnt"]))
        bike_dict["shared"].append(int(row["shared"]))
        bike_dict["latitude"].append(float(row["stationLatitude"]))
        bike_dict["longitude"].append(float(row["stationLongitude"]))
    if len(result["rentBikeStatus"]["row"]) != 1000:
        break
    num += 1

df = pd.DataFrame(bike_dict)
st.write("# 따릉이 시각화 결과")
st.write(df)

# pydeck 모듈로 시각화
layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position=["longitude", "latitude"],
    get_fill_color=["255-shared", "255-shared", "255"],  #색의 RGB값 0~255
    get_radius="60*shared/100",  #점의 크기
    pickable=True  #마우스 이동가능 옵션
)
lat_center = df["latitude"].mean()
lon_center = df["longitude"].mean()
initial_view = pdk.ViewState(latitude=lat_center, longitude=lon_center, zoom=10)
map = pdk.Deck(layers=[layer], initial_view_state=initial_view,
               tooltip={"text":"대여소 : {stationName}\n현재 주차 대수 : {parkingBikeTotCnt}"})   #마우스 올리면 정보가 뜨게끔(tooltip)
st.pydeck_chart(map)
