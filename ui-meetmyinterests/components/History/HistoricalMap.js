import React, { useLayoutEffect, useRef } from "react";
import * as am5 from "@amcharts/amcharts5";
import * as am5map from "@amcharts/amcharts5/map";
import am5geodata_worldLow from "@amcharts/amcharts5-geodata/worldLow";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";

const HistoricalMap = () => {
  const chartRef = useRef(null);
  const chartInstanceRef = useRef(null);

  const empires = [
    {
      id: "Greek Empire",
      period: "800 BC - 146 BC",
      color: 0x2ca02c,
      areas: ["GR", "TR", "SY", "EG", "IR"],
    },
    {
      id: "Macedonian Empire",
      period: "336 BC - 323 BC",
      color: 0x1f78b4,
      areas: ["GR", "EG", "IR", "SY", "TR"],
    },
    {
      id: "Roman Empire",
      period: "27 BC - 476 AD",
      color: 0xff7f00,
      areas: ["IT", "FR", "ES", "PT", "GR", "TR", "BG", "RO", "AL", "DZ", "LY", "TN", "MA", "EG"],
    },
    {
      id: "Byzantine Empire",
      period: "330 AD - 1453 AD",
      color: 0x9467bd,
      areas: ["GR", "TR", "BG", "RO", "AL"],
    },
    {
      id: "Islamic Caliphate",
      period: "622 AD - 1258 AD",
      color: 0x33a02c,
      areas: ["SA", "EG", "SY", "IQ", "LY", "YE"],
    },
    {
      id: "Umayyad Dynasty",
      period: "661 AD - 750 AD",
      color: 0xd62728,
      areas: ["MA", "DZ", "LY", "TN", "EG", "ES", "PT", "SY", "IQ", "SA", "YE", "JO", "KW", "AF"],
    },
    {
      id: "Abbasid Dynasty",
      period: "750 AD - 1258 AD",
      color: 0x8c564b,
      areas: ["IQ", "SY", "SA", "YE", "EG", "IR", "PK", "IN"],
    },
    {
      id: "Seljuk Empire",
      period: "1037 AD - 1194 AD",
      color: 0xe377c2,
      areas: ["IR", "TR", "SY", "UZ", "KZ"],
    },
    {
      id: "Mongol Empire",
      period: "1206 AD - 1368 AD",
      color: 0xe31a1c,
      areas: ["MN", "CN", "KZ", "UZ", "TJ", "KG"],
    },
    {
      id: "Ottoman Empire",
      period: "1299 AD - 1923 AD",
      color: 0xffc107,
      areas: ["TR", "GR", "BG", "RO", "RS", "BA", "AL", "MK", "ME", "HU", "HR",
      "SY", "IQ", "IL", "JO", "LB", "SA",
      "EG", "LY", "TN", "DZ",],
    },
    {
      id: "Mughal Empire",
      period: "1526 AD - 1857 AD",
      color: 0x6a3d9a,
      areas: ["IN", "PK", "BD"],
    },
    {
      id: "Ethiopian Empire",
      period: "1270 AD - 1974 AD",
      color: 0xb15928,
      areas: ["ET"],
    },
  ];

  const markers = [
    { id: "1", empire: "Greek Empire", oldName: "Athens", modernName: "Athens", lat: 37.9838, lon: 23.7275 },
    { id: "2", empire: "Roman Empire", oldName: "Rome", modernName: "Rome", lat: 41.9028, lon: 12.4964 },
    { id: "3", empire: "Byzantine Empire", oldName: "Constantinople", modernName: "Istanbul", lat: 41.0082, lon: 28.9784 },
    { id: "4", empire: "Islamic Caliphate", oldName: "Mecca", modernName: "Mecca", lat: 21.3891, lon: 39.8579 },
    { id: "5", empire: "Islamic Caliphate", oldName: "Medina", modernName: "Medina", lat: 24.5247, lon: 39.6111 },
    { id: "6", empire: "Umayyad Dynasty", oldName: "Damascus", modernName: "Damascus", lat: 33.5138, lon: 36.2913 },
    { id: "7", empire: "Abbasid Dynasty", oldName: "Baghdad", modernName: "Baghdad", lat: 33.3152, lon: 44.3661 },
    { id: "8", empire: "Fatimid Caliphate", oldName: "Cairo", modernName: "Cairo", lat: 30.0444, lon: 31.2357 },
    { id: "9", empire: "Seljuk Empire", oldName: "Samarkand", modernName: "Samarkand", lat: 39.627, lon: 66.9783 },
    { id: "10", empire: "Mongol Empire", oldName: "Karakorum", modernName: "Ulaanbaatar", lat: 47.9212, lon: 103.8467 },
    { id: "11", empire: "Mughal Empire", oldName: "Delhi", modernName: "Delhi", lat: 28.7041, lon: 77.1025 },
    { id: "12", empire: "Ethiopian Empire", oldName: "Gondar", modernName: "Gondar", lat: 12.6115, lon: 37.4666 },
  ];

  useLayoutEffect(() => {
    const root = am5.Root.new(chartRef.current);
    root.setThemes([am5themes_Animated.new(root)]);

    const chart = root.container.children.push(
      am5map.MapChart.new(root, {
        projection: am5map.geoEqualEarth(),
      })
    );

    chartInstanceRef.current = chart;

    const polygonSeries = chart.series.push(
      am5map.MapPolygonSeries.new(root, {
        geoJSON: am5geodata_worldLow,
        include: [
          // Europe (all countries)
          "AL", "AD", "AM", "AT", "AZ", "BE", "BA", "BG", "BY", "CH", "CY", "CZ", "DE", 
          "DK", "EE", "ES", "FI", "FR", "GE", "GR", "HR", "HU", "IE", "IT", "KZ", "LI", 
          "LT", "LU", "LV", "MD", "MC", "ME", "MK", "MT", "NL", "NO", "PL", "PT", "RO", 
          "RS", "SE", "SI", "SK", "SM", "TR", "UA", "VA",
        
          // Middle East
          "AE", "AF", "BH", "EG", "IR", "IQ", "IL", "JO", "KW", "LB", "OM", "PS", "QA", 
          "SA", "SY", "YE",

          // North Africa
          "DZ", "EG", "LY", "MA", "SD", "TN", "EH", "ET",
        
          // South Asia
          "IN", "PK", "BD", "LK", "NP", "BT", "MV",
        
          // Eastern Europe minus Russia
          "BY", "UA", "MD", "PL", "CZ", "SK", "HU", "RO", "BG",
        
          // Mongolian area
          "MN", "CN", "KZ", "KG", "UZ", "TJ", "TM",
        ]
      })
    );

    polygonSeries.mapPolygons.template.setAll({
      tooltipText: "{name}",
      interactive: true,
    });

    empires.forEach((empire) => {
      const series = chart.series.push(
        am5map.MapPolygonSeries.new(root, {
          geoJSON: am5geodata_worldLow,
          include: empire.areas,
        })
      );

      series.set("id", empire.id); // Assign an id for reference

      series.mapPolygons.template.setAll({
        fill: am5.color(empire.color),
        tooltipText: `${empire.id} (${empire.period})`,
        interactive: true,
      });
      
    });

    const pointSeries = chart.series.push(am5map.MapPointSeries.new(root, {}));

    markers.forEach((marker) => {
      pointSeries.pushDataItem({
        geometry: {
          type: "Point",
          coordinates: [marker.lon, marker.lat],
        },
        name: marker.oldName,
        empire: marker.empire,
        modernName: marker.modernName,
      });
    });

    pointSeries.bullets.push((root, series, dataItem) => {
      const circle = am5.Circle.new(root, {
        radius: 5,
        fill: am5.color(0xff5533),
        tooltipText: `Empire: ${dataItem.get("empire")}\nOld Name: ${dataItem.get(
          "name"
        )}\nModern Name: ${dataItem.get("modernName")}`,
      });

      return am5.Bullet.new(root, { sprite: circle });
    });

    return () => root.dispose();
  }, []);


  const handleHighlight = (empireId) => {
    const chart = chartInstanceRef.current;

    if (chart) {
      chart.series.each((series) => {
        if (series.get("id") === empireId) {
          series.show(); 
        } else if (series.get("id")) {
          series.hide();
        }
      });
    }
  };

  return (
    <div style={{ display: "flex" }}>
      <div style={{ width: "20%", padding: "10px" }}>
        {empires.map((empire) => (
          <div
            key={empire.id}
            style={{
              padding: "5px",
              cursor: "pointer",
              background: am5.color(empire.color).toCSSHex(),
            }}
            onClick={() => handleHighlight(empire.id)}
          >
            {empire.id} ({empire.period})
          </div>
        ))}
      </div>
      <div ref={chartRef} style={{ width: "800px", height: "400px", border: "2px solid grey", borderRadius: "20px", boxShadow: "2px 3px grey"  }} />
    </div>
  );
};

export default HistoricalMap;
